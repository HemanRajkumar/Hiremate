<<<<<<< HEAD
"""Parse work and internship entries into structured records."""
import re
from models.resume_model import Experience

DATE_RE = re.compile(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\s*[-–—]\s*(?:Present|Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}))", re.I)

class ExperienceParser:
    def parse(self, resume):
        entries = []
        current = None
        for raw in resume.sections.get("experience", "").splitlines():
            line = raw.strip().lstrip("•*-▪● ").strip()
            if not line:
                continue
            date = DATE_RE.search(line)
            if current is None or (date and not raw.strip().startswith(("•", "-", "*", "▪"))):
                if current:
                    entries.append(current)
                heading = DATE_RE.sub("", line).strip(" |:-")
                parts = [x.strip() for x in heading.split("|") if x.strip()]
                current = Experience(role=parts[0] if parts else heading, company=parts[1] if len(parts) > 1 else "")
                if date:
                    current.duration = date.group(1)
                    current.date_range = date.group(1)
            elif current:
                current.bullets.append(line)
                current.description = " ".join(current.bullets)
        if current:
            entries.append(current)
        resume.experience = entries
=======
"""
Experience Parser.
"""

from models.resume_model import Experience


class ExperienceParser:

    def parse(
        self,
        resume,
    ):

        section = resume.sections.get(
            "experience",
            "",
        )

        if not section:
            return

        for line in section.splitlines():

            line = line.strip()

            if not line:
                continue

            resume.experience.append(
                Experience(
                    company=line,
                )
            )
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
