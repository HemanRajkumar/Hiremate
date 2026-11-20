"""Split resume text into named sections without treating content as headings."""
import re
from services.parsers.base_parser import BaseParser


class SectionParser(BaseParser):
    SECTION_HEADERS = {
        "summary": {"summary", "professional summary", "objective", "profile", "about"},
        "skills": {"skills", "technical skills", "core skills"},
        "education": {"education", "academic background", "qualification", "qualifications"},
        "experience": {"experience", "work experience", "employment", "internship", "internships"},
        "projects": {"projects", "academic projects", "personal projects"},
        "certifications": {"certifications", "certificates", "licenses"},
        "training": {"training", "courses", "professional training"},
        "achievements": {"achievements", "awards", "accomplishments", "co curricular activities", "co curricular activites", "extracurricular activities"},
        "languages": {"languages", "spoken languages"},
    }

    @staticmethod
    def _normalize(line):
        return re.sub(r"\s+", " ", re.sub(r"[^a-z]+", " ", line.lower())).strip()

    def parse(self, text, resume):
        resume.sections = {"general": ""}
        current = "general"
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            normalized = self._normalize(line.rstrip(":"))
            # "Languages:" is a skill-category label in many resumes, not a section.
            found = None if current == "skills" and normalized == "languages" else next(
                (name for name, aliases in self.SECTION_HEADERS.items() if normalized in aliases), None
            )
            if found:
                current = found
                resume.sections.setdefault(current, "")
                continue
            resume.sections[current] = resume.sections.get(current, "") + line + "\n"
