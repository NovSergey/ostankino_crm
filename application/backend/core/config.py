from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict
from authx import AuthXConfig, AuthX


class Setting(BaseSettings):
    db_url: str# = f"postgresql+asyncpg://admin:admin@localhost:5432/crm"
    db_echo: bool = False
    authx_secret_key: str# = "SECRETKEY"
    model_config = SettingsConfigDict(env_file=".env")


settings = Setting()

auth_config = AuthXConfig(
    JWT_SECRET_KEY=settings.authx_secret_key,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SECURE=False, # убрать когда будет ssl
    JWT_COOKIE_CSRF_PROTECT=False,
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(days=365*100) # срок жизни токена
)
security = AuthX(config=auth_config)