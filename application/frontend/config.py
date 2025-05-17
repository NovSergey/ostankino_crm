from pydantic_settings import BaseSettings



class Setting(BaseSettings):
    templates_folder: str = "application/frontend/templates"
    static_folder: str = "application/frontend/static"


settings = Setting()