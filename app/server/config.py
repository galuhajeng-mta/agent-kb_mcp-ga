from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 7310
    API_KEY: Optional[str] = None
