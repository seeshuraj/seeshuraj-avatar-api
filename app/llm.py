"""
NVIDIA NIM — meta/llama-3.1-8b-instruct (free, OpenAI-compatible).
GLiNER-PII and GLM-4.7 are NOT chat models — do not use them here.
"""

from openai import AsyncOpenAI
from app.config import settings

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL = "meta/llama-3.1-8b-instruct"

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
- Always respond in plain English, no markdown formatting
"""

FALLBACK = (
    "I'm Seeshuraj — an MSc HPC grad from Trinity College Dublin, passionate about AI, "
    "cloud systems, and full-stack development. Ask me anything about my background or projects!"
)


async def chat(user_message: str, context: str, history: list[dict]) -> str:
    """Call NVIDIA NIM Llama-3.1-8B and return the assistant reply."""
    if not settings.nvidia_api_key:
        return (
            "My AI brain isn't connected yet — the API key isn't configured. "
            "But feel free to email me at bhoopals@tcd.ie!"
        )

    try:
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
        # keep last 6 turns to stay within context window
        for turn in history[-6:]:
            messages.append(turn)
        messages.append({"role": "user", "content": user_message})

        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=400,
            temperature=0.7,
            top_p=0.9,
        )

        choice = response.choices[0]
        finish_reason = choice.finish_reason
        raw_content = choice.message.content if choice.message else None

        print(
            f"[llm] model={MODEL} finish_reason={finish_reason} "
            f"content_len={len(raw_content) if raw_content else 0}"
        )

        if not raw_content or not raw_content.strip():
            print("[llm] empty/null response — using fallback")
            return FALLBACK

        return raw_content.strip()

    except Exception as e:
        err = str(e)
        print(f"[llm] NVIDIA NIM error: {err}")
        if "401" in err or "403" in err or "invalid" in err.lower():
            return "My AI brain hit an auth error — the API key needs updating. Email me at bhoopals@tcd.ie!"
        if "429" in err or "quota" in err.lower():
            return "I'm getting a lot of questions right now — try again in a moment!"
        if "timeout" in err.lower() or "timed out" in err.lower():
            return "My response took too long — try asking again!"
        return FALLBACK
