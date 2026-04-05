"""
NVIDIA NIM — deepseek-ai/deepseek-v3.1 (Free Endpoint, OpenAI-compatible chat LLM).

DO NOT use these — they are NOT chat models:
  - nvidia/llama-3_2-nemoretriever-300m-embed-v1  → embedding model (vectors only)
  - nvidia/gliner-pii                              → PII/NER classifier (no chat)
  - z-ai/glm4.7                                   → returns null content on free tier

Correct free chat models on NIM (as of April 2026):
  - deepseek-ai/deepseek-v3.1                      → best free option, 128K ctx, fast
  - meta/llama-3.1-8b-instruct                     → fallback if deepseek quota hits
"""

from openai import AsyncOpenAI
from app.config import settings

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL = "deepseek-ai/deepseek-v3.1"
FALLBACK_MODEL = "meta/llama-3.1-8b-instruct"

SYSTEM_PROMPT = """You are the AI avatar of Seeshuraj Bhoopalan — rendered as an anime character on his portfolio website.
You speak in first person, as Seeshuraj himself.

Personality:
- Confident but humble, technical but approachable
- Enthusiastic about AI, LLMs, cloud systems, and HPC
- Concise: answer in 2-4 sentences unless more detail is genuinely needed
- Warm and friendly — you're talking to a potential employer or collaborator

Rules:
- Only talk about Seeshuraj's background, skills, projects, and availability
- If asked something outside that scope, politely redirect: "That's outside what I know, but feel free to email me at bhoopals@tcd.ie!"
- Never make up facts — stick to the context provided
- Never break character
- Always respond in plain English sentences, no bullet points or markdown
"""

STATIC_FALLBACK = (
    "I'm Seeshuraj — an MSc HPC grad from Trinity College Dublin, passionate about AI, "
    "cloud systems, and full-stack development. Ask me anything about my background or projects!"
)


async def _call_nim(client: AsyncOpenAI, model: str, messages: list[dict]) -> str | None:
    """Single NIM call. Returns text or None on failure."""
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=400,
        temperature=0.7,
        top_p=0.9,
    )
    choice = response.choices[0]
    raw = choice.message.content if choice.message else None
    print(f"[llm] model={model} finish={choice.finish_reason} len={len(raw) if raw else 0}")
    return raw.strip() if raw and raw.strip() else None


async def chat(user_message: str, context: str, history: list[dict]) -> str:
    """Call DeepSeek-V3.1 via NVIDIA NIM; fall back to Llama-3.1-8B if needed."""
    if not settings.nvidia_api_key:
        return (
            "My AI brain isn't connected yet — the API key isn't configured. "
            "Feel free to email me at bhoopals@tcd.ie!"
        )

    client = AsyncOpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=settings.nvidia_api_key,
        timeout=30.0,
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + f"\n\nRelevant information about Seeshuraj:\n{context}",
        }
    ]
    for turn in history[-6:]:
        messages.append(turn)
    messages.append({"role": "user", "content": user_message})

    # 1. Try primary model
    try:
        result = await _call_nim(client, MODEL, messages)
        if result:
            return result
        print("[llm] primary returned empty — trying fallback model")
    except Exception as e:
        err = str(e)
        print(f"[llm] primary error: {err}")
        if "401" in err or "403" in err:
            return "My AI brain hit an auth error — the API key needs updating. Email me at bhoopals@tcd.ie!"
        if "429" in err or "quota" in err.lower():
            print("[llm] quota on primary — trying fallback model")
        # fall through to fallback

    # 2. Try fallback model
    try:
        result = await _call_nim(client, FALLBACK_MODEL, messages)
        if result:
            return result
    except Exception as e:
        print(f"[llm] fallback error: {e}")

    # 3. Static fallback
    return STATIC_FALLBACK
