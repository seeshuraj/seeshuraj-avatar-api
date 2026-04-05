# seeshuraj-avatar-api

FastAPI backend for Seeshuraj's AI anime avatar — deployed on Render.

## Stack
- **LLM**: xAI Grok-3-fast (OpenAI-compatible API)
- **TTS**: Azure Cognitive Services Neural TTS
- **Framework**: FastAPI + Uvicorn
- **RAG**: In-memory keyword retrieval (CV knowledge base)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/avatar-chat` | Chat with the avatar |

### POST `/api/avatar-chat`
```json
{
  "message": "What are your skills?",
  "history": [],
  "tts": true
}
```
Response:
```json
{
  "answer": "My core stack is Python, TypeScript, C++...",
  "audio_base64": "UklGRi...",
  "latency_ms": 820
}
```

## Local Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real keys
uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs
```

## Deploy on Render
1. Push this repo to GitHub
2. Render → New Web Service → connect repo
3. Set env vars in Render dashboard:
   - `XAI_API_KEY` — from [console.x.ai](https://console.x.ai)
   - `SPEECH_KEY` — Azure Portal → Speech resource → Keys
   - `SPEECH_REGION` — e.g. `westeurope`
   - `ALLOWED_ORIGINS` — `["https://seeshuraj.github.io"]`
4. Render auto-detects `render.yaml` — builds + deploys automatically
5. Copy the deployed URL and paste it into `index.html`:
   ```js
   window.__AVATAR_API_URL = 'https://seeshuraj-avatar-api.onrender.com';
   ```
