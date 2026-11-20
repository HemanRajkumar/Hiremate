<<<<<<< HEAD
"""Typed structures for resume information extracted from source documents."""
from dataclasses import dataclass, field
from typing import Dict, List

=======
from dataclasses import dataclass, field
from typing import Dict, List
from services.metadata_service import (
    MetadataService,
)
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

@dataclass
class PersonalInfo:
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""


@dataclass
class Education:
    degree: str = ""
    institution: str = ""
<<<<<<< HEAD
    location: str = ""
    start_year: str = ""
    end_year: str = ""
    date_range: str = ""
=======
    start_year: str = ""
    end_year: str = ""
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
    cgpa: str = ""


@dataclass
class Experience:
    company: str = ""
    role: str = ""
<<<<<<< HEAD
    location: str = ""
    duration: str = ""
    date_range: str = ""
    description: str = ""
    bullets: List[str] = field(default_factory=list)
=======
    duration: str = ""
    description: str = ""
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029


@dataclass
class Project:
    title: str = ""
<<<<<<< HEAD
    date: str = ""
    location: str = ""
    description: str = ""
    bullets: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    github_url: str = ""


@dataclass
class Certification:
    title: str = ""
    issuer: str = ""
    date: str = ""
    details: str = ""


@dataclass
class Achievement:
    title: str = ""
    issuer: str = ""
    date: str = ""
    details: str = ""


@dataclass
class Training:
    title: str = ""
    provider: str = ""
    date: str = ""
    bullets: List[str] = field(default_factory=list)
=======
    description: str = ""
    technologies: List[str] = field(default_factory=list)
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029


@dataclass
class ResumeData:
<<<<<<< HEAD
    personal_info: PersonalInfo = field(default_factory=PersonalInfo)
    education: List[Education] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    programming_languages: List[str] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    training: List[Training] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    sections: Dict[str, str] = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
=======
    """
    Structured representation of a parsed resume.
    """

    personal_info: PersonalInfo = field(default_factory=PersonalInfo)

    education: List[Education] = field(default_factory=list)

    experience: List[Experience] = field(default_factory=list)

    projects: List[Project] = field(default_factory=list)

    skills: List[str] = field(default_factory=list)

    certifications: List[str] = field(default_factory=list)

    achievements: List[str] = field(default_factory=list)

    languages: List[str] = field(default_factory=list)

    # ⭐ New
    # Stores the raw text of each detected resume section.
    sections: Dict[str, str] = field(default_factory=dict)
    metadata: dict = field(
    default_factory=dict
)
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
