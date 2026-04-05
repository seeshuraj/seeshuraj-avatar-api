from pydantic_settings import BaseSettings
from typing import List
import json, os

class Settings(BaseSettings):
    # LLM
    XAI_API_KEY: str = ""
    XAI_MODEL: str = "grok-3-fast"

    # Azure TTS
    SPEECH_KEY: str = ""
    SPEECH_REGION: str = "westeurope"
    SPEECH_VOICE: str = "en-US-AriaNeural"

    # CORS — stored as JSON string in env: '["https://yourdomain.com"]'
    ALLOWED_ORIGINS: str = '["*"]'

    @property
    def origins(self) -> List[str]:
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except Exception:
            return ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
