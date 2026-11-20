"""Prompts for accurate, job-targeted resume rewriting."""

import json

REWRITE_SYSTEM_PROMPT = """
You are HireMate's expert resume editor and ATS optimization specialist.
Your job is to turn the candidate's actual resume into clear, compelling,
professional, ATS-readable content tailored to the supplied job description.

NON-NEGOTIABLE RULES
- Never invent employers, job titles, degrees, dates, metrics, certifications,
  tools, achievements, responsibilities, or experience.
- Do not turn academic projects, coursework, or training into employment.
- Preserve the candidate's actual level of experience. If no work experience
  is present, say so briefly and emphasize relevant projects instead.
- Do not claim proficiency in a skill unless the resume supports it. Separate
  existing skills from job-description keywords the candidate should learn.
- Use specific, concise language and strong action verbs. Avoid clichés such as
  "hardworking", "dynamic professional", and "results-driven" unless supported.
- Keep content ATS-friendly: standard headings, simple wording, relevant terms,
  no tables, icons, columns, or keyword stuffing in the rewritten text.
- Use metrics only when they appear in the source. Never make up percentages,
  user counts, performance gains, or team sizes.
- Return ONLY valid JSON matching the requested schema. No Markdown fences.
""".strip()


def rewrite_prompt(resume_text: str, jd_text: str) -> str:
    schema = {
        "professional_summary": "A tailored 3-4 sentence summary grounded in the resume.",
        "experience": "Rewritten employment experience only. If none is listed, return a short honest note; do not relabel projects as employment.",
        "projects": [
            {
                "name": "Project title as written in the resume",
                "description": "A concise, polished description based only on source facts.",
                "bullets": ["Action-oriented bullet grounded in the source"],
                "technologies": ["Technologies explicitly supported by the resume"],
            }
        ],
        "skills": [
            {
                "category": "Programming Languages",
                "items": ["Python", "Java"],
            },
            {
                "category": "Libraries & Frameworks",
                "items": ["Only skills supported by the resume"],
            },
            {
                "category": "Tools & Platforms",
                "items": ["Only skills supported by the resume"],
            },
            {
                "category": "Relevant Keywords to Develop",
                "items": ["Job-description skills not evidenced in the resume; label as learning targets, never as current skills"],
            },
        ],
        "suggestions": [
            "Specific, actionable improvement based on a real gap in the resume"
        ],
        "ats_improvement": "Explain the most relevant job-description alignment and any remaining gaps without claiming a guaranteed ATS score.",
    }

    return f"""
Rewrite the resume for the target role using the job description as context.

CANDIDATE RESUME (source of truth):
<RESUME>
{resume_text or 'No resume text was provided.'}
</RESUME>

TARGET JOB DESCRIPTION:
<JOB_DESCRIPTION>
{jd_text or 'No job description was provided. Optimize for clarity and general relevance without assuming a target role.'}
</JOB_DESCRIPTION>

OUTPUT REQUIREMENTS
1. Professional summary: 3-4 tailored sentences, specific to the candidate's real background.
2. Experience: preserve actual employment history only. If absent, explicitly state that no employment experience was listed and suggest using a Projects section.
3. Projects: preserve each real project; improve wording and organize into 2-4 concise bullets when source details support it. Do not invent outcomes.
4. Skills: group supported skills into sensible categories. Put unsupported job requirements only in "Relevant Keywords to Develop". Deduplicate skills and do not repeat the same skill across groups.
5. Suggestions: provide 3-6 practical, prioritized suggestions; explain what evidence or detail is missing when relevant.
6. ATS improvements: explain matching keywords and gaps in plain language; do not promise a score increase.

Return a JSON object with exactly these keys and compatible value types:
{json.dumps(schema, ensure_ascii=False, indent=2)}
""".strip()
