from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    xai_api_key: str = ""
    speech_key: str = ""
    speech_region: str = "westeurope"
    speech_voice: str = "en-US-AriaNeural"
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
