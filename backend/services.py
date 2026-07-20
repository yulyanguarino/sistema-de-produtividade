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
