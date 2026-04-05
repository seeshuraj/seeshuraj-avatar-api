import json
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    xai_api_key: str = ""
    speech_key: str = ""
    speech_region: str = "westeurope"
    speech_voice: str = "en-US-AriaNeural"
    # ALLOWED_ORIGINS env var can be:
    #   - a JSON array string: '["https://seeshuraj.github.io"]'
    #   - a comma-separated string: 'https://seeshuraj.github.io,http://localhost:3000'
    #   - a single origin string: 'https://seeshuraj.github.io'
    #   - '*' or omitted → defaults to allow all
    allowed_origins_raw: str = "*"

    @property
    def allowed_origins(self) -> List[str]:
        raw = self.allowed_origins_raw.strip()
        if raw == "*" or raw == "":
            return ["*"]
        # Try JSON array first
        if raw.startswith("["):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(o).strip() for o in parsed]
            except json.JSONDecodeError:
                pass
        # Comma-separated fallback
        return [o.strip() for o in raw.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        env_prefix = ""
        # Map ALLOWED_ORIGINS env var → allowed_origins_raw field
        fields = {"allowed_origins_raw": {"env": "ALLOWED_ORIGINS"}}


settings = Settings()
