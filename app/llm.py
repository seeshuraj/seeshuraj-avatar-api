"""
Grok (xAI) wrapper with Seeshuraj anime persona.
Uses the OpenAI-compatible xAI API.
"""

import httpx
import json
from app.config import settings

XAI_BASE_URL = "https://api.x.ai/v1"
MODEL = "grok-3-fast"

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
            "My AI brain isn't connected yet — the API key isn't set. "
            "But feel free to email me at bhoopals@tcd.ie!"
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"Relevant information about Seeshuraj:\n{context}",
        },
    ]
    # Append recent history (cap at last 6 turns to keep tokens low)
    for turn in history[-6:]:
        messages.append(turn)
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 256,
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            f"{XAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.xai_api_key}",
                "Content-Type": "application/json",
            },
            content=json.dumps(payload),
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
