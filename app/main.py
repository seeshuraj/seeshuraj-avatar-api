import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import Any, List, Optional

from .config import settings
from .rag import retrieve
from .llm import chat
from .tts import synthesise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Seeshuraj Avatar API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ───────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    # Use List[Any] so Pydantic never tries to coerce individual items
    # We sanitise manually in the validator below
    history: Optional[List[Any]] = []
    tts_enabled: Optional[bool] = True

    @field_validator("message", mode="before")
    @classmethod
    def message_not_empty(cls, v):
        v = str(v).strip() if v else ""
        if not v:
            raise ValueError("message must not be empty")
        return v

    def clean_history(self) -> list[dict]:
        """Return history as clean [{role, content}] dicts, dropping any bad entries."""
        result = []
        for item in (self.history or []):
            try:
                if isinstance(item, dict):
                    role    = str(item.get("role",    "")).strip()
                    content = str(item.get("content", "")).strip()
                elif hasattr(item, "role") and hasattr(item, "content"):
                    role    = str(item.role).strip()
                    content = str(item.content).strip()
                else:
                    continue
                if role in ("user", "assistant") and content:
                    result.append({"role": role, "content": content})
            except Exception:
                pass
        return result


class ChatResponse(BaseModel):
    answer: str
    audio_base64: str
    latency_ms: int


# ── 422 debug handler — logs exact body so we can see what failed ─────────────

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    body = await request.body()
    logger.error(
        "422 | url=%s | body=%s | errors=%s",
        request.url.path,
        body.decode(errors="replace"),
        exc,
    )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors() if hasattr(exc, "errors") else str(exc)},
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Seeshuraj Avatar API v1.2.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.2.0"}


@app.post("/api/avatar-chat", response_model=ChatResponse)
def avatar_chat(req: ChatRequest):
    t0 = time.perf_counter()

    passages     = retrieve(req.message)
    history_safe = req.clean_history()          # always a clean list[dict]
    answer       = chat(req.message, passages, history_safe)
    audio_b64    = synthesise(answer) if req.tts_enabled else ""
    latency      = int((time.perf_counter() - t0) * 1000)

    logger.info("OK | %.0fms | history_turns=%d", latency, len(history_safe))

    return ChatResponse(answer=answer, audio_base64=audio_b64, latency_ms=latency)
