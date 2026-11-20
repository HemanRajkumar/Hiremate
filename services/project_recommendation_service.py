from models.project_recommendation_model import ProjectRecommendation


class ProjectRecommendationService:
    PROJECTS = {
        "data science": [
            ("End-to-end data analysis dashboard", "Clean a real dataset, explore trends, and publish an interactive dashboard.", ["Python", "Pandas", "SQL", "Matplotlib"], "Intermediate", "2-3 weeks"),
            ("Predictive machine learning application", "Train, evaluate, explain, and deploy a predictive model behind an API.", ["Python", "Scikit-learn", "Machine Learning", "FastAPI"], "Intermediate", "3-4 weeks"),
        ],
        "ai/ml": [
            ("Deploy a machine learning model", "Build a reproducible model pipeline and serve predictions through an API.", ["Python", "Scikit-learn", "FastAPI", "Docker"], "Advanced", "3-4 weeks"),
            ("Model evaluation and monitoring toolkit", "Compare models, track experiments, and monitor prediction quality.", ["Python", "Machine Learning", "Statistics"], "Advanced", "2-3 weeks"),
        ],
        "web development": [
            ("Full-stack portfolio application", "Build an accessible app with authentication, CRUD workflows, and deployment.", ["HTML", "CSS", "JavaScript", "React", "SQL"], "Intermediate", "3-4 weeks"),
            ("REST API with database", "Create a tested API with validation, authentication, and documentation.", ["Python", "FastAPI", "SQL", "Docker"], "Intermediate", "2-3 weeks"),
        ],
    }

    def generate(self, resume_data, ats_result) -> list[ProjectRecommendation]:
        domain = str(resume_data.metadata.get("primary_domain", "General")).lower()
        ideas = self.PROJECTS.get(domain, [
            ("Role-focused portfolio project", "Build and deploy a complete project that solves a practical problem and document your decisions.", list(ats_result.missing_skills[:4]) or list(ats_result.candidate_skills[:4]), "Intermediate", "2-3 weeks"),
            ("Practical skills demonstration", "Create a smaller project with tests, clear documentation, and a public demo.", list(ats_result.missing_skills[:3]) or list(ats_result.candidate_skills[:3]), "Beginner", "1-2 weeks"),
        ])
        return [ProjectRecommendation(title=title, description=description, technologies=skills, skills_covered=skills, difficulty=level, estimated_duration=duration, expected_score_gain=10 if i == 0 else 7, priority="High" if i == 0 else "Medium") for i, (title, description, skills, level, duration) in enumerate(ideas)]
"""
Project Recommendation Service.
"""

from models.project_recommendation_model import (
    ProjectRecommendation,
)


class ProjectRecommendationService:
    """
    Recommend projects based on
    resume and missing skills.
    """

    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        resume_data,
        ats_result,
    ) -> list[ProjectRecommendation]:

        projects = []

        return projects
