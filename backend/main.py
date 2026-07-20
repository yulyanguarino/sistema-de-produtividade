from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import colaboradores, operacoes, dashboard

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
    Base.metadata.create_all(bind=engine)


app.include_router(colaboradores.router)
app.include_router(operacoes.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "sistema-de-produtividade-backend",
        "docs": "/docs",
    }
