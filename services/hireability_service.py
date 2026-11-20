from models.hireability_model import (
    HireabilityScore,
)


class HireabilityService:
    """
    Calculates the overall Hireability Score.
    """

    def generate(
        self,
        ats_result,
        career,
    ) -> HireabilityScore:

        score = HireabilityScore()

        score.resume = int(
            ats_result.completeness_score
        )

        score.ats = int(
            ats_result.overall_score
        )

        score.technical = int(
            ats_result.skills_score
        )

        score.matched_skills = list(ats_result.matched_skills)
        score.missing_skills = list(ats_result.missing_skills)
        score.candidate_skills = list(ats_result.candidate_skills)
        score.required_skills = list(ats_result.required_skills)
        score.skill_match_percentage = (
            round(ats_result.skills_score) if score.required_skills else None
        )
        score.skill_match_status = (
            "Add a target job description to compare your skills"
            if not score.required_skills
            else f"{len(score.matched_skills)} of {len(score.required_skills)} required skills matched"
        )
        score.lacking = list(score.missing_skills)

        score.projects = int(
            ats_result.projects_score
        )

        score.career = int(
            career.readiness_score
        )

        # Placeholder until Interview Intelligence
        # becomes more sophisticated.

        score.interview = int(
            career.readiness_score * 0.9
        )

        values = [
            score.resume,
            score.ats,
            score.technical,
            score.projects,
            score.career,
            score.interview,
        ]

        score.overall = sum(values) // len(values)

# ==================================================
# Grade
# ==================================================

        if score.overall >= 90:
            score.grade = "A+"

        elif score.overall >= 80:

            score.grade = "A"

        elif score.overall >= 70:

            score.grade = "B"

        elif score.overall >= 60:

            score.grade = "C"

        else:

            score.grade = "D"

# ==================================================
# Improvement Potential
# ==================================================

        score.improvement_potential = (
            100 - score.overall
        )

# ==================================================
# Insights
# ==================================================

        score.strengths = (
            ats_result.strengths[:3]
            if ats_result.strengths
            else ["Keep building your strengths."]
        )

        score.weaknesses = (
            ats_result.weaknesses[:3]
            if ats_result.weaknesses
            else ["No major weaknesses detected."]
        )

        score.assessment_breakdown = {
            "Resume completeness": score.resume,
            "Overall ATS score": score.ats,
            "Technical skill match": score.technical,
            "Project experience": score.projects,
            "Career readiness": score.career,
            "Interview readiness estimate": score.interview,
        }

        score.next_actions = [
            *[f"Learn and practice {skill}, then demonstrate it in a project." for skill in score.missing_skills[:5]],
            "Add measurable outcomes to relevant projects and experience.",
            "Tailor your resume summary and project descriptions to the target role.",
            "Practice role-specific technical and behavioral interview questions.",
        ]
        if not score.required_skills:
            score.next_actions.insert(0, "Add a specific job description to identify exact matched and missing requirements.")
        elif not score.missing_skills:
            score.next_actions.insert(0, "Maintain your current skill coverage and deepen your strongest skills.")

        return score