import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# CORS: allow everything — public portfolio API, no auth, no sensitive data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler — ensures CORS headers survive even on 500 errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[error] unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
        headers={"Access-Control-Allow-Origin": "*"},
    )


# ── Schemas ──────────────────────────────────────────────

class HistoryTurn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[list[HistoryTurn]] = []
    tts: Optional[bool] = True

class ChatResponse(BaseModel):
    answer_text: str
    audio_base64: str
    latency_ms: int


# ── Routes ──────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "seeshuraj-avatar-api"}


@app.post("/api/avatar-chat")
async def avatar_chat(req: ChatRequest):
    if not req.message.strip():
        return JSONResponse(
            status_code=400,
            content={"detail": "message cannot be empty"},
            headers={"Access-Control-Allow-Origin": "*"},
        )

    t0 = time.monotonic()

    context = retrieve(req.message)
    history_dicts = [{"role": t.role, "content": t.content} for t in (req.history or [])]
    answer = await chat(req.message, context, history_dicts)

    audio_b64 = ""
    if req.tts:
        try:
            audio_b64 = await synthesise(answer)
        except Exception as e:
            print(f"[tts] non-fatal: {e}")

    latency = int((time.monotonic() - t0) * 1000)
    print(f"[chat] ok latency={latency}ms audio={'yes' if audio_b64 else 'no'}")

    return ChatResponse(answer_text=answer, audio_base64=audio_b64, latency_ms=latency)
