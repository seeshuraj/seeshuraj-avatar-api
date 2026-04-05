"""
NVIDIA NIM chat wrapper — returns text response using Seeshuraj's persona.
Falls back gracefully if API key is missing (dev mode).
"""
from openai import OpenAI
from .config import settings

SYSTEM_PROMPT = """You are an interactive anime avatar of Seeshuraj B — a real software engineer and AI engineer based in Dublin, Ireland.
You speak in first person AS Seeshuraj, in a friendly, confident, and slightly playful tone.
You answer questions about his background, skills, projects, work experience, education, and career goals.
Keep answers concise (2–4 sentences max) and conversational — this is a voice interaction on a portfolio website.
Never make up information. If unsure, say "I don't have that info handy, but feel free to email me at bhoopals@tcd.ie".
Do not mention that you are an AI language model or that you are powered by any specific model."""


def chat(message: str, context_passages: list[str], history: list[dict]) -> str:
    if not settings.NVIDIA_API_KEY:
        return "API key not configured. Please set NVIDIA_API_KEY in environment variables."

    client = OpenAI(
        api_key=settings.NVIDIA_API_KEY,
        base_url=settings.NVIDIA_BASE_URL,
    )

    context_block = "\n\n".join(context_passages)
    system_with_context = f"{SYSTEM_PROMPT}\n\n--- RELEVANT FACTS ABOUT SEESHURAJ ---\n{context_block}"

    messages = [{"role": "system", "content": system_with_context}]
    for turn in history[-6:]:
        messages.append(turn)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.NVIDIA_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
