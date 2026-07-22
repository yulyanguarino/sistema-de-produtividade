from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import colaboradores, operacoes, dashboard, admin
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sistema de Produtividade Operacional",
    description="Sistema web para registrar operações de separação e conferência de pedidos",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    logger.info("🚀 Iniciando aplicação...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas criadas/verificadas com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {str(e)}")


app.include_router(colaboradores.router)
app.include_router(operacoes.router)
app.include_router(dashboard.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "sistema-de-produtividade-backend",
        "docs": "/docs",
    }
