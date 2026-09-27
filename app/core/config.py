from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    EXPIRY_TIME: int

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

settings = Settings()

