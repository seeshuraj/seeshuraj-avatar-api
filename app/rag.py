"""
In-memory knowledge base for Seeshuraj Bhoopalan.
Keyword retrieval — no vector DB needed for this scale.
Sources: Resume (Apr 2026) + live GitHub repos.
"""

KNOWLEDGE_BASE = [
    {
        "id": "identity",
        "keywords": ["who", "name", "about", "yourself", "introduce", "tell me", "what do you do"],
        "text": (
            "I'm Seeshuraj Bhoopalan, an AI Engineer & Software Engineer based in Dublin, Ireland. "
            "I completed a PG Diploma in High-Performance Computing at Trinity College Dublin (2024–2026). "
            "I build LLM-powered tools, cloud systems, and full-stack products with a focus on "
            "performance, scale, and correctness. I'm actively looking for graduate AI/software engineering roles in Dublin and the EU."
        ),
    },
    {
        "id": "education",
        "keywords": ["education", "degree", "university", "college", "study", "diploma", "pg diploma", "masters", "msc", "trinity", "hpc", "btech"],
        "text": (
            "I hold a PG Diploma in High-Performance Computing from Trinity College Dublin (2024–2026), "
            "focusing on Parallel Computing, AI-powered Data Engineering, Cloud Resilience, and System Optimisation. "
            "Before that I completed a B.Tech in Information Technology from St. Joseph's College of Engineering, "
            "Anna University (2020–2024), graduating with an 8.63 CGPA. "
            "I also published a paper at ACM 2023 on multi-modal biometric authentication."
        ),
    },
    {
        "id": "skills",
        "keywords": ["skills", "technologies", "stack", "language", "framework", "tools", "tech", "know", "proficient"],
        "text": (
            "Core languages: Python (asyncio, type hints), C++, C, Java, JavaScript, Node.js, SQL, Bash, PHP, Dart. "
            "ML & LLMs: Neural networks, Transformers, TensorFlow, PyTorch, Hugging Face, LangChain, LangGraph, "
            "Ollama, Claude (Amazon Bedrock), OpenAI APIs, RAG pipelines, LLM fine-tuning, few-shot & chain-of-thought prompting, "
            "red-teaming, prompt injection, model serving APIs, quantisation/distillation. "
            "Cloud & DevOps: AWS (EC2, FSx, S3, VPC, CloudWatch, Bedrock), Azure (Data Factory, Azure AI), "
            "Docker, Kubernetes, OpenShift, Jenkins, Terraform, Ansible, CI/CD, MLOps, AIOps. "
            "Data & Observability: MongoDB, MySQL, PostgreSQL, SQLite3, Oracle, vector databases, "
            "Prometheus, Grafana, CloudWatch, distributed tracing. "
            "Web & APIs: FastAPI, Flask, Django, React, Next.js, Node.js, RESTful APIs. "
            "HPC & Systems: CUDA, OpenMP, MPI, parallel optimisations, Linux, Bash scripting."
        ),
    },
    {
        "id": "experience_cloud",
        "keywords": ["experience", "work", "job", "cloud", "beyond youth", "aws", "etl", "devops", "slo", "sli", "observability"],
        "text": (
            "As Cloud Engineer at Beyond Youth's Solution (Apr 2024 – Jun 2025), I designed scalable AWS "
            "infrastructures with defined SLOs and SLIs maintaining 99.9% uptime targets with error budget tracking. "
            "I automated ETL pipelines for multi-source integration, deployed CI/CD using Docker and Jenkins "
            "(cutting release cycles by 40%), and implemented an observability stack with CloudWatch metrics, "
            "logs, dashboards, and distributed tracing. I also authored postmortems and RCAs for production incidents."
        ),
    },
    {
        "id": "experience_fullstack",
        "keywords": ["freelance", "jjs", "fullstack", "react", "node", "frontend", "backend", "web", "seo"],
        "text": (
            "As Freelance Full Stack Developer at JJS Impex (Aug 2025 – Nov 2025), I built a React + Node.js "
            "product catalog with real-time validation (improving lead conversion by 40%), implemented SEO "
            "strategies that boosted organic visibility by 35%, and integrated Zoho Workforce for automated "
            "scheduling and attendance tracking. The live site is at jjsimpex.com."
        ),
    },
    {
        "id": "experience_lyft",
        "keywords": ["lyft", "flask", "api", "microservices", "intern", "internship", "backend", "transactions"],
        "text": (
            "During my Backend Developer internship at Lyft (Jan 2023 – Jun 2023), I engineered high-throughput "
            "Flask APIs handling 1M+ transactions/day, built microservices improving reliability by 30%, and "
            "optimised MongoDB and PostgreSQL queries reducing latency by 25%."
        ),
    },
    {
        "id": "experience_tranz",
        "keywords": ["tranz", "django", "ecommerce", "payment", "web developer", "intern"],
        "text": (
            "As Web Developer Intern at Tranz Mannequins Pvt. Ltd (Apr 2022 – Oct 2022), I developed a "
            "Django-based e-commerce platform that boosted sales by 50% and integrated payment gateways "
            "with improved real-time transaction flow."
        ),
    },
    {
        "id": "projects_github",
        "keywords": ["project", "built", "made", "developed", "showcase", "portfolio", "github", "repo", "code", "work", "show me"],
        "text": (
            "Here are my key projects, all available on GitHub:\n"
            "1) LLM Test Lab (github.com/seeshuraj/llm-test-lab) — TypeScript/Next.js platform to evaluate, score, "
            "and compare LLM outputs. Features A/B comparison, latency tracking, and drift detection for AI apps.\n"
            "2) Intelligent Data Center Selection (github.com/seeshuraj/Intelligent-Data-Center-Selection-Using-Real-Time-Metrics-and-KD-Tree-Optimization) — "
            "KD-Tree nearest-neighbour selection parallelised via MPI, achieving 6.3ms query time over 10,000+ nodes, 50% throughput improvement.\n"
            "3) MPI KD-Tree Data Center Selection (github.com/seeshuraj/mpi-kdtree-data-center-selection) — "
            "Benchmarks comparing distributed vs local performance in Python with MPI.\n"
            "4) CUDA GPU vs CPU Integration Benchmarks (github.com/seeshuraj/cuda_integral_GPU-CPU) — "
            "CUDA C++ performance benchmarks for numerical integration with parallel thread optimisation.\n"
            "5) Flow Manager System (github.com/seeshuraj/flow-manager-system) — "
            "Python backend for dynamic task & workflow management with REST API, Docker, and modular task scheduling.\n"
            "6) JJS Impex Website (github.com/seeshuraj/JJS_IMPEX) — "
            "Production website live at jjsimpex.com, built with HTML/CSS, SEO-optimised with sitemap & web manifest.\n"
            "7) ERCOT BESS Analyzer (github.com/seeshuraj/ercot-bess-analyzer) — "
            "Streamlit dashboard for ERCOT energy arbitrage and ancillary services revenue simulation.\n"
            "8) Seeshuraj Avatar API (github.com/seeshuraj/seeshuraj-avatar-api) — "
            "This AI avatar backend itself — FastAPI + NVIDIA NIM + Azure TTS, deployed on Render."
        ),
    },
    {
        "id": "projects_resume",
        "keywords": ["langgraph", "multi-agent", "chatbot", "llm chatbot", "biometric", "etl", "n8n", "automation", "visualisation", "bedrock"],
        "text": (
            "Additional projects from my resume:\n"
            "1) LangGraph Multi-Agent Chatbot — Stateful supervisor-agent architecture with Ollama local inference (Llama 3, Mistral) "
            "and Claude via Amazon Bedrock. Streaming FastAPI responses, LangGraph checkpointing, red-teaming & prompt injection testing.\n"
            "2) Multi-Agent LLM Automation & Data Visualisation — N8N pipeline curating job postings and generating customised resumes; "
            "Azure AI multi-agent system with LangChain tool-calling, self-correction, and interactive visualisations from Excel uploads.\n"
            "3) ETL Pipeline for Biometric Authentication — Facial, lip, and voice recognition with deep learning encoders, "
            "95% accuracy, low-latency inference APIs, React dashboard. Published at ACM 2023.\n"
            "4) LLM Chatbot for Data Insights — OpenAI + LangChain + MongoDB; structured/role-playing prompts, "
            "LLM fine-tuning, hallucination mitigation, React conversational UI. Won Smart India Hackathon 2023."
        ),
    },
    {
        "id": "certifications",
        "keywords": ["cert", "certification", "award", "hackathon", "achievement", "acm", "azure", "aws", "anthropic", "microsoft", "patent", "publication"],
        "text": (
            "Certifications (2026): Anthropic — Claude with Amazon Bedrock (RAG, tools, evals, extended thinking, prompt caching); "
            "Anthropic AI Fluency — 4D Framework; Microsoft Applied Skills: Create an AI Agent (Credential ID: A41534D6AD963F5A); "
            "Microsoft Azure AI Vision — Object Detection, Image Classification, Face Analysis, OCR; "
            "Microsoft: Plan & Prepare AI Solutions on Azure, Generative AI & Agents, Power BI. "
            "Earlier: AWS Cloud & DevOps, HPC CUDA/OpenMP, Full Stack Java (2023), MySQL, Ethical Hacking (2021–22). "
            "Awards: Smart India Hackathon Winner 2023 & Mentor 2025; IEEE Conocithon 2022 Winner; "
            "Coding Ninja 8th nationally 2022. "
            "Publication: ACM 2023 — ‘Multi-Modal Biometric Authentication with Dynamic Hosting’. "
            "Patent filed 2024: WEARCOMM — AI-Driven Multilingual Communication wearable. "
            "Guinness World Record Contributor (Global AI project); Speaker at AI & Cloud Symposium, SRM University."
        ),
    },
    {
        "id": "location_availability",
        "keywords": ["location", "dublin", "ireland", "visa", "available", "hire", "open", "remote", "relocate", "work", "job", "opportunity"],
        "text": (
            "I'm based in Dublin 18, Ireland on a Stamp 2 visa, open to sponsorship. "
            "Available immediately for graduate AI / software engineering roles. "
            "Open to Dublin, EU, UK, Qatar, Australia, and Canada. I respond to every email."
        ),
    },
    {
        "id": "contact",
        "keywords": ["contact", "email", "reach", "linkedin", "github", "hire", "connect", "phone"],
        "text": (
            "You can reach me at bhoopals@tcd.ie or call +353 089 493 1217. "
            "LinkedIn: linkedin.com/in/seeshuraj — GitHub: github.com/seeshuraj — Portfolio: seeshuraj.github.io. "
            "I respond to every message!"
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
