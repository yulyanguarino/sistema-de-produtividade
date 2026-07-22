from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    # Em produção (Render): usar DATABASE_URL (Neon PostgreSQL)
    # Localmente: usar SQLite como padrão
    # Se tiver postgresql://, converter para postgresql+psycopg://
    _raw_url: str = os.getenv("DATABASE_URL", "sqlite:///./produtividade.db")

    @property
    def database_url(self) -> str:
        url = self._raw_url
        # Converter postgresql:// para postgresql+psycopg://
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def get_database_url(self) -> str:
        return self.database_url


settings = Settings()

import logging
logger = logging.getLogger(__name__)

db_url = settings.get_database_url
# Mascarar senha nos logs
db_url_safe = db_url.replace(db_url.split("@")[0].split("://")[1], "***:***") if "@" in db_url else db_url
logger.info(f"📊 Conectando ao banco: {db_url_safe}")

# Para PostgreSQL, não precisa de connect_args
# Para SQLite, precisa de check_same_thread=False
connect_args = {}
if "sqlite" in db_url:
    connect_args = {"check_same_thread": False}
    logger.info("📁 Usando SQLite (local)")
else:
    logger.info("🔵 Usando PostgreSQL (Neon)")

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=300,  # Recicla conexões a cada 5 min (Neon morre após 5-15 min)
    pool_size=5,
    max_overflow=10,
    connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
