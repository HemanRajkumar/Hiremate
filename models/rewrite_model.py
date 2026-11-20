from dataclasses import dataclass, field
<<<<<<< HEAD
from typing import Any
=======
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029


@dataclass
class RewriteResult:
<<<<<<< HEAD
    """AI-rewritten resume content."""

    professional_summary: str = ""
    experience: str = ""
    projects: Any = field(default_factory=list)
    skills: Any = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    ats_improvement: str = ""
=======
    """
    AI rewritten resume.
    """

    professional_summary: str = ""

    experience: str = ""

    projects: str = ""

    skills: str = ""

    suggestions: list[str] = field(
        default_factory=list,
    )

    ats_improvement: str = ""
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
