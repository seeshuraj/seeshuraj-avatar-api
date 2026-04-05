import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.config import settings
from app.rag import retrieve
from app.llm import chat
from app.tts import synthesise

app = FastAPI(
    title="Seeshuraj Avatar API",
    description="AI avatar backend: Grok LLM + Azure TTS",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


# ── Request / Response schemas ──────────────────────────────

class HistoryTurn(BaseModel):
    role: str  # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[list[HistoryTurn]] = []
    tts: Optional[bool] = True

class ChatResponse(BaseModel):
    answer_text: str        # ← matches frontend: data.answer_text
    audio_base64: str       # empty string if TTS disabled / unavailable
    latency_ms: int


# ── Routes ──────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "seeshuraj-avatar-api"}


@app.post("/api/avatar-chat", response_model=ChatResponse)
async def avatar_chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")

    t0 = time.monotonic()

    # 1. Retrieve relevant context from knowledge base
    context = retrieve(req.message)

    # 2. Convert history to plain dicts for the LLM
    history_dicts = [
        {"role": turn.role, "content": turn.content}
        for turn in (req.history or [])
    ]

    # 3. Get LLM response
    answer = await chat(req.message, context, history_dicts)

    # 4. TTS (optional) — falls back to "" if Azure keys missing
    audio_b64 = ""
    if req.tts:
        try:
            audio_b64 = await synthesise(answer)
        except Exception as tts_err:
            # TTS failure must never kill the text response
            print(f"[tts] error (non-fatal): {tts_err}")
            audio_b64 = ""

    latency = int((time.monotonic() - t0) * 1000)

    return ChatResponse(answer_text=answer, audio_base64=audio_b64, latency_ms=latency)
