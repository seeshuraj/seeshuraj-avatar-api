"""
Settings — pydantic-settings v2 compatible.
All env vars are read directly by field name (case-insensitive).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    gemini_api_key: str = ""
    speech_key: str = ""
    speech_region: str = "westeurope"
    speech_voice: str = "en-US-AriaNeural"


settings = Settings()
