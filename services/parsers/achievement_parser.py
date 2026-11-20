"""Parse co-curricular achievements with their organizer and date."""
import re
from models.resume_model import Achievement

DATE_RE = re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b", re.I)

class AchievementParser:
    def parse(self, resume):
        results = []
        for raw in resume.sections.get("achievements", "").splitlines():
            line = raw.strip().lstrip("•*-▪● ").strip()
            if not line:
                continue
            date_match = DATE_RE.search(line)
            date = date_match.group(0) if date_match else ""
            if date:
                line = line.replace(date, "").strip(" |:-")
            parts = [x.strip() for x in line.split("|") if x.strip()]
            title = parts[0] if parts else line
            issuer = parts[1] if len(parts) > 1 else ""
            details = parts[2] if len(parts) > 2 else ""
            results.append(Achievement(title=title, issuer=issuer, date=date, details=details))
        resume.achievements = results
"""
Achievement Parser.
"""


class AchievementParser:

    def parse(
        self,
        resume,
    ):

        section = resume.sections.get(
            "achievements",
            "",
        )

        if not section:
            return

        for line in section.splitlines():

            line = line.strip()

            if line:

                resume.achievements.append(
                    line,
                )
