# HireMate — Connected Frontend and Backend

The repository now contains a working React frontend and FastAPI backend integration around the existing Python services.

```text
Browser
  │
  ▼
React + TypeScript (frontend, port 5173 in dev / 8080 in Docker)
  │  HTTP JSON / multipart requests under /api
  ▼
FastAPI (backend, port 8000)
  │
  ├── Existing services/resume_service.py
  ├── Existing services/jd_service.py
  ├── Existing services/ats_service.py
  ├── Existing services/skill_gap_service.py
  └── Existing services/analysis_service.py (full AI pipeline)
       │
       └── Groq API (server-side only; GROQ_API_KEY)
```

## Local development

Terminal 1, from repository root:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api` requests to FastAPI at port 8000.

## Docker

1. Copy `.env.example` to `.env` and set `GROQ_API_KEY` for AI-powered full analysis.
2. Run `docker compose up --build`.
3. Open http://localhost:8080. API docs are available at http://localhost:8000/docs.

## Connected API endpoints

- `GET /api/health`
- `POST /api/resumes/parse` (PDF upload)
- `POST /api/jobs/parse` (PDF/TXT upload or form text)
- `POST /api/analysis/preview` (deterministic ATS and skill-gap preview; no API key needed)
- `POST /api/analysis/full` (existing full analysis pipeline; requires `GROQ_API_KEY`)

## Important deployment notes

- Existing Python business logic stays in its original `services/`, `models/`, `ai/`, and `utils/` packages and is called by FastAPI. This avoids duplicating or prematurely moving proven logic.
- The frontend never receives the Groq API key.
- For a separate frontend host and backend host, set `VITE_API_URL` to the backend origin at frontend build time and set `CORS_ORIGINS` on the backend to the frontend origin.
- The current React screen is a functional integration harness only. It is not the final visual redesign.
