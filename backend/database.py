from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "Dash_Estoque"
    db_user: str = "postgres"
    db_password: str = "postgres"
    database_url: str = "sqlite:///./produtividade.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def get_database_url(self) -> str:
        return self.database_url


settings = Settings()

engine = create_engine(settings.get_database_url, pool_pre_ping=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
