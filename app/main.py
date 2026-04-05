import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from .config import settings
from .rag import retrieve
from .llm import chat
from .tts import synthesise

app = FastAPI(title="Seeshuraj Avatar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    tts_enabled: Optional[bool] = True


class ChatResponse(BaseModel):
    answer: str
    audio_base64: str
    latency_ms: int


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/avatar-chat", response_model=ChatResponse)
def avatar_chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="message must not be empty")

    t0 = time.perf_counter()
    passages = retrieve(req.message)
    history_dicts = [{"role": m.role, "content": m.content} for m in (req.history or [])]
    answer = chat(req.message, passages, history_dicts)
    audio_b64 = synthesise(answer) if req.tts_enabled else ""
    latency = int((time.perf_counter() - t0) * 1000)
    return ChatResponse(answer=answer, audio_base64=audio_b64, latency_ms=latency)
