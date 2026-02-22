# Student Support Specialist Agent (Computer Science Program)

This project is a starter AI agent that answers student questions about a Computer Science program.

It is designed to:
- Prioritize official program information from a local knowledge base.
- Avoid guessing when information is missing.
- Escalate students to the right office when needed.
- Cover common student support topics:
  - Admissions
  - Courses and curriculum
  - Fees and billing basics
  - Exams and grading process
  - Campus services and logistics

## 1) Setup

```bash
cd /Users/osora/Documents/Project\ Alyssa
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your API key:

```bash
cp .env.example .env
```

## 2) Customize Program Knowledge

Edit the files in:

- `knowledge/cs_program_handbook.md`
- `knowledge/admissions.md`
- `knowledge/courses.md`
- `knowledge/fees_exams.md`
- `knowledge/campus_information.md`

Replace placeholder information with your real program details:
- Degree requirements
- Course sequence
- GPA/probation policies
- Internship/capstone requirements
- Advising contacts
- Registration and graduation deadlines
- Admissions criteria and deadlines
- Tuition/fee and exam policy details
- Campus office locations and student services

## 3) Run (Terminal)

```bash
source .venv/bin/activate
python3 src/student_support_agent.py
```

Type questions in the terminal. Type `exit` to quit.

## 4) Run (Web Frontend)

```bash
source .venv/bin/activate
python3 src/web_app.py
```

Backend: Flask (`src/web_app.py`)

Open:

- http://127.0.0.1:8000

The web UI includes:
- Chat with Alyssa
- Quick prompt buttons
- Source section badges showing what knowledge sections were retrieved

## 5) Notes

- Default model: `gpt-4.1-mini`
- Configure model with `OPENAI_MODEL` in `.env`
- The agent uses lightweight retrieval across all `knowledge/*.md` files and includes source section hints in responses.
