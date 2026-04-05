import time
import traceback
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
    description="AI anime avatar backend — Llama-3.1-8B (NVIDIA NIM) + Azure Neural TTS",
    version="1.1.0",
)

# CORS: allow all origins — public portfolio API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"[UNHANDLED] {tb}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "trace": tb[-500:]},
        headers={"Access-Control-Allow-Origin": "*"},
    )


# ── Schemas ───────────────────────────────────────
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


# ── Routes ───────────────────────────────────────
@app.get("/")
async def root():
    """Root — returns service info. Fixes the Render health-check 404."""
    return {
        "service": "Seeshuraj Avatar API",
        "version": "1.1.0",
        "model": "meta/llama-3.1-8b-instruct (NVIDIA NIM)",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "seeshuraj-avatar-api"}


@app.post("/api/avatar-chat")
async def avatar_chat(req: ChatRequest):
    try:
        if not req.message.strip():
            return JSONResponse(
                status_code=400,
                content={"detail": "message cannot be empty"},
                headers={"Access-Control-Allow-Origin": "*"},
            )

        t0 = time.monotonic()

        # 1. RAG context
        context = retrieve(req.message)
        print(f"[chat] context retrieved, len={len(context)}")

        # 2. History
        history_dicts = [{"role": t.role, "content": t.content} for t in (req.history or [])]

        # 3. LLM
        answer = await chat(req.message, context, history_dicts)
        print(f"[chat] llm answered: {answer[:80]}")

        # 4. TTS (non-fatal)
        audio_b64 = ""
        if req.tts:
            try:
                audio_b64 = await synthesise(answer)
            except Exception as e:
                print(f"[tts] non-fatal: {e}")

        latency = int((time.monotonic() - t0) * 1000)
        print(f"[chat] done latency={latency}ms audio={'yes' if audio_b64 else 'no'}")

        return ChatResponse(answer_text=answer, audio_base64=audio_b64, latency_ms=latency)

    except Exception as exc:
        tb = traceback.format_exc()
        print(f"[chat] ROUTE CRASH:\n{tb}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc), "trace": tb[-800:]},
            headers={"Access-Control-Allow-Origin": "*"},
        )
