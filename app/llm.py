"""
Google Gemini wrapper with Seeshuraj anime persona.
Uses google-generativeai SDK (gemini-2.0-flash — free tier).
"""

import google.generativeai as genai
from app.config import settings

MODEL = "gemini-2.0-flash"

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
"""


async def chat(user_message: str, context: str, history: list[dict]) -> str:
    """Call Gemini and return the assistant reply."""
    if not settings.gemini_api_key:
        return (
            "My AI brain isn't connected yet — the API key isn't configured. "
            "But feel free to email me at bhoopals@tcd.ie!"
        )

    try:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(
            model_name=MODEL,
            system_instruction=SYSTEM_PROMPT + f"\n\nRelevant information about Seeshuraj:\n{context}",
        )

        # Build history for multi-turn
        gemini_history = []
        for turn in history[-6:]:
            role = "user" if turn["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [turn["content"]]})

        chat_session = model.start_chat(history=gemini_history)
        response = chat_session.send_message(user_message)
        return response.text.strip()

    except Exception as e:
        err = str(e)
        print(f"[llm] Gemini error: {err}")
        if "API_KEY_INVALID" in err or "403" in err:
            return "My AI brain hit an auth error — the Gemini API key needs updating. Email me at bhoopals@tcd.ie!"
        if "quota" in err.lower() or "429" in err:
            return "I'm getting a lot of questions right now — try again in a moment!"
        return "Something went wrong on my end — email me at bhoopals@tcd.ie!"
