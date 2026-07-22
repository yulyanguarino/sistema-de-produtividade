from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    # APENAS Neon PostgreSQL
    _raw_url: str = os.getenv("DATABASE_URL")

    @property
    def database_url(self) -> str:
        if not self._raw_url:
            raise ValueError("DATABASE_URL não configurada! Use variável de ambiente.")

        url = self._raw_url
        # Converter postgresql:// para postgresql+psycopg://
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def get_database_url(self) -> str:
        return self.database_url


settings = Settings()

import logging
logger = logging.getLogger(__name__)

db_url = settings.get_database_url
# Mascarar senha nos logs
db_url_safe = db_url.replace(db_url.split("@")[0].split("://")[1], "***:***") if "@" in db_url else db_url
logger.info(f"🔵 Conectando ao Neon PostgreSQL: {db_url_safe}")

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
