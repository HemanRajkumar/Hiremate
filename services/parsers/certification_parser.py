"""Extract certificates with issuer and completion date when present."""
import re
from models.resume_model import Certification

DATE_RE = re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b", re.I)

class CertificationParser:
    def parse(self, resume):
        results = []
        for raw in resume.sections.get("certifications", "").splitlines():
            line = raw.strip().lstrip("•*-▪● ").strip()
            if not line:
                continue
            date_match = DATE_RE.search(line)
            date = date_match.group(0) if date_match else ""
            if date:
                line = line.replace(date, "").strip(" |:-")
            parts = [p.strip() for p in line.split("|") if p.strip()]
            title = parts[0] if parts else line
            issuer = parts[1] if len(parts) > 1 else ""
            results.append(Certification(title=title, issuer=issuer, date=date))
        resume.certifications = results
"""
Certification Parser.
"""


class CertificationParser:

    def parse(
        self,
        resume,
    ):

        section = resume.sections.get(
            "certifications",
            "",
        )

        if not section:
            return

        for line in section.splitlines():

            line = line.strip()

            if line:

                resume.certifications.append(
                    line,
                )
