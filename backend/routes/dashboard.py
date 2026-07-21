from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database import get_db
from schemas import DashboardResponse, DashboardFiltrosResponse
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
