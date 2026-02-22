# Project Alyssa - Run Guide

This guide explains how to run Alyssa locally.

## 1) Prerequisites
- Python 3.9+
- An OpenAI API key

## 2) Setup
```bash
cd /Users/osora/Documents/Project\ Alyssa
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Environment Variables
Create `.env` from template:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `OPENAI_API_KEY=...`
- Optional: `OPENAI_MODEL=gpt-4.1-mini`
- Optional: `MAX_CONTEXT_CHUNKS=4`

## 4) Run in Terminal
```bash
source .venv/bin/activate
python3 src/student_support_agent.py
```

## 5) Run Web App (Flask backend)
```bash
source .venv/bin/activate
python3 src/web_app.py
```

Open:
- http://127.0.0.1:8000

## 6) Update Knowledge Base
Edit files in `/Users/osora/Documents/Project Alyssa/knowledge`:
- `admissions.md`
- `courses.md`
- `fees_exams.md`
- `campus_information.md`
- `cs_program_handbook.md`
