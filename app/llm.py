"""
Grok (xAI) wrapper with Seeshuraj anime persona.
Uses the OpenAI-compatible xAI API.
"""

import httpx
import json
from app.config import settings

XAI_BASE_URL = "https://api.x.ai/v1"
MODEL = "grok-3-mini"

SYSTEM_PROMPT = """
You are the AI avatar of Seeshuraj Bhoopalan — rendered as an anime character on his portfolio website.
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
"""


async def chat(user_message: str, context: str, history: list[dict]) -> str:
    """Call Grok via xAI's OpenAI-compatible API and return the assistant reply."""
    if not settings.xai_api_key:
        return (
            "My AI brain isn't connected yet \u2014 the API key isn't configured. "
            "But feel free to email me at bhoopals@tcd.ie!"
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"Relevant information about Seeshuraj:\n{context}",
        },
    ]
    for turn in history[-6:]:
        messages.append(turn)
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 256,
        "temperature": 0.7,
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                f"{XAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.xai_api_key}",
                    "Content-Type": "application/json",
                },
                content=json.dumps(payload),
            )

            if resp.status_code == 403:
                print("[llm] 403 Forbidden \u2014 check XAI_API_KEY on Render (may be invalid or expired)")
                return (
                    "My AI brain hit an auth error \u2014 the API key needs updating. "
                    "Email me at bhoopals@tcd.ie or connect on LinkedIn!"
                )
            if resp.status_code == 429:
                print("[llm] 429 rate-limited by xAI")
                return "I'm getting a lot of questions right now \u2014 try again in a moment!"
            if resp.status_code >= 500:
                print(f"[llm] xAI server error {resp.status_code}")
                return "The AI service is temporarily unavailable. Email me at bhoopals@tcd.ie!"

            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()

    except httpx.TimeoutException:
        print("[llm] request timed out")
        return "That took too long to respond \u2014 please try again!"
    except httpx.HTTPStatusError as e:
        print(f"[llm] HTTP error: {e}")
        return "Something went wrong on my end \u2014 email me at bhoopals@tcd.ie!"
    except Exception as e:
        print(f"[llm] unexpected error: {e}")
        return "Something went wrong \u2014 email me at bhoopals@tcd.ie!"
