from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    EXPIRY_TIME: int
    ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    OTP_EXPIRATION_TIME: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

settings = Settings()

