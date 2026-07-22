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

# Para PostgreSQL, não precisa de connect_args
# Para SQLite, precisa de check_same_thread=False
connect_args = {}
if "sqlite" in settings.get_database_url:
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.get_database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
