"""Parse project headings, dates, bullet descriptions and technology lists."""
import re
from models.resume_model import Project

MONTH_DATE = re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b", re.I)
BULLET_PREFIX = ("•", "-", "*", "▪", "●")


class ProjectParser:
    def parse(self, resume):
        projects = []
        current = None
        pending_bullet = False

        for raw in resume.sections.get("projects", "").splitlines():
            source = raw.strip()
            if not source:
                continue
            if source in BULLET_PREFIX:
                pending_bullet = True
                continue

            is_bullet = source.startswith(BULLET_PREFIX) or pending_bullet
            line = source.lstrip("•*-▪● ").strip()
            pending_bullet = False
            if not line:
                continue

            if line.lower().startswith("tech:"):
                if current:
                    current.technologies = [x.strip() for x in re.split(r",|/", line.split(":", 1)[1]) if x.strip()]
                continue

            date_match = MONTH_DATE.search(line)
            # PDF extraction may place the date on a separate line directly after its title.
            if date_match and len(line.split()) <= 3 and current and not is_bullet:
                current.date = date_match.group(0)
                continue

            is_heading = not is_bullet and ("github:" in line.lower() or bool(date_match))
            if current is None or is_heading:
                if current:
                    projects.append(current)
                date = date_match.group(0) if date_match else ""
                title = line.replace(date, "").strip(" |:-") if date else line
                title = re.sub(r"\s*\|\s*GitHub:?.*$", "", title, flags=re.I).strip()
                current = Project(title=title or "Untitled Project", date=date)
                continue

            if current:
                if is_bullet:
                    current.bullets.append(line)
                elif current.bullets:
                    current.bullets[-1] += " " + line
                else:
                    current.description = (current.description + " " + line).strip()

        if current:
            projects.append(current)

        for project in projects:
            project.bullets = [re.sub(r"(?<=\w)-\s+(?=[a-z])", "", re.sub(r"\s+", " ", b)).strip() for b in project.bullets if b.strip()]
            project.description = re.sub(r"\s+", " ", project.description).strip()
            if not project.description and project.bullets:
                project.description = project.bullets[0]
        resume.projects = projects
"""
Project Parser.
"""

from models.resume_model import Project


class ProjectParser:

    def parse(
        self,
        resume,
    ):

        section = resume.sections.get(
            "projects",
            "",
        )

        if not section:
            return

        for line in section.splitlines():

            line = line.strip()

            if not line:
                continue

            resume.projects.append(
                Project(
                    title=line,
                )
            )
