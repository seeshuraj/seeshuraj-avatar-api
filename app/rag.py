"""
In-memory knowledge base for Seeshuraj Bhoopalan.
Keyword retrieval — no vector DB needed for this scale.
"""

KNOWLEDGE_BASE = [
    {
        "id": "identity",
        "keywords": ["who", "name", "about", "yourself", "introduce", "tell me"],
        "text": (
            "I'm Seeshuraj Bhoopalan, an AI & Software Engineer based in Dublin, Ireland. "
            "I'm completing my MSc in High Performance Computing at Trinity College Dublin. "
            "I build LLM-powered tools, cloud systems, and full-stack products with a focus on "
            "performance, scale, and correctness."
        ),
    },
    {
        "id": "education",
        "keywords": ["education", "degree", "university", "college", "study", "msc", "masters", "trinity", "hpc"],
        "text": (
            "I hold a PG Diploma in High Performance Computing from Trinity College Dublin (2024–2026, 2:1). "
            "Before that I completed a B.Tech in Information Technology from St. Joseph's College of Engineering, "
            "Anna University (2020–2024, 8.63 GPA). I also published a paper at ACM 2023 on multi-modal biometric authentication."
        ),
    },
    {
        "id": "skills",
        "keywords": ["skills", "technologies", "stack", "language", "framework", "tools", "tech"],
        "text": (
            "My core languages are Python, TypeScript, C++, JavaScript, Java, SQL, and Bash. "
            "On the ML/LLM side: LangChain, LangGraph, Ollama, RAG pipelines, PyTorch, Hugging Face, OpenAI API, Amazon Bedrock. "
            "Cloud & DevOps: AWS, Azure, Docker, Kubernetes, Jenkins, Terraform, CI/CD, CloudWatch. "
            "Web & Data: FastAPI, React, Next.js, Node.js, PostgreSQL, MongoDB, Supabase. "
            "HPC & Systems: CUDA, OpenMP, MPI, Prometheus, Grafana, Linux."
        ),
    },
    {
        "id": "experience_cloud",
        "keywords": ["experience", "work", "job", "cloud", "beyond youth", "aws", "etl", "devops"],
        "text": (
            "As Cloud Engineer at Beyond Youth's Solution (Apr 2024 – Jun 2025), I designed scalable AWS "
            "infrastructures with 99.9% uptime SLOs, automated ETL pipelines, deployed CI/CD using Docker and "
            "Jenkins (cutting release cycles by 40%), and implemented observability with CloudWatch and distributed tracing."
        ),
    },
    {
        "id": "experience_fullstack",
        "keywords": ["freelance", "jjs", "fullstack", "react", "node", "frontend", "backend", "web"],
        "text": (
            "As Freelance Full Stack Developer at JJS Impex (Aug 2025 – Nov 2025), I built a React + Node.js "
            "product catalog with real-time validation, improving lead conversion by 40%, and boosted organic "
            "SEO visibility by 35%."
        ),
    },
    {
        "id": "experience_lyft",
        "keywords": ["lyft", "flask", "api", "microservices", "intern", "internship", "backend"],
        "text": (
            "During my Backend Developer internship at Lyft (Jan 2023 – Jun 2023), I engineered high-throughput "
            "Flask APIs handling 1M+ transactions/day, built microservices improving reliability by 30%, and "
            "optimised MongoDB and PostgreSQL queries reducing latency by 25%."
        ),
    },
    {
        "id": "projects",
        "keywords": ["project", "built", "made", "developed", "showcase", "portfolio", "work"],
        "text": (
            "Key projects: "
            "1) LangGraph Multi-Agent Chatbot — stateful multi-agent system with supervisor routing, Ollama local LLM, Claude via Bedrock, streaming FastAPI responses. "
            "2) Multi-Agent LLM Automation — N8N pipeline + Azure AI agents for automated job curation and resume generation. "
            "3) ETL Pipeline for Biometric Auth — facial/lip/voice recognition, 95% accuracy, ACM 2023 published. "
            "4) Intelligent Data Centre Selection — MPI parallelised KD-Tree, 6.3ms query time over 10,000 nodes. "
            "5) LLM Chatbot for Data Insights — OpenAI + LangChain + MongoDB, Smart India Hackathon winner 2023. "
            "6) LLM Test Lab — FastAPI + Next.js evaluation platform for AI model comparison and regression tracking."
        ),
    },
    {
        "id": "certifications",
        "keywords": ["cert", "certification", "award", "hackathon", "achievement", "acm", "azure", "aws"],
        "text": (
            "Certifications: Anthropic Claude with Amazon Bedrock (2026), Microsoft Applied Skills: Create an AI Agent (Feb 2026), "
            "Anthropic AI Fluency (2026), Azure AI Vision & Generative AI (2025–2026), AWS Cloud & DevOps, NVIDIA CUDA HPC (2023). "
            "Awards: Smart India Hackathon Winner 2023 & Mentor 2025, IEEE Conocithon 2022 Winner, Coding Ninja 8th nationally 2022."
        ),
    },
    {
        "id": "location_availability",
        "keywords": ["location", "dublin", "ireland", "visa", "available", "hire", "open", "remote", "relocate"],
        "text": (
            "I'm based in Dublin 18, Ireland on a Stamp 2 visa, open to sponsorship. "
            "Available immediately for graduate AI / software engineering roles in Dublin, EU, and remote. "
            "I'm also open to opportunities in the UK, Qatar, Australia, and Canada."
        ),
    },
    {
        "id": "contact",
        "keywords": ["contact", "email", "reach", "linkedin", "github", "hire"],
        "text": (
            "You can reach me at bhoopals@tcd.ie, on LinkedIn at linkedin.com/in/seeshuraj, "
            "or on GitHub at github.com/seeshuraj. I respond to every email."
        ),
    },
]


def retrieve(query: str, top_k: int = 3) -> str:
    """Return the top_k most relevant knowledge snippets for a query."""
    q = query.lower()
    scored: list[tuple[int, str]] = []
    for entry in KNOWLEDGE_BASE:
        score = sum(1 for kw in entry["keywords"] if kw in q)
        scored.append((score, entry["text"]))
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [text for score, text in scored[:top_k] if score > 0]
    if not results:
        # fallback: return identity + skills
        results = [KNOWLEDGE_BASE[0]["text"], KNOWLEDGE_BASE[2]["text"]]
    return "\n\n".join(results)
