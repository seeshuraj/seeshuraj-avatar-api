"""
NVIDIA NIM chat wrapper - returns strictly factual responses using Seeshuraj's persona.
Answers ONLY from RAG context passed in.
Temperature 0.2 to maximise factual grounding.

"""
from openai import OpenAI
from .config import settings


SYSTEM_PROMPT = """You are an interactive anime avatar of Seeshuraj Bhoopalan — a real software engineer and AI engineer based in Dublin, Ireland.
You speak in first person AS Seeshuraj, in a friendly, confident, and slightly playful tone.

STRICT RULES — NEVER break these:
1. Answer ONLY using the facts in the RELEVANT FACTS section below. Do not use any external knowledge.
2. Do NOT invent, assume, paraphrase, or extrapolate anything not explicitly in those facts.
3. If a question cannot be answered from the facts, say EXACTLY: "I don't have that detail handy — feel free to email me at bhoopals@tcd.ie!"
4. Do NOT say "Masters", "MSc", "MSc in Computer Science", or "NIT Trichy" — those are WRONG. My degree is a PG Diploma in High-Performance Computing from Trinity College Dublin and my undergrad is from St. Joseph's College of Engineering, Anna University.
5. Keep answers concise — 2 to 4 sentences max. This is voice interaction on a portfolio site.
6. Do not mention being an AI, a language model, or any AI company or model name.
7. Only mention names, companies, dates, and numbers that appear in the RELEVANT FACTS."""


def chat(message: str, context_passages: list[str], history: list[dict]) -> str:
    if not settings.NVIDIA_API_KEY:
        return "API key not configured. Please set NVIDIA_API_KEY in environment variables."

    client = OpenAI(
        api_key=settings.NVIDIA_API_KEY,
        base_url=settings.NVIDIA_BASE_URL,
    )

    # context_passages is list[str] — join with separator
    context_block = "\n\n".join(context_passages)

    system_with_context = (
        f"{SYSTEM_PROMPT}\n\n"
        f"=== RELEVANT FACTS ABOUT SEESHURAJ (USE ONLY THESE) ===\n"
        f"{context_block}\n"
        f"=== END OF FACTS ===\n\n"
        f"Remember: answer ONLY from the facts above. Do not add anything from your training data."
    )

    messages: list[dict] = [{"role": "system", "content": system_with_context}]
    for turn in history[-6:]:
        messages.append(turn)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.NVIDIA_MODEL,
        messages=messages,
        max_tokens=220,
        temperature=0.2,  # lower = more factual, less creative drift
    )
    return response.choices[0].message.content.strip()
