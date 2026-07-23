import sys
from sqlalchemy import func, desc, asc
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional
from models import Colaborador, Operacao
from schemas import (
    ColaboradorCreate,
    ColaboradorUpdate,
    OperacaoCreate,
    OperacaoUpdate,
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

    return query.order_by(Operacao.id.desc()).offset(skip).limit(limit).all()


def obter_operacao(db: Session, operacao_id: int) -> Optional[Operacao]:
    return db.query(Operacao).filter(Operacao.id == operacao_id).first()


def atualizar_operacao(db: Session, operacao_id: int, dados: OperacaoUpdate) -> Optional[Operacao]:
    operacao = obter_operacao(db, operacao_id)
    if not operacao:
        return None

    update_data = dados.model_dump(exclude_unset=True)

    novo_separador_id = update_data.get("separador_id", operacao.separador_id)
    if not obter_colaborador(db, novo_separador_id):
        raise NotFoundError(f"Separador com ID {novo_separador_id} não encontrado")

    novo_conferente_id = update_data.get("conferente_id", operacao.conferente_id)
    if not obter_colaborador(db, novo_conferente_id):
        raise NotFoundError(f"Conferente com ID {novo_conferente_id} não encontrado")

    for field, value in update_data.items():
        setattr(operacao, field, value)

    db.commit()
    db.refresh(operacao)
    return operacao


def deletar_operacao(db: Session, operacao_id: int) -> bool:
    operacao = obter_operacao(db, operacao_id)
    if not operacao:
        return False

    db.delete(operacao)
    db.commit()
    return True


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

    ticket_medio = round(total_itens_separados / total_pedidos, 2) if total_pedidos > 0 else 0.0

    return IndicadoresRead(
        total_pedidos=total_pedidos,
        total_itens_separados=total_itens_separados,
        total_itens_conferidos=total_itens_conferidos,
        colaboradores_ativos=int(colaboradores_ativos),
        ticket_medio=ticket_medio,
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
    # Retornar as datas completas e ordenadas (NÃO reconstruir com enero)
    datas_set = {r[0] for r in rows if r[0] is not None}
    return sorted(list(datas_set))


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
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ LIMPANDO BANCO DE DADOS - TODAS AS OPERAÇÕES E COLABORADORES SERÃO DELETADOS!")
    db.query(Operacao).delete()
    db.query(Colaborador).delete()
    db.commit()
    logger.warning("⚠️ BANCO DE DADOS LIMPO COM SUCESSO")


def importar_operacoes_excel(db: Session, dados: list[dict]) -> dict:
    """
    Importa operações de uma lista de dicts (vindo de Excel)
    Espera: [{"DATA": date, "SEPARADOR": str, "QTD ITENS(separador)": int,
              "PEDIDÉ": str, "CONFERENTE": str, "QTD ITENS(conferente)": int}, ...]

    Pré-carrega colaboradores e operações existentes em memória para evitar
    fazer múltiplas queries por linha (o que tornava a importação de
    planilhas grandes lenta o suficiente para estourar timeout do servidor).
    """
    from datetime import datetime
    import logging
    logger = logging.getLogger(__name__)

    msg = f"📥 Iniciando importação de {len(dados)} linhas do Excel"
    logger.info(msg)
    importados = 0
    erros = []
    dados_processados = 0
    dados_com_erro = 0
    batch_size = 100  # Commit a cada 100 linhas (evita perda total em caso de erro)

    colaboradores_cache = {c.nome.strip().upper(): c for c in db.query(Colaborador).all()}
    operacoes_cache = {
        (op.data, op.pedido, op.separador_id, op.conferente_id): op
        for op in db.query(Operacao).all()
    }

    def obter_ou_criar_colaborador(nome: str) -> Colaborador:
        chave = nome.upper()
        colaborador = colaboradores_cache.get(chave)
        if not colaborador:
            colaborador = Colaborador(nome=nome, ativo=True)
            db.add(colaborador)
            db.flush()
            colaboradores_cache[chave] = colaborador
        return colaborador

    for idx, row in enumerate(dados, start=2):  # start=2 pois linha 1 é header
        try:
            # Extrair dados
            data = row.get("DATA")
            # Converter datetime para date se necessário (openpyxl retorna datetime)
            if isinstance(data, datetime):
                data = data.date()
            elif isinstance(data, str):
                # Se for string ISO (ex: "2026-01-05T00:00:00"), converter para date
                try:
                    data = datetime.fromisoformat(data.replace('Z', '+00:00')).date()
                except (ValueError, AttributeError):
                    pass  # Deixa como está se não conseguir converter
            pedido = row.get("PEDIDO")
            separador_nome = (row.get("SEPARADOR") or "").strip()
            qtd_sep = row.get("QTD ITENS(separador)")
            conferente_nome = (row.get("CONFERENTE") or "").strip()
            qtd_conf = row.get("QTD ITENS(conferente)")

            # Validações
            if not data or not pedido or not separador_nome or not conferente_nome:
                erros.append(f"Linha {idx}: Dados incompletos (data={data}, pedido={pedido}, sep={separador_nome}, conf={conferente_nome})")
                dados_com_erro += 1
                continue

            dados_processados += 1

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

            separador = obter_ou_criar_colaborador(separador_nome)
            conferente = obter_ou_criar_colaborador(conferente_nome)
            pedido_str = str(pedido).strip()

            # Verificar se operação já existe (evitar duplicatas) - via cache em memória
            chave_operacao = (data, pedido_str, separador.id, conferente.id)
            operacao_existente = operacoes_cache.get(chave_operacao)

            if operacao_existente:
                # Atualizar quantidades se houver diferença
                if (operacao_existente.qtd_itens_separados != qtd_sep or
                    operacao_existente.qtd_itens_conferidos != qtd_conf):
                    operacao_existente.qtd_itens_separados = qtd_sep
                    operacao_existente.qtd_itens_conferidos = qtd_conf
                    importados += 1
            else:
                # Criar operação nova
                operacao = Operacao(
                    data=data,
                    pedido=pedido_str,
                    separador_id=separador.id,
                    qtd_itens_separados=qtd_sep,
                    conferente_id=conferente.id,
                    qtd_itens_conferidos=qtd_conf,
                )
                db.add(operacao)
                operacoes_cache[chave_operacao] = operacao
                importados += 1

        except Exception as e:
            logger.error(f"❌ Erro na linha {idx}: {str(e)}")
            erros.append(f"Linha {idx}: {str(e)}")

        # Commit em batches para evitar perder tudo se algo falhar no meio
        if importados % batch_size == 0 and importados > 0:
            try:
                db.commit()
                logger.info(f"✅ Batch de {batch_size} operações commitado (progresso: linha {idx})")
            except Exception as e:
                msg = f"❌ Erro CRÍTICO ao salvar batch: {str(e)}"
                sys.stderr.write(msg + "\n")
                sys.stderr.flush()
                logger.error(msg)
                db.rollback()
                raise

    try:
        db.commit()
        total_depois_commit = db.query(Operacao).count()
        msg = f"✅ SUCESSO! {importados} operações processadas. Total no banco: {total_depois_commit}"
        logger.info(msg)
    except Exception as e:
        msg = f"❌ ERRO ao salvar no Neon: {str(e)}"
        logger.error(msg)
        db.rollback()
        raise

    return {
        "importados": importados,
        "erros": erros[:10],  # Retornar apenas os 10 primeiros erros
        "total_erros": len(erros),
        "dados_processados": dados_processados,
        "dados_com_erro": dados_com_erro,
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
