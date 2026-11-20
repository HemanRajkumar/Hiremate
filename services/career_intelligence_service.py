from models.career_intelligence_model import (
    CareerIntelligence,
)


class CareerIntelligenceService:
    """
    Generates a unified career intelligence report
    using resume analysis, ATS results, skill gaps,
    and the personalized learning roadmap.
    """

    def generate(
        self,
        resume_data,
        ats_result,
        skill_gap,
        roadmap,
    ) -> CareerIntelligence:

        career = CareerIntelligence()

        # ==================================================
        # Candidate Information
        # ==================================================

        career.current_role = "Student"

        career.target_role = resume_data.metadata.get(
            "primary_domain",
            "Software Engineer",
        )

        # ==================================================
        # Readiness Score
        # ==================================================

        score = int(
            ats_result.overall_score
        )

        career.readiness_score = score

        # ==================================================
        # Career Stage
        # ==================================================

        if score >= 90:

            career.stage = "💎 Industry Ready"

            career.confidence = "Very High"

        elif score >= 80:

            career.stage = "🏆 Competitive"

            career.confidence = "High"

        elif score >= 70:

            career.stage = "🚀 Job Ready"

            career.confidence = "Moderate"

        elif score >= 55:

            career.stage = "🌿 Emerging Developer"

            career.confidence = "Growing"

        else:

            career.stage = "🌱 Beginner"

            career.confidence = "Low"

        # ==================================================
        # Summary
        # ==================================================

        career.summary = (
            f"Your resume currently matches approximately "
            f"{score}% of the target job requirements."
        )

        # ==================================================
        # Learning Timeline
        # ==================================================

        career.estimated_duration = (
            f"{roadmap.duration_weeks} Weeks"
        )

        # ==================================================
        # Strengths
        # ==================================================

        career.strengths = (
            ats_result.strengths[:5]
            if ats_result.strengths
            else ["No major strengths identified yet."]
        )

        # ==================================================
        # Improvement Areas
        # ==================================================

        career.improvement_areas = [
<<<<<<< HEAD
            f"Strengthen {gap.skill} (high priority)"
            for gap in skill_gap.high_priority
        ] + [
            f"Develop {gap.skill} (medium priority)"
            for gap in skill_gap.medium_priority
        ] + [
            f"Consider learning {gap.skill}"
            for gap in skill_gap.low_priority
        ]
        if not career.improvement_areas:
            career.improvement_areas = [
                "Add a target job description to identify role-specific skill gaps.",
                "Add measurable results to your project descriptions.",
                "Include internship, freelance, or practical experience where applicable.",
            ]
=======
            gap.skill
            for gap in skill_gap.high_priority
        ]
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

        # ==================================================
        # Next Learning Steps
        # ==================================================

        career.next_steps = [
            task.title
            for task in roadmap.tasks[:5]
        ]
<<<<<<< HEAD
        if not career.next_steps:
            career.next_steps = [
                "Choose a target role and add its job description for an accurate skills comparison.",
                "Build one end-to-end project that demonstrates your strongest technical skills.",
                "Add project links, tools used, and measurable outcomes to your resume.",
                "Practice technical questions for your target role.",
            ]
=======
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

        # ==================================================
        # Recommended Projects
        # (Placeholder for v1.0.0)
        # ==================================================

<<<<<<< HEAD
        domain = str(resume_data.metadata.get("primary_domain", "General")).lower()
        project_ideas = {
            "data science": ["Build an end-to-end data analytics dashboard", "Create a predictive ML project with model evaluation"],
            "ai/ml": ["Build and deploy an ML model with an API", "Create an experiment-tracking and model-monitoring demo"],
            "web development": ["Build and deploy a full-stack portfolio application", "Create an authenticated CRUD app with a database"],
            "devops": ["Create a CI/CD pipeline with automated tests", "Containerize and deploy an application with monitoring"],
        }
        career.recommended_projects = project_ideas.get(domain, [
            "Build a portfolio project that solves a real-world problem",
            "Create an end-to-end application and document its architecture",
        ])
=======
        career.recommended_projects = []
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

        # ==================================================
        # Recommended Certifications
        # (Placeholder for v1.0.0)
        # ==================================================

<<<<<<< HEAD
        cert_ideas = {
            "data science": ["IBM Data Science Professional Certificate", "Microsoft Power BI Data Analyst Associate"],
            "ai/ml": ["AWS Certified Machine Learning – Specialty (check current exam availability)", "DeepLearning.AI Machine Learning Specialization"],
            "web development": ["Meta Front-End Developer Professional Certificate", "Meta Back-End Developer Professional Certificate"],
            "devops": ["AWS Certified Cloud Practitioner", "HashiCorp Certified: Terraform Associate"],
        }
        career.recommended_certifications = cert_ideas.get(domain, [
            "Choose a recognized certification aligned with your target role",
            "Complete a practical course that includes a portfolio project",
        ])
=======
        career.recommended_certifications = []
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

        return career