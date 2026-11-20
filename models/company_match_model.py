from dataclasses import dataclass, field


@dataclass
class CompanyMatch:
<<<<<<< HEAD
    company: str = ""
    overall_match: int = 0
    skill_match: int = 0
    ats_match: int = 0
    hireability_match: int = 0
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    required_skills: list[str] = field(default_factory=list)
    recommendation: str = ""
    recommendation_details: str = ""
=======

    company: str = ""

    overall_match: int = 0

    skill_match: int = 0

    ats_match: int = 0

    hireability_match: int = 0

    missing_skills: list[str] = field(
        default_factory=list
    )

    recommendation: str = ""
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
