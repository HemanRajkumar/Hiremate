"""
Certification Recommendation Service.
"""

from models.certification_model import (
    CertificationRecommendation,
)

from data.certification_library import (
    CERTIFICATION_LIBRARY,
)


class CertificationService:
    """
    Recommend certifications based on
    the candidate's missing skills.
    """

    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        ats_result,
    ) -> list[CertificationRecommendation]:
        """
        Generate certification recommendations.
        """

        recommendations = []

        candidate_missing_skills = {

            skill.lower()

            for skill in ats_result.missing_skills

        }

        # ==================================================
        # Certification Matching
        # ==================================================

        for skill, cert in CERTIFICATION_LIBRARY.items():

            if skill not in candidate_missing_skills:

                continue

            recommendations.append(

                CertificationRecommendation(

                    name=cert["name"],

                    provider=cert["provider"],

                    description=cert["description"],

                    difficulty=cert["difficulty"],

                    estimated_duration=cert["duration"],

                    expected_score_gain=cert["gain"],

                    target_companies=cert["companies"],

                    skills_covered=[skill],

                    priority="High",

                )

            )

        if not recommendations:
            domain = " ".join(ats_result.candidate_skills).lower()
            fallback = [
                ("IBM Data Science Professional Certificate", "IBM", "Practical data analysis, Python, SQL, and machine learning foundations.", ["Python", "SQL", "Pandas"]),
                ("DeepLearning.AI Machine Learning Specialization", "DeepLearning.AI", "Build foundations in supervised learning, model evaluation, and machine learning practice.", ["Python", "Machine Learning", "Scikit-learn"]),
            ]
            if any(term in domain for term in ["pandas", "numpy", "matplotlib", "scikit-learn"]):
                recommendations = [CertificationRecommendation(name=name, provider=provider, description=description, difficulty="Intermediate", estimated_duration="2-4 months", expected_score_gain=8, target_companies=(["IBM", "Accenture", "Infosys", "TCS"] if provider == "IBM" else ["Google", "Microsoft", "Amazon", "Adobe"]), skills_covered=skills, priority="Medium") for name, provider, description, skills in fallback]
        return recommendations