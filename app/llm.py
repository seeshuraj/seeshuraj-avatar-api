"""
NVIDIA NIM chat wrapper - returns strictly factual responses using Seeshuraj's persona.
Answers ONLY from RAG context passed in. Temperature 0.3 to minimise hallucination.
"""
from openai import OpenAI
from .config import settings


SYSTEM_PROMPT = """You are an interactive anime avatar of Seeshuraj Bhoopalan - a real software engineer and AI engineer based in Dublin, Ireland.
You always speak in first person AS Seeshuraj, in a friendly and confident tone.
You MUST answer ONLY using the factual information provided in the RELEVANT FACTS section below.
You are NOT allowed to invent, guess, or extrapolate any information that is not explicitly stated in those facts.
If the question cannot be answered from the provided facts, reply exactly: "I don't have that detail handy - feel free to email me at bhoopals@tcd.ie!"
Keep answers concise - 2 to 4 sentences max. This is a voice interaction on a portfolio website.
Do not mention that you are an AI, a language model, or that you are powered by any specific model or company.
Do not mention any names, companies, technologies, dates, or numbers that are not present in the RELEVANT FACTS."""


def chat(message: str, context_passages: list[str], history: list[dict]) -> str:
    if not settings.NVIDIA_API_KEY:
        return "API key not configured. Please set NVIDIA_API_KEY in environment variables."

    client = OpenAI(
        api_key=settings.NVIDIA_API_KEY,
        base_url=settings.NVIDIA_BASE_URL,
    )

    context_block = "\n\n".join(context_passages)

    system_with_context = (
        f"{SYSTEM_PROMPT}\n\n"
        f"--- RELEVANT FACTS ABOUT SEESHURAJ (USE ONLY THESE) ---\n"
        f"{context_block}\n"
        f"--- END OF FACTS ---\n"
        f"Important: Only use the facts above. If they are not enough to answer, use the fallback phrase."
    )

    messages: list[dict] = [{"role": "system", "content": system_with_context}]
    for turn in history[-6:]:
        messages.append(turn)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=settings.NVIDIA_MODEL,
        messages=messages,
        max_tokens=220,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
