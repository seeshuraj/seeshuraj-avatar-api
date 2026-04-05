import time
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.rag import retrieve
from app.llm import chat
from app.tts import synthesise

app = FastAPI(
    title="Seeshuraj Avatar API",
    description="AI avatar backend: Grok LLM + Azure TTS",
    version="1.0.0",
)

# ── CORS: allow all origins unconditionally ──────────────────
# This is a public read-only portfolio API — no auth, no sensitive data.
# We hardcode ["*"] so no env-var parsing can ever break it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response schemas ───────────────────────────────

class HistoryTurn(BaseModel):
    role: str        # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[list[HistoryTurn]] = []
    tts: Optional[bool] = True

class ChatResponse(BaseModel):
    answer_text: str    # matches frontend: data.answer_text
    audio_base64: str   # empty string if TTS disabled / unavailable
    latency_ms: int


# ── Routes ───────────────────────────────────────────────────

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

    # 2. Flatten history to plain dicts for the LLM
    history_dicts = [
        {"role": t.role, "content": t.content}
        for t in (req.history or [])
    ]

    # 3. LLM response
    answer = await chat(req.message, context, history_dicts)

    # 4. TTS — non-fatal: text always returns even if audio fails
    audio_b64 = ""
    if req.tts:
        try:
            audio_b64 = await synthesise(answer)
        except Exception as e:
            print(f"[tts] non-fatal error: {e}")

    latency = int((time.monotonic() - t0) * 1000)
    print(f"[chat] latency={latency}ms tts={'yes' if audio_b64 else 'no'}")

    return ChatResponse(answer_text=answer, audio_base64=audio_b64, latency_ms=latency)
