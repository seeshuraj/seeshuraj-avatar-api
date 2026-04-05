import time
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from typing import List, Optional

from .config import settings
from .rag import retrieve
from .llm import chat
from .tts import synthesise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Seeshuraj Avatar API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ────────────────────────────────────────────────

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    tts_enabled: Optional[bool] = True

    @field_validator("history", mode="before")
    @classmethod
    def sanitise_history(cls, v):
        """Accept list of dicts or Message objects; drop any malformed entries."""
        if v is None:
            return []
        cleaned = []
        for item in v:
            try:
                if isinstance(item, dict):
                    role = str(item.get("role", "")).strip()
                    content = str(item.get("content", "")).strip()
                    if role and content:
                        cleaned.append({"role": role, "content": content})
                elif isinstance(item, Message):
                    if item.role and item.content:
                        cleaned.append(item)
            except Exception:
                pass  # silently skip unparseable entries
        return cleaned

    @field_validator("message", mode="before")
    @classmethod
    def message_not_empty(cls, v):
        v = str(v).strip() if v else ""
        if not v:
            raise ValueError("message must not be empty")
        return v


class ChatResponse(BaseModel):
    answer: str
    audio_base64: str
    latency_ms: int


# ── 422 debug middleware — logs the actual body that failed validation ────────

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    body = await request.body()
    logger.error("422 Unprocessable Entity | body: %s | errors: %s", body.decode(), exc)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors() if hasattr(exc, "errors") else str(exc)},
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.1.0"}


@app.post("/api/avatar-chat", response_model=ChatResponse)
def avatar_chat(req: ChatRequest):
    t0 = time.perf_counter()

    passages = retrieve(req.message)
    history_dicts = [
        {"role": m.role, "content": m.content}
        for m in (req.history or [])
    ]

    answer = chat(req.message, passages, history_dicts)
    audio_b64 = synthesise(answer) if req.tts_enabled else ""
    latency = int((time.perf_counter() - t0) * 1000)

    logger.info("chat OK | %.0fms | turns=%d", latency, len(history_dicts))

    return ChatResponse(answer=answer, audio_base64=audio_b64, latency_ms=latency)
