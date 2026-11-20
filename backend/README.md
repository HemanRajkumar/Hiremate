# HireMate Backend

FastAPI exposes the existing HireMate Python services over HTTP.

## Run locally

From the repository root:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://localhost:8000/docs

## Endpoints

- `GET /api/health` — health check
- `POST /api/resumes/parse` — parse a PDF resume
- `POST /api/jobs/parse` — parse a PDF/TXT upload or text field
- `POST /api/analysis/preview` — deterministic ATS and skill-gap preview; no Groq key required
- `POST /api/analysis/full` — full existing analysis pipeline, including Groq-powered features

Set `GROQ_API_KEY` in the backend environment for full AI analysis. Never put this key in frontend variables.
