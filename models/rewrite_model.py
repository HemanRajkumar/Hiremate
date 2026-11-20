from dataclasses import dataclass, field
from typing import Any


@dataclass
class RewriteResult:
    """AI-rewritten resume content."""

    professional_summary: str = ""
    experience: str = ""
    projects: Any = field(default_factory=list)
    skills: Any = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    ats_improvement: str = ""
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
