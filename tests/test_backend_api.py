"""Smoke tests for the FastAPI integration layer."""
import fitz
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def make_pdf(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_resume_pdf_parse_endpoint():
    response = client.post(
        "/api/resumes/parse",
        files={"file": ("resume.pdf", make_pdf("Taylor Example\nPython developer\nSkills: Python, SQL, Docker"), "application/pdf")},
    )
    assert response.status_code == 200
    assert "Python" in response.json()["extracted_text"]
    assert "resume" in response.json()


def test_analysis_preview_endpoint():
    response = client.post(
        "/api/analysis/preview",
        json={
            "resume_text": "Python developer with Python, SQL, Docker and Git experience building APIs.",
            "job_description": "Python Developer\nRequired skills: Python, SQL, Docker, AWS, React.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "overall_score" in payload["ats"]
    assert "missing_skills" in payload["ats"]


def test_health_reports_ai_configuration(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ai_configured"] is False


def test_full_analysis_requires_real_groq_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "your_groq_api_key_here")
    response = client.post(
        "/api/analysis/full",
        json={
            "resume_text": "Python developer with several years of experience building applications.",
            "job_description": "Python developer role requiring Python, SQL and API development.",
        },
    )
    assert response.status_code == 503
    assert "GROQ_API_KEY" in response.json()["detail"]
