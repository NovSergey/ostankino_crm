from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):

    db_url: str = f"postgresql+asyncpg://admin:admin@localhost:5432/crm"
    db_echo: bool = False


settings = Setting()