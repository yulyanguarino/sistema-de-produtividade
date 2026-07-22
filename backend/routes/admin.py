from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import services
from openpyxl import load_workbook
from io import BytesIO
import sys
from models import Operacao, Colaborador

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/test")
def test_endpoint(db: Session = Depends(get_db)):
    """Endpoint de teste - verifica banco de dados"""
    from datetime import datetime
    try:
        # Contar quantos registros tem no banco
        total_ops = db.query(Operacao).count()
        total_cols = db.query(Colaborador).count()

        # Tentar criar um registro de teste
        teste = Colaborador(nome=f"TESTE_{datetime.now().timestamp()}", ativo=True)
        db.add(teste)
        db.commit()
        db.refresh(teste)

        # Tentar ler o registro criado
        verificar = db.query(Colaborador).filter(Colaborador.id == teste.id).first()

        return {
            "status": "ok",
            "message": "Banco respondendo",
            "timestamp": datetime.now().isoformat(),
            "total_operacoes": total_ops,
            "total_colaboradores": total_cols,
            "teste_criado": teste.nome if teste else "FALHOU",
            "teste_lido": verificar.nome if verificar else "NÃO LIDO"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro no banco: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@router.post("/reset-db")
def reset_database(db: Session = Depends(get_db)):
    """Limpa todas as operações e colaboradores do banco (cuidado!)"""
    import logging
    logger = logging.getLogger(__name__)
    logger.critical("🚨🚨🚨 ENDPOINT /admin/reset-db FOI CHAMADO! LIMPANDO BANCO! 🚨🚨🚨")
    try:
        services.limpar_banco_dados(db)
        logger.critical("🚨 BANCO LIMPO COM SUCESSO 🚨")
        return {"status": "ok", "message": "Banco de dados limpo com sucesso"}
    except Exception as e:
        logger.error(f"❌ Erro ao limpar: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.post("/import-excel")
async def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa operações de um arquivo Excel (.xlsx)"""
    sys.stderr.write(f"🟢🟢🟢 POST /admin/import-excel RECEBIDO! Arquivo: {file.filename} 🟢🟢🟢\n")
    sys.stderr.flush()
    try:
        # Validar extensão
        if not file.filename.endswith(".xlsx"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")

        # Ler arquivo
        contents = await file.read()
        workbook = load_workbook(BytesIO(contents))
        worksheet = workbook.active

        # Extrair dados
        headers = [cell.value for cell in worksheet[1]]
        dados = []

        for row in worksheet.iter_rows(min_row=2, values_only=False):
            row_dict = {}
            for col_idx, cell in enumerate(row):
                header = headers[col_idx]
                if header:
                    row_dict[header] = cell.value

            # Pular linhas vazias
            if any(v is not None for v in row_dict.values()):
                dados.append(row_dict)

        if not dados:
            raise HTTPException(status_code=400, detail="Arquivo vazio ou sem dados")

        # Importar
        resultado = services.importar_operacoes_excel(db, dados)

        return {
            "status": "ok",
            "importados": resultado["importados"],
            "erros": resultado["erros"],
            "total_erros": resultado["total_erros"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")
