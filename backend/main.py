"""FastAPI entry point for HireMate's independently deployable backend."""
from __future__ import annotations

import os
import logging
from dataclasses import asdict, is_dataclass
from typing import Any

import fitz
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.resume_service import ResumeService
from services.jd_service import JDService
from services.ats_service import ATSService
from services.skill_gap_service import SkillGapService

load_dotenv()

APP_VERSION = "1.0.0"
logger = logging.getLogger("hiremate.api")

app = FastAPI(
    title="HireMate API",
    version=APP_VERSION,
    description="HTTP API for HireMate resume intelligence features.",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisTextRequest(BaseModel):
    resume_text: str = Field(min_length=20, max_length=100_000)
    job_description: str = Field(min_length=10, max_length=100_000)


def to_jsonable(value: Any) -> Any:
    """Convert HireMate dataclasses and nested values to JSON-safe objects."""
    if is_dataclass(value):
        return to_jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def extract_text(filename: str, content: bytes) -> str:
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if suffix == "txt":
        try:
            return content.decode("utf-8-sig").strip()
        except UnicodeDecodeError as exc:
            raise HTTPException(400, "The text file must be UTF-8 encoded.") from exc
    if suffix == "pdf":
        try:
            with fitz.open(stream=content, filetype="pdf") as document:
                return "\n".join(page.get_text() for page in document).strip()
        except Exception as exc:
            raise HTTPException(400, "Could not read this PDF file.") from exc
    raise HTTPException(415, "Only PDF and TXT files are supported.")


@app.get("/")
def root():
    return {
        "name": "HireMate API",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
def health():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    ai_configured = bool(api_key and api_key != "your_groq_api_key_here")
    return {
        "status": "ok",
        "service": "hiremate-api",
        "version": APP_VERSION,
        "ai_configured": ai_configured,
    }


@app.post("/api/resumes/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(415, "Resume upload must be a PDF.")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(413, "Resume file must be 10 MB or smaller.")
    resume_text = extract_text(file.filename, content)
    if not resume_text:
        raise HTTPException(422, "No readable text was found in the resume PDF.")
    parsed = ResumeService().parse(resume_text)
    return {
        "filename": file.filename,
        "text_length": len(resume_text),
        "extracted_text": resume_text,
        "resume": to_jsonable(parsed),
    }


@app.post("/api/jobs/parse")
async def parse_job_description(
    file: UploadFile | None = File(default=None),
    job_description: str = Form(default=""),
):
    if file is not None:
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(413, "Job description file must be 10 MB or smaller.")
        text = extract_text(file.filename or "", content)
    else:
        text = job_description.strip()
    if len(text) < 10:
        raise HTTPException(422, "Provide a job description of at least 10 characters.")
    parsed = JDService().parse(text)
    return {"job_description": to_jsonable(parsed)}


@app.post("/api/analysis/preview")
def analysis_preview(payload: AnalysisTextRequest):
    """Run the deterministic resume/JD/ATS/skill-gap pipeline (no AI key needed)."""
    resume = ResumeService().parse(payload.resume_text)
    job = JDService().parse(payload.job_description)
    ats = ATSService().analyze(resume, job.skills)
    skill_gap = SkillGapService().analyze(ats)
    return {
        "resume": to_jsonable(resume),
        "job": to_jsonable(job),
        "ats": to_jsonable(ats),
        "skill_gap": to_jsonable(skill_gap),
    }


@app.post("/api/analysis/rewrite")
def generate_resume_rewrite(payload: AnalysisTextRequest):
    """Generate only the optimized resume section without rerunning the full report."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_api_key_here":
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured on the backend. Add it to the backend environment to generate an optimized resume.",
        )
    try:
        from services.rewrite_service import RewriteService

        rewrite = RewriteService().generate(payload.resume_text, payload.job_description)
        if (rewrite.professional_summary or "").startswith("The AI rewrite is temporarily unavailable"):
            raise RuntimeError("The AI provider did not return a usable rewrite.")
        return {"rewrite": to_jsonable(rewrite)}
    except Exception as exc:
        logger.exception("HireMate resume rewrite failed")
        raise HTTPException(
            status_code=502,
            detail=(
                f"Resume rewrite failed ({type(exc).__name__}). Check the backend terminal, "
                "verify GROQ_API_KEY and Groq connectivity, then try again."
            ),
        ) from exc


@app.post("/api/analysis/full")
def full_analysis(payload: AnalysisTextRequest):
    """Run HireMate's existing full analysis orchestration, including Groq-powered features."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_api_key_here":
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured on the backend. Add it to the backend environment to use full AI analysis.",
        )
    try:
        from services.analysis_service import AnalysisService

        result = AnalysisService().analyze(
            payload.resume_text,
            payload.job_description,
        )
        keys = [
            "resume", "job", "ats", "skill_gap", "roadmap", "career",
            "hireability", "projects", "career_coach", "company_matches",
            "certifications", "personalization", "review", "recommendations",
            "interview", "cover_letter", "rewrite",
        ]
        if len(result) != len(keys):
            raise RuntimeError(
                f"Analysis pipeline returned {len(result)} sections; expected {len(keys)}."
            )
        return {key: to_jsonable(value) for key, value in zip(keys, result)}
    except Exception as exc:
        # Keep implementation details and credentials out of API responses,
        # but log the traceback so the real cause is visible to the developer.
        logger.exception("HireMate full AI analysis failed")
        raise HTTPException(
            status_code=502,
            detail=(
                f"Full AI report failed ({type(exc).__name__}). "
                "Check the backend terminal for details, verify GROQ_API_KEY, "
                "and try again with a readable resume and job description."
            ),
        ) from exc
