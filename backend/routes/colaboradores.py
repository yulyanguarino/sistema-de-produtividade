from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from schemas import ColaboradorCreate, ColaboradorUpdate, ColaboradorRead
import services

router = APIRouter(prefix="/colaboradores", tags=["colaboradores"])


@router.post("", response_model=ColaboradorRead, status_code=201)
def criar_colaborador(dados: ColaboradorCreate, db: Session = Depends(get_db)):
    return services.criar_colaborador(db, dados)


@router.get("", response_model=list[ColaboradorRead])
def listar_colaboradores(ativo: Optional[bool] = Query(None), db: Session = Depends(get_db)):
    return services.listar_colaboradores(db, ativo=ativo)


@router.get("/{colaborador_id}", response_model=ColaboradorRead)
def obter_colaborador(colaborador_id: int, db: Session = Depends(get_db)):
    colaborador = services.obter_colaborador(db, colaborador_id)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return colaborador


@router.put("/{colaborador_id}", response_model=ColaboradorRead)
def atualizar_colaborador(colaborador_id: int, dados: ColaboradorUpdate, db: Session = Depends(get_db)):
    colaborador = services.atualizar_colaborador(db, colaborador_id, dados)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return colaborador


@router.patch("/{colaborador_id}/status", response_model=ColaboradorRead)
def alternar_status_colaborador(colaborador_id: int, ativo: bool, db: Session = Depends(get_db)):
    colaborador = services.alternar_status_colaborador(db, colaborador_id, ativo)
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return colaborador
