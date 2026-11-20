import re

from models.job_model import JobData
from services.skill_service import SkillService


class JDService:
    ROLE_SKILL_PROFILES = {
        "data science": ["Python", "SQL", "Pandas", "NumPy", "Statistics", "Scikit-learn", "Matplotlib", "Data Visualization", "Machine Learning"],
        "data scientist": ["Python", "SQL", "Pandas", "NumPy", "Statistics", "Scikit-learn", "Matplotlib", "Data Visualization", "Machine Learning"],
        "machine learning": ["Python", "Machine Learning", "Scikit-learn", "TensorFlow", "Statistics", "NumPy", "Pandas", "SQL", "Model Deployment"],
        "machine learning engineer": ["Python", "Machine Learning", "Scikit-learn", "TensorFlow", "Docker", "FastAPI", "SQL", "Model Deployment"],
        "web development": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git", "REST API"],
        "full stack developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git", "REST API"],
        "python developer": ["Python", "SQL", "Git", "FastAPI", "REST API", "Docker", "Testing"],
        "devops": ["Linux", "Git", "Docker", "Kubernetes", "AWS", "CI/CD", "Terraform"]
    }

    """
    Service responsible for extracting structured information
    from a Job Description (JD).
    """

    def __init__(self):
        self.skill_service = SkillService()

    # =====================================================
    # Job Title Extraction
    # =====================================================

    def extract_job_title(self, lines: list) -> str:
        """
        Extract job title using improved heuristics.
        Avoids noise like 'apply now', URLs, etc.
        """

        ignore_keywords = {
            "apply",
            "apply now",
            "email",
            "http",
            "www",
            "job description",
            "career",
        }

        for line in lines[:5]:

            cleaned = line.strip()
            lowered = cleaned.lower()

            if not cleaned:
                continue

            if any(word in lowered for word in ignore_keywords):
                continue

            if re.search(r"[@\d]", cleaned):
                continue

            return cleaned

        return ""

    # =====================================================
    # Experience Extraction
    # =====================================================

    def extract_experience(self, text: str) -> str:
        """
        Extract required experience (years).
        """

        pattern = r"(\d+\s*(?:\+|to|-)?\s*\d*\s*(?:years|year|yrs|yr))"

        match = re.search(pattern, text, re.IGNORECASE)

        return match.group() if match else ""

    # =====================================================
    # Skills Extraction
    # =====================================================

    def extract_skills(self, text: str):
        """
        Extract technical skills using SkillService.
        """

        return self.skill_service.extract_skills(text)

    # =====================================================
    # Main Parser
    # =====================================================

    def parse(self, text: str) -> JobData:
        """
        Parse Job Description into structured JobData.
        """

        job = JobData()

        # Normalize text
        clean_text = text.strip()
        lines = [line.strip() for line in clean_text.splitlines() if line.strip()]

        # -----------------------------
        # Job Title
        # -----------------------------
        job.job_info.title = self.extract_job_title(lines)

        # -----------------------------
        # Experience
        # -----------------------------
        job.requirements.experience = self.extract_experience(clean_text)

        # -----------------------------
        # Skills
        # -----------------------------
        job.skills = self.extract_skills(clean_text)
        if not job.skills and len(clean_text.split()) <= 8:
            role_key = clean_text.lower().strip(" .-")
            job.skills = list(self.ROLE_SKILL_PROFILES.get(role_key, []))

        # -----------------------------
        # Basic keyword extraction (light enhancement)
        # -----------------------------
        job.keywords = list(
            set(word.lower() for word in re.findall(r"[a-zA-Z]{3,}", clean_text))
        )[:50]

        return job
