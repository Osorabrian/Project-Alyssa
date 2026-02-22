import os
import re
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv
from openai import OpenAI


SYSTEM_PROMPT = """You are Alyssa, a Student Support Specialist for the Jessup University Computer Science program.

Your job:
1) Answer student questions accurately using the provided program context.
2) Keep answers clear, practical, and student-friendly.
3) If policy details are missing or uncertain, say what is unknown and direct the student to the correct office/contact.

Coverage scope:
- Admissions
- Courses and degree planning
- Fees and payment-related academic policies
- Exams and assessment policies
- Campus and student services information

Rules:
- Do not invent program requirements, deadlines, or policy details.
- Prefer concise bullet points for procedural answers.
- If a question is outside CS program support scope (e.g., legal/medical/personal crisis), provide a brief referral to the appropriate campus office.
- End each answer with:
  Source sections: <list of section headings used>
"""


def load_settings() -> Tuple[str, str, int]:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing OPENAI_API_KEY in environment/.env")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    max_chunks = int(os.getenv("MAX_CONTEXT_CHUNKS", "4"))
    return api_key, model, max_chunks


def read_knowledge_files(knowledge_dir: Path) -> List[Tuple[str, str]]:
    if not knowledge_dir.exists():
        raise FileNotFoundError(f"Knowledge directory not found: {knowledge_dir}")

    files = sorted(knowledge_dir.glob("*.md"))
    if not files:
        raise FileNotFoundError(f"No markdown knowledge files found in: {knowledge_dir}")

    docs: List[Tuple[str, str]] = []
    for file_path in files:
        docs.append((file_path.name, file_path.read_text(encoding="utf-8")))
    return docs


def split_into_sections(markdown_text: str, file_name: str) -> List[Tuple[str, str]]:
    sections: List[Tuple[str, str]] = []
    current_heading = f"{file_name} > General"
    current_lines: List[str] = []

    for line in markdown_text.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines).strip()))
                current_lines = []
            current_heading = f"{file_name} > {line[3:].strip()}"
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines).strip()))

    return [(h, c) for h, c in sections if c]


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def rank_sections(query: str, sections: List[Tuple[str, str]], max_chunks: int) -> List[Tuple[str, str]]:
    query_tokens = set(tokenize(query))
    scored: List[Tuple[int, str, str]] = []

    for heading, content in sections:
        section_tokens = set(tokenize(f"{heading}\n{content}"))
        overlap = len(query_tokens.intersection(section_tokens))
        scored.append((overlap, heading, content))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = [(heading, content) for score, heading, content in scored if score > 0]
    return selected[:max_chunks]


def build_context(chunks: List[Tuple[str, str]]) -> str:
    if not chunks:
        return "No relevant program sections were found."
    blocks = []
    for heading, content in chunks:
        blocks.append(f"## {heading}\n{content}")
    return "\n\n".join(blocks)


def ask_agent(client: OpenAI, model: str, question: str, context: str) -> str:
    user_prompt = f"""Student question:
{question}

Program context:
{context}
"""
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.output_text.strip()


def parse_source_sections(answer: str) -> List[str]:
    marker = "Source sections:"
    for line in reversed(answer.splitlines()):
        if line.strip().lower().startswith(marker.lower()):
            raw = line.split(":", 1)[1].strip()
            if not raw:
                return []
            return [item.strip() for item in raw.split(",") if item.strip()]
    return []


class AlyssaAgent:
    def __init__(self) -> None:
        api_key, model, max_chunks = load_settings()
        self.model = model
        self.max_chunks = max_chunks
        self.client = OpenAI(api_key=api_key)
        knowledge_dir = Path(__file__).resolve().parents[1] / "knowledge"
        docs = read_knowledge_files(knowledge_dir)
        self.sections: List[Tuple[str, str]] = []
        for file_name, content in docs:
            self.sections.extend(split_into_sections(content, file_name=file_name))

    def answer(self, question: str) -> Tuple[str, List[str]]:
        top_sections = rank_sections(question, self.sections, max_chunks=self.max_chunks)
        context = build_context(top_sections)
        answer = ask_agent(self.client, self.model, question, context)
        return answer, [heading for heading, _ in top_sections]
