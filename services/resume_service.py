<<<<<<< HEAD
"""Coordinate resume section extraction and typed parsing."""
from models.resume_model import ResumeData
from services.skill_service import SkillService
from services.metadata_service import MetadataService
from services.parsers.personal_parser import PersonalParser
from services.parsers.section_parser import SectionParser
from services.parsers.education_parser import EducationParser
from services.parsers.experience_parser import ExperienceParser
from services.parsers.project_parser import ProjectParser
from services.parsers.certification_parser import CertificationParser
from services.parsers.training_parser import TrainingParser
from services.parsers.language_parser import LanguageParser
from services.parsers.achievement_parser import AchievementParser


class ResumeService:
    def __init__(self):
        self.personal_parser = PersonalParser()
        self.section_parser = SectionParser()
        self.education_parser = EducationParser()
        self.experience_parser = ExperienceParser()
        self.project_parser = ProjectParser()
        self.certification_parser = CertificationParser()
        self.training_parser = TrainingParser()
        self.language_parser = LanguageParser()
        self.achievement_parser = AchievementParser()
        self.skill_service = SkillService()
        self.metadata_service = MetadataService()

    def parse(self, text: str) -> ResumeData:
        resume = ResumeData()
        self.personal_parser.parse(text, resume)
        self.section_parser.parse(text, resume)
        self.education_parser.parse(resume)
        self.experience_parser.parse(resume)
        self.project_parser.parse(resume)
        self.certification_parser.parse(resume)
        self.training_parser.parse(resume)
        self.language_parser.parse(resume)
        self.achievement_parser.parse(resume)
        resume.skills = self.skill_service.extract_skills(text)
        resume.metadata = self.metadata_service.generate(resume)
        return resume
=======
"""
Resume Service.

Coordinates all resume parsers and returns a structured ResumeData object.
"""

from models.resume_model import ResumeData

from services.skill_service import SkillService
from services.metadata_service import MetadataService

from services.parsers.personal_parser import (
    PersonalParser,
)

from services.parsers.section_parser import (
    SectionParser,
)

from services.parsers.education_parser import (
    EducationParser,
)

from services.parsers.experience_parser import (
    ExperienceParser,
)

from services.parsers.project_parser import (
    ProjectParser,
)

from services.parsers.certification_parser import (
    CertificationParser,
)

from services.parsers.language_parser import (
    LanguageParser,
)

from services.parsers.achievement_parser import (
    AchievementParser,
)


class ResumeService:
    """
    Main resume parsing service.

    This class orchestrates all specialized parsers.
    """

    def __init__(self):

        self.personal_parser = PersonalParser()

        self.section_parser = SectionParser()

        self.education_parser = EducationParser()

        self.experience_parser = ExperienceParser()

        self.project_parser = ProjectParser()

        self.certification_parser = CertificationParser()

        self.language_parser = LanguageParser()

        self.achievement_parser = AchievementParser()

        self.skill_service = SkillService()

        self.metadata_service = MetadataService()

    # =====================================================
    # Main Parser
    # =====================================================

    def parse(
        self,
        text: str,
    ) -> ResumeData:
        """
        Parse resume text into structured ResumeData.
        """

        resume = ResumeData()

        # ------------------------------------------
        # Personal Information
        # ------------------------------------------

        self.personal_parser.parse(
            text,
            resume,
        )

        # ------------------------------------------
        # Resume Sections
        # ------------------------------------------

        self.section_parser.parse(
            text,
            resume,
        )

        # ------------------------------------------
        # Structured Parsers
        # ------------------------------------------

        self.education_parser.parse(
            resume,
        )

        self.experience_parser.parse(
            resume,
        )

        self.project_parser.parse(
            resume,
        )

        self.certification_parser.parse(
            resume,
        )

        self.language_parser.parse(
            resume,
        )

        self.achievement_parser.parse(
            resume,
        )

        # ------------------------------------------
        # Skills
        # ------------------------------------------

        resume.skills = self.skill_service.extract_skills(
            text,
        )

        # ------------------------------------------
        # Metadata
        # ------------------------------------------

        resume.metadata = self.metadata_service.generate(
            resume,
        )

        return resume
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
