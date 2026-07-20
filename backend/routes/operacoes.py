from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database import get_db
from schemas import OperacaoCreate, OperacaoRead, OperacaoReadDetalhado
import services

router = APIRouter(prefix="/operacoes", tags=["operacoes"])


@router.post("", response_model=OperacaoRead, status_code=201)
def criar_operacao(dados: OperacaoCreate, db: Session = Depends(get_db)):
    try:
        return services.criar_operacao(db, dados)
    except services.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=list[OperacaoReadDetalhado])
def listar_operacoes(
    dia: Optional[date] = Query(None),
    mes: Optional[str] = Query(None),
    periodo_inicio: Optional[date] = Query(None),
    periodo_fim: Optional[date] = Query(None),
    separador_id: Optional[int] = Query(None),
    conferente_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    operacoes = services.listar_operacoes(
        db,
        dia=dia,
        mes=mes,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        separador_id=separador_id,
        conferente_id=conferente_id,
        skip=skip,
        limit=limit,
    )
    return [
        OperacaoReadDetalhado(
            **op.__dict__,
            separador_nome=op.separador.nome,
            conferente_nome=op.conferente.nome,
        )
        for op in operacoes
    ]


@router.get("/{operacao_id}", response_model=OperacaoRead)
def obter_operacao(operacao_id: int, db: Session = Depends(get_db)):
    operacao = services.obter_operacao(db, operacao_id)
    if not operacao:
        raise HTTPException(status_code=404, detail="Operação não encontrada")
    return operacao
