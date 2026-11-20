"""Group institution, location, degree, grade and date lines into education records."""
import re
from models.resume_model import Education

DATE_RE = re.compile(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\s*[-–—]\s*(?:Present|Current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}))", re.I)

class EducationParser:
    def parse(self, resume):
        lines = [x.strip() for x in resume.sections.get("education", "").splitlines() if x.strip()]
        records = []
        current = None
        for line in lines:
            line = line.lstrip("•*-▪● ").strip()
            # Institution lines commonly contain a location after a wide PDF column gap.
            parts = re.split(r"\s{2,}|\t+", line, maxsplit=1)
            if current is None or (not re.search(r"(?:CGPA|GPA|Percentage|%|\b(?:B\.?Tech|Bachelor|Master|Intermediate|Matriculation|Diploma)\b)", line, re.I) and len(parts) == 2 and "," in parts[-1]):
                if current:
                    records.append(current)
                institution = parts[0].strip()
                location = parts[1].strip() if len(parts) > 1 else ""
                current = Education(institution=institution, location=location)
                continue
            if current:
                date = DATE_RE.search(line)
                if date:
                    current.date_range = date.group(1).strip()
                    dates = re.split(r"\s*[-–—]\s*", current.date_range, maxsplit=1)
                    current.start_year = dates[0]
                    current.end_year = dates[-1] if len(dates) > 1 else ""
                    line = DATE_RE.sub("", line).strip(" -–—")
                grade = re.search(r"(?:CGPA|GPA)\s*[:=]?\s*([\d.]+)|([\d.]+\s*%)", line, re.I)
                if grade:
                    current.cgpa = grade.group(0).strip()
                degree = re.sub(r";?\s*(?:CGPA|GPA|Percentage)\s*[:=]?.*$", "", line, flags=re.I).strip(" ;,")
                if degree:
                    current.degree = degree
        if current:
            records.append(current)
        resume.education = [r for r in records if r.institution or r.degree]
"""
Education Parser.
"""

from models.resume_model import Education


class EducationParser:

    def parse(
        self,
        resume,
    ):

        section = resume.sections.get(
            "education",
            "",
        )

        if not section:
            return

        for line in section.splitlines():

            line = line.strip()

            if not line:
                continue

            resume.education.append(
                Education(
                    degree=line,
                )
            )
