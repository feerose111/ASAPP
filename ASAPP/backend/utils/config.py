from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    HF_TOKEN: str
    BACKEND_URL: Optional[str] = None

    PLAN_MODEL: str = ""
    CREATE_PROJECT_URL: str = ""
    CHAT_URL: str = ""


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()