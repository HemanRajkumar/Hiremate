# HireMate React frontend

The user interface is a React + TypeScript + Vite application. It does not use Streamlit to render or serve the frontend. The existing Python/FastAPI backend remains the API and analysis layer.

## Run locally

Terminal 1 (backend, from the repository root):

```bash
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` requests to `http://127.0.0.1:8000`.

## Run with Docker

From the repository root:

```bash
docker compose up --build
```

Open `http://localhost:3000`. The frontend is built as static assets and served by Nginx; `/api` is proxied to FastAPI.

## Backend capabilities

- `GET /api/health` - backend status
- `POST /api/resumes/parse` - PDF resume extraction and parsing
- `POST /api/analysis/preview` - deterministic ATS and skill-gap analysis
- `POST /api/analysis/full` - full AI report (requires `GROQ_API_KEY`)

The dashboard can run a deterministic analysis without an AI key. AI rewrite, roadmap and extended career outputs require a configured `GROQ_API_KEY` in the backend environment.
