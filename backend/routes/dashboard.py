from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database import get_db
from schemas import DashboardResponse, DashboardFiltrosResponse, ProducaoMensalItem, DistribuicaoResponse
import services

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def obter_dashboard(
    dia: Optional[date] = Query(None),
    mes: Optional[str] = Query(None),
    periodo_inicio: Optional[date] = Query(None),
    periodo_fim: Optional[date] = Query(None),
    separador_id: Optional[int] = Query(None),
    conferente_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        return services.montar_dashboard(
            db,
            dia=dia,
            mes=mes,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            separador_id=separador_id,
            conferente_id=conferente_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/filtros", response_model=DashboardFiltrosResponse)
def obter_dashboard_filtros(
    dia: Optional[date] = Query(None),
    mes: Optional[str] = Query(None),
    separador_id: Optional[int] = Query(None),
    conferente_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        return services.montar_dashboard_filtros(
            db, dia=dia, mes=mes, separador_id=separador_id, conferente_id=conferente_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/producao-mensal/separador/{separador_id}", response_model=list[ProducaoMensalItem])
def producao_mensal_separador(separador_id: int, db: Session = Depends(get_db)):
    return services.producao_mensal_separador(db, separador_id)


@router.get("/producao-mensal/conferente/{conferente_id}", response_model=list[ProducaoMensalItem])
def producao_mensal_conferente(conferente_id: int, db: Session = Depends(get_db)):
    return services.producao_mensal_conferente(db, conferente_id)


@router.get("/resultado-mensal", response_model=list[ProducaoMensalItem])
def resultado_mensal(colaborador_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    return services.resultado_mensal_colaborador(db, colaborador_id)


@router.get("/distribuicao", response_model=DistribuicaoResponse)
def obter_distribuicao(
    dia: Optional[date] = Query(None),
    mes: Optional[str] = Query(None),
    periodo_inicio: Optional[date] = Query(None),
    periodo_fim: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    # Sempre a participação de TODO MUNDO no período (o front destaca a fatia
    # do colaborador selecionado vs. "Outros" quando um filtro está ativo -
    # não faz sentido calcular % de alguém sem saber o total geral).
    try:
        return DistribuicaoResponse(
            separadores=services.calcular_ranking_separadores(db, dia, mes, periodo_inicio, periodo_fim),
            conferentes=services.calcular_ranking_conferentes(db, dia, mes, periodo_inicio, periodo_fim),
            total=services.calcular_ranking_total(db, dia, mes, periodo_inicio, periodo_fim),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
