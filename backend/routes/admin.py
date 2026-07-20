from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import services

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/reset-db")
def reset_database(db: Session = Depends(get_db)):
    """Limpa todas as operações e colaboradores do banco (cuidado!)"""
    try:
        services.limpar_banco_dados(db)
        return {"status": "ok", "message": "Banco de dados limpo com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
