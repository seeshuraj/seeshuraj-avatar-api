from pydantic_settings import BaseSettings
from typing import List
import json, os

class Settings(BaseSettings):
    # LLM — NVIDIA NIM (OpenAI-compatible)
    NVIDIA_API_KEY: str = ""
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL: str = "meta/llama-3.1-8b-instruct"

    # Azure TTS
    SPEECH_KEY: str = ""
    SPEECH_REGION: str = "westeurope"
    SPEECH_VOICE: str = "en-US-GuyNeural"

    # CORS — stored as JSON string in env: '["https://yourdomain.com"]'
    ALLOWED_ORIGINS: str = '["https://seeshuraj.github.io"]'

    @property
    def origins(self) -> List[str]:
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except Exception:
            return ["https://seeshuraj.github.io"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
