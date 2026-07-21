from sqlalchemy import func, desc, asc
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional
from models import Colaborador, Operacao
from schemas import (
    ColaboradorCreate,
    ColaboradorUpdate,
    OperacaoCreate,
    IndicadoresRead,
    RankingItem,
    RankingResponse,
    DashboardResponse,
    ColaboradorFiltroItem,
    DashboardFiltrosResponse,
)


class NotFoundError(Exception):
    pass


# ---- Colaboradores ----
def criar_colaborador(db: Session, dados: ColaboradorCreate) -> Colaborador:
    colaborador = Colaborador(**dados.model_dump())
    db.add(colaborador)
    db.commit()
    db.refresh(colaborador)
    return colaborador


def listar_colaboradores(db: Session, ativo: Optional[bool] = None) -> list[Colaborador]:
    query = db.query(Colaborador)
    if ativo is not None:
        query = query.filter(Colaborador.ativo == ativo)
    return query.all()


def obter_colaborador(db: Session, colaborador_id: int) -> Optional[Colaborador]:
    return db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()


def atualizar_colaborador(db: Session, colaborador_id: int, dados: ColaboradorUpdate) -> Optional[Colaborador]:
    colaborador = obter_colaborador(db, colaborador_id)
    if not colaborador:
        return None

    update_data = dados.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(colaborador, field, value)

    db.commit()
    db.refresh(colaborador)
    return colaborador


def alternar_status_colaborador(db: Session, colaborador_id: int, ativo: bool) -> Optional[Colaborador]:
    colaborador = obter_colaborador(db, colaborador_id)
    if not colaborador:
        return None

    colaborador.ativo = ativo
    db.commit()
    db.refresh(colaborador)
    return colaborador


def deletar_colaborador(db: Session, colaborador_id: int) -> bool:
    colaborador = obter_colaborador(db, colaborador_id)
    if not colaborador:
        return False

    # Verificar se há operações relacionadas
    ops_como_separador = db.query(Operacao).filter(Operacao.separador_id == colaborador_id).count()
    ops_como_conferente = db.query(Operacao).filter(Operacao.conferente_id == colaborador_id).count()

    if ops_como_separador > 0 or ops_como_conferente > 0:
        raise ValueError(
            f"Não é possível deletar este colaborador. "
            f"Existem {ops_como_separador + ops_como_conferente} operação(ões) relacionada(s)."
        )

    db.delete(colaborador)
    db.commit()
    return True


# ---- Operações ----
def criar_operacao(db: Session, dados: OperacaoCreate) -> Operacao:
    separador = obter_colaborador(db, dados.separador_id)
    if not separador:
        raise NotFoundError(f"Separador com ID {dados.separador_id} não encontrado")

    conferente = obter_colaborador(db, dados.conferente_id)
    if not conferente:
        raise NotFoundError(f"Conferente com ID {dados.conferente_id} não encontrado")

    operacao = Operacao(**dados.model_dump())
    db.add(operacao)
    db.commit()
    db.refresh(operacao)
    return operacao


def listar_operacoes(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    periodo_inicio: Optional[date] = None,
    periodo_fim: Optional[date] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Operacao]:
    query = db.query(Operacao)

    query = _aplicar_filtros_data(query, dia, mes, periodo_inicio, periodo_fim)

    if separador_id:
        query = query.filter(Operacao.separador_id == separador_id)
    if conferente_id:
        query = query.filter(Operacao.conferente_id == conferente_id)

    return query.offset(skip).limit(limit).all()


def obter_operacao(db: Session, operacao_id: int) -> Optional[Operacao]:
    return db.query(Operacao).filter(Operacao.id == operacao_id).first()


# ---- Dashboard filtering ----
def _aplicar_filtros_data(
    query,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    periodo_inicio: Optional[date] = None,
    periodo_fim: Optional[date] = None,
):
    num_filtros = sum([dia is not None, mes is not None, periodo_inicio is not None or periodo_fim is not None])
    if num_filtros > 1:
        raise ValueError("Apenas um filtro de data pode ser utilizado: dia, mes, ou periodo")

    if dia:
        query = query.filter(Operacao.data == dia)
    elif mes:
        try:
            mes_date = datetime.strptime(mes, "%Y-%m").date()
            primeiro_dia = mes_date.replace(day=1)
            ultimo_dia = (mes_date.replace(day=28) + __import__("datetime").timedelta(days=4)).replace(day=1) - __import__("datetime").timedelta(days=1)
            query = query.filter(Operacao.data.between(primeiro_dia, ultimo_dia))
        except ValueError:
            raise ValueError("Formato de mês inválido. Use YYYY-MM")
    elif periodo_inicio or periodo_fim:
        if periodo_inicio:
            query = query.filter(Operacao.data >= periodo_inicio)
        if periodo_fim:
            query = query.filter(Operacao.data <= periodo_fim)

    return query


def calcular_indicadores(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    periodo_inicio: Optional[date] = None,
    periodo_fim: Optional[date] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
) -> IndicadoresRead:
    # Helper to build filtered query
    def build_filtered_query():
        q = db.query(Operacao)
        q = _aplicar_filtros_data(q, dia, mes, periodo_inicio, periodo_fim)
        if separador_id:
            q = q.filter(Operacao.separador_id == separador_id)
        if conferente_id:
            q = q.filter(Operacao.conferente_id == conferente_id)
        return q

    # Get count
    total_pedidos = build_filtered_query().count()

    # Get sums
    result = build_filtered_query().with_entities(
        func.coalesce(func.sum(Operacao.qtd_itens_separados), 0),
        func.coalesce(func.sum(Operacao.qtd_itens_conferidos), 0),
    ).first()

    total_itens_separados = int(result[0] or 0) if result else 0
    total_itens_conferidos = int(result[1] or 0) if result else 0

    # Get count of active colaboradores (global, not filtered by date/operacoes)
    colaboradores_ativos = db.query(func.count(Colaborador.id)).filter(Colaborador.ativo == True).scalar() or 0

    return IndicadoresRead(
        total_pedidos=total_pedidos,
        total_itens_separados=total_itens_separados,
        total_itens_conferidos=total_itens_conferidos,
        colaboradores_ativos=int(colaboradores_ativos),
    )


def calcular_ranking_separadores(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    periodo_inicio: Optional[date] = None,
    periodo_fim: Optional[date] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
    limit: Optional[int] = None,
) -> list[RankingItem]:
    query = db.query(
        Colaborador.id,
        Colaborador.nome,
        func.count(Operacao.id).label("qtd_pedidos"),
        func.coalesce(func.sum(Operacao.qtd_itens_separados), 0).label("qtd_itens"),
    ).join(Operacao, Operacao.separador_id == Colaborador.id)

    query = _aplicar_filtros_data(query, dia, mes, periodo_inicio, periodo_fim)
    if separador_id:
        query = query.filter(Operacao.separador_id == separador_id)
    if conferente_id:
        query = query.filter(Operacao.conferente_id == conferente_id)

    query = query.group_by(Colaborador.id, Colaborador.nome).order_by(desc(func.sum(Operacao.qtd_itens_separados)))

    if limit:
        query = query.limit(limit)

    results = query.all()
    return [
        RankingItem(
            colaborador_id=r[0],
            colaborador_nome=r[1],
            qtd_pedidos=r[2],
            qtd_itens=int(r[3] or 0),
        )
        for r in results
    ]


def calcular_ranking_conferentes(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    periodo_inicio: Optional[date] = None,
    periodo_fim: Optional[date] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
    limit: Optional[int] = None,
) -> list[RankingItem]:
    query = db.query(
        Colaborador.id,
        Colaborador.nome,
        func.count(Operacao.id).label("qtd_pedidos"),
        func.coalesce(func.sum(Operacao.qtd_itens_conferidos), 0).label("qtd_itens"),
    ).join(Operacao, Operacao.conferente_id == Colaborador.id)

    query = _aplicar_filtros_data(query, dia, mes, periodo_inicio, periodo_fim)
    if separador_id:
        query = query.filter(Operacao.separador_id == separador_id)
    if conferente_id:
        query = query.filter(Operacao.conferente_id == conferente_id)

    query = query.group_by(Colaborador.id, Colaborador.nome).order_by(desc(func.sum(Operacao.qtd_itens_conferidos)))

    if limit:
        query = query.limit(limit)

    results = query.all()
    return [
        RankingItem(
            colaborador_id=r[0],
            colaborador_nome=r[1],
            qtd_pedidos=r[2],
            qtd_itens=int(r[3] or 0),
        )
        for r in results
    ]


# ---- Dashboard Filters (Cascading) ----
def _obter_meses_disponiveis(
    db: Session,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
) -> list[str]:
    query = db.query(Operacao.data).distinct()
    if separador_id:
        query = query.filter(Operacao.separador_id == separador_id)
    if conferente_id:
        query = query.filter(Operacao.conferente_id == conferente_id)
    rows = query.all()
    meses_set = {d[0].strftime("%Y-%m") for d in rows if d[0] is not None}
    return sorted(list(meses_set))


def _obter_dias_disponiveis(
    db: Session,
    mes: Optional[str] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
) -> list[date]:
    query = db.query(Operacao.data).distinct()
    query = _aplicar_filtros_data(query, dia=None, mes=mes, periodo_inicio=None, periodo_fim=None)
    if separador_id:
        query = query.filter(Operacao.separador_id == separador_id)
    if conferente_id:
        query = query.filter(Operacao.conferente_id == conferente_id)
    rows = query.all()
    if not rows:
        return []
    dias_set = set(r[0].day for r in rows)
    dias_ordenados = sorted(dias_set)
    primeiro_ano = rows[0][0].year
    mes_com_31_dias = datetime.strptime(f"{primeiro_ano}-01-01", "%Y-%m-%d").date()
    resultado = []
    for d in dias_ordenados:
        resultado.append(mes_com_31_dias.replace(day=d))
    return resultado


def _obter_separadores_disponiveis(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    conferente_id: Optional[int] = None,
) -> list[Colaborador]:
    query = (
        db.query(Colaborador)
        .join(Operacao, Operacao.separador_id == Colaborador.id)
        .distinct()
    )
    query = _aplicar_filtros_data(query, dia=dia, mes=mes, periodo_inicio=None, periodo_fim=None)
    if conferente_id:
        query = query.filter(Operacao.conferente_id == conferente_id)
    return query.order_by(Colaborador.nome.asc()).all()


def _obter_conferentes_disponiveis(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    separador_id: Optional[int] = None,
) -> list[Colaborador]:
    query = (
        db.query(Colaborador)
        .join(Operacao, Operacao.conferente_id == Colaborador.id)
        .distinct()
    )
    query = _aplicar_filtros_data(query, dia=dia, mes=mes, periodo_inicio=None, periodo_fim=None)
    if separador_id:
        query = query.filter(Operacao.separador_id == separador_id)
    return query.order_by(Colaborador.nome.asc()).all()


def montar_dashboard_filtros(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
) -> DashboardFiltrosResponse:
    meses = _obter_meses_disponiveis(db, separador_id, conferente_id)
    dias = _obter_dias_disponiveis(db, mes, separador_id, conferente_id)
    separadores = _obter_separadores_disponiveis(db, dia, mes, conferente_id)
    conferentes = _obter_conferentes_disponiveis(db, dia, mes, separador_id)

    return DashboardFiltrosResponse(
        meses=meses,
        dias=dias,
        separadores=[ColaboradorFiltroItem(id=c.id, nome=c.nome) for c in separadores],
        conferentes=[ColaboradorFiltroItem(id=c.id, nome=c.nome) for c in conferentes],
    )


# ---- Admin ----
def limpar_banco_dados(db: Session) -> None:
    """Deleta todas as operações e colaboradores"""
    db.query(Operacao).delete()
    db.query(Colaborador).delete()
    db.commit()


def importar_operacoes_excel(db: Session, dados: list[dict]) -> dict:
    """
    Importa operações de uma lista de dicts (vindo de Excel)
    Espera: [{"DATA": date, "SEPARADOR": str, "QTD ITENS(separador)": int,
              "PEDIDÉ": str, "CONFERENTE": str, "QTD ITENS(conferente)": int}, ...]
    """
    from datetime import datetime

    importados = 0
    erros = []

    for idx, row in enumerate(dados, start=2):  # start=2 pois linha 1 é header
        try:
            # Normalizar nomes de colunas (aceita PEDIDO ou PEDIDÉ)
            data = row.get("DATA")
            # Converter datetime para date se necessário (openpyxl retorna datetime)
            if isinstance(data, datetime):
                data = data.date()
            pedido = row.get("PEDIDO") or row.get("PEDIDÉ")
            separador_nome = row.get("SEPARADOR", "").strip()
            qtd_sep = row.get("QTD ITENS(separador)")
            conferente_nome = row.get("CONFERENTE", "").strip()
            qtd_conf = row.get("QTD ITENS(conferente)")

            # Validações
            if not data or not pedido or not separador_nome or not conferente_nome:
                erros.append(f"Linha {idx}: Dados incompletos")
                continue

            # Converter quantidades para int (ignorar se for fórmula ou inválido)
            try:
                qtd_sep = int(float(str(qtd_sep).replace("=", ""))) if qtd_sep else 0
                qtd_conf = int(float(str(qtd_conf).replace("=", ""))) if qtd_conf else 0
            except (ValueError, TypeError):
                erros.append(f"Linha {idx}: Quantidades inválidas (não são números)")
                continue

            if qtd_sep <= 0 or qtd_conf <= 0:
                erros.append(f"Linha {idx}: Quantidades devem ser maiores que 0")
                continue

            # Buscar/criar colaboradores
            separador = db.query(Colaborador).filter(
                Colaborador.nome.ilike(separador_nome)
            ).first()
            if not separador:
                separador = Colaborador(nome=separador_nome, ativo=True)
                db.add(separador)
                db.flush()

            conferente = db.query(Colaborador).filter(
                Colaborador.nome.ilike(conferente_nome)
            ).first()
            if not conferente:
                conferente = Colaborador(nome=conferente_nome, ativo=True)
                db.add(conferente)
                db.flush()

            # Verificar se operação já existe (evitar duplicatas)
            operacao_existente = db.query(Operacao).filter(
                Operacao.data == data,
                Operacao.pedido == str(pedido).strip(),
                Operacao.separador_id == separador.id,
                Operacao.conferente_id == conferente.id,
            ).first()

            if operacao_existente:
                # Atualizar quantidades se houver diferença
                if (operacao_existente.qtd_itens_separados != qtd_sep or
                    operacao_existente.qtd_itens_conferidos != qtd_conf):
                    operacao_existente.qtd_itens_separados = qtd_sep
                    operacao_existente.qtd_itens_conferidos = qtd_conf
                    db.add(operacao_existente)
                    importados += 1
            else:
                # Criar operação nova
                operacao = Operacao(
                    data=data,
                    pedido=str(pedido).strip(),
                    separador_id=separador.id,
                    qtd_itens_separados=qtd_sep,
                    conferente_id=conferente.id,
                    qtd_itens_conferidos=qtd_conf,
                )
                db.add(operacao)
                importados += 1

        except Exception as e:
            erros.append(f"Linha {idx}: {str(e)}")

    db.commit()

    return {
        "importados": importados,
        "erros": erros,
        "total_erros": len(erros),
    }


def montar_dashboard(
    db: Session,
    dia: Optional[date] = None,
    mes: Optional[str] = None,
    periodo_inicio: Optional[date] = None,
    periodo_fim: Optional[date] = None,
    separador_id: Optional[int] = None,
    conferente_id: Optional[int] = None,
) -> DashboardResponse:
    indicadores = calcular_indicadores(
        db, dia, mes, periodo_inicio, periodo_fim, separador_id, conferente_id
    )

    ranking_separadores = calcular_ranking_separadores(
        db, dia, mes, periodo_inicio, periodo_fim, separador_id, conferente_id
    )
    ranking_conferentes = calcular_ranking_conferentes(
        db, dia, mes, periodo_inicio, periodo_fim, separador_id, conferente_id
    )

    ranking = RankingResponse(
        separadores=ranking_separadores,
        conferentes=ranking_conferentes,
    )

    filtros_aplicados = {
        "dia": dia,
        "mes": mes,
        "periodo_inicio": periodo_inicio,
        "periodo_fim": periodo_fim,
        "separador_id": separador_id,
        "conferente_id": conferente_id,
    }

    return DashboardResponse(
        indicadores=indicadores,
        ranking=ranking,
        filtros_aplicados=filtros_aplicados,
    )
