"""Regression tests for structured resume sections and metadata extraction."""
import unittest

from services.resume_service import ResumeService


SAMPLE_RESUME = """\
Alex Candidate
Email: alex@example.com
Phone: +91-9876543210
SKILLS
Languages:
C, C++, Python, Java
PROJECTS
Skill Gap Analyzer | GitHub:
Aug 2026
• Built an analyzer for career skills.
• Added a FastAPI backend.
• Integrated a generative AI model.
Tech: Python, FastAPI, HTML
EDUCATION
Lovely Professional University                         Phagwara, Punjab
Bachelor of Technology - Computer Science; CGPA: 8.1       Aug 2024 - Present
CERTIFICATES
Python with Libraries | Skillera | Certificate          Mar 2025
TRAINING
AI Engineer Launchpad | LPU | Certificate:              Jun 2026 – Jul 2026
• Learned LLM integration.
• Practiced prompt engineering.
ACHIEVEMENTS
• Participated in a student competition | Student Program | Certificate Nov 2025
"""


class StructuredResumeParserTests(unittest.TestCase):
    def test_sections_are_structured_and_not_mixed(self):
        resume = ResumeService().parse(SAMPLE_RESUME)
        self.assertEqual(len(resume.education), 1)
        self.assertEqual(resume.education[0].location, "Phagwara, Punjab")
        self.assertEqual(resume.education[0].date_range, "Aug 2024 - Present")
        self.assertEqual(len(resume.projects), 1)
        self.assertEqual(resume.projects[0].title, "Skill Gap Analyzer")
        self.assertEqual(resume.projects[0].date, "Aug 2026")
        self.assertEqual(len(resume.projects[0].bullets), 3)
        self.assertIn("C++", resume.skills)
        self.assertEqual(len(resume.certifications), 1)
        self.assertEqual(resume.certifications[0].date, "Mar 2025")
        self.assertEqual(len(resume.training), 1)
        self.assertEqual(len(resume.training[0].bullets), 2)
        self.assertEqual(len(resume.achievements), 1)
        self.assertEqual(resume.achievements[0].date, "Nov 2025")
        self.assertEqual(resume.personal_info.location, "")
        self.assertEqual(resume.languages, [])
        self.assertEqual(resume.experience, [])


if __name__ == "__main__":
    unittest.main()
