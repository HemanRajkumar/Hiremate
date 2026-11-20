<<<<<<< HEAD
"""Clean, readable AI resume rewrite workspace."""
=======
"""
Resume Rewrite Workspace.
"""
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

import streamlit as st


<<<<<<< HEAD
def _plain_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(str(item) for item in value if item)
    if isinstance(value, dict):
        return "\n".join(f"{key}: {val}" for key, val in value.items() if val)
    return str(value)


def _render_projects(projects):
    if isinstance(projects, str):
        if projects.strip():
            st.markdown(projects)
        else:
            st.info("No project rewrites were generated.")
        return
    if isinstance(projects, dict):
        projects = [projects]
    if not isinstance(projects, list) or not projects:
        st.info("No project rewrites were generated.")
        return

    for project in projects:
        if isinstance(project, str):
            with st.container(border=True):
                st.markdown(project)
            continue
        if not isinstance(project, dict):
            continue
        name = project.get("name") or project.get("project_name") or project.get("title") or "Project"
        description = project.get("description") or project.get("project_description") or ""
        with st.container(border=True):
            st.markdown(f"**{name}**")
            if description:
                st.write(description)
            bullets = project.get("bullets") or []
            if isinstance(bullets, str):
                bullets = [bullets]
            for bullet in bullets:
                st.markdown(f"- {bullet}")
            technologies = project.get("technologies") or []
            if isinstance(technologies, str):
                technologies = [x.strip() for x in technologies.split(",") if x.strip()]
            if technologies:
                st.caption("Technologies: " + " · ".join(str(x) for x in technologies))


def _render_skills(skills):
    """Render skills as compact category cards instead of a large text area."""
    if isinstance(skills, str):
        # Compatibility with older cached RewriteResult objects.
        groups = [{"category": "Relevant Skills", "items": [x.strip(" •-*\t") for x in skills.replace(";", ",").replace("\n", ",").split(",") if x.strip(" •-*\t")]}]
    elif isinstance(skills, dict):
        groups = [{"category": key, "items": val if isinstance(val, list) else str(val).split(",")} for key, val in skills.items()]
    else:
        groups = skills or []

    cleaned_groups = []
    seen = set()
    for group in groups:
        if isinstance(group, str):
            category, _, raw = group.partition(":")
            items = raw.split(",") if raw else [category]
            category = category if raw else "Relevant Skills"
        elif isinstance(group, dict):
            category = group.get("category") or "Relevant Skills"
            items = group.get("items") or group.get("skills") or []
            if isinstance(items, str):
                items = items.replace(";", ",").split(",")
        else:
            continue
        unique = []
        for item in items:
            label = str(item).strip(" •-*\t")
            key = label.casefold()
            if label and key not in seen:
                unique.append(label)
                seen.add(key)
        if unique:
            cleaned_groups.append((str(category), unique))

    if not cleaned_groups:
        st.info("No optimized skills were returned. Try generating the rewrite again with a job description.")
        return

    columns_per_row = 2
    for start in range(0, len(cleaned_groups), columns_per_row):
        cols = st.columns(columns_per_row, gap="medium")
        for col, (category, items) in zip(cols, cleaned_groups[start:start + columns_per_row]):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{category}**")
                    # Inline code gives each skill a compact, consistent chip-like treatment.
                    st.markdown("  ".join(f"`{skill}`" for skill in items))


def render_rewrite_tab(rewrite):
    """Render the AI Resume Rewrite workspace."""
    st.title("✨ AI Resume Rewrite")
    st.caption("A clearer, ATS-friendly rewrite tailored to the target role—without inventing experience or achievements.")

    if rewrite is None:
        st.warning("Resume rewrite is unavailable. Run resume analysis again to generate it.")
        return

    # Summary
    st.subheader("📝 Professional Summary")
    with st.container(border=True):
        summary = _plain_text(getattr(rewrite, "professional_summary", ""))
        st.write(summary or "No professional summary was generated.")

    # Experience
    st.subheader("💼 Experience")
    with st.container(border=True):
        experience = _plain_text(getattr(rewrite, "experience", ""))
        st.write(experience or "No employment experience was returned. Keep projects and academic work in their own section.")

    # Projects
    st.subheader("🚀 Projects")
    _render_projects(getattr(rewrite, "projects", []))

    # Skills
    st.subheader("🛠 Optimized Skills")
    st.caption("Grouped by skill type. Learning targets are kept separate from skills already shown in your resume.")
    _render_skills(getattr(rewrite, "skills", []))

    # ATS alignment
    st.subheader("🎯 ATS Alignment")
    with st.container(border=True):
        st.write(_plain_text(getattr(rewrite, "ats_improvement", "")) or "No ATS alignment notes are available.")

    # Suggestions
    st.subheader("💡 Recommended Improvements")
    suggestions = getattr(rewrite, "suggestions", []) or []
    if isinstance(suggestions, str):
        suggestions = [x.strip(" •-*\t") for x in suggestions.splitlines() if x.strip()]
    if suggestions:
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
    else:
        st.info("No additional suggestions were generated.")

    # Export a readable plain-text copy.
    project_lines = []
    projects = getattr(rewrite, "projects", [])
    if isinstance(projects, str):
        project_lines.append(projects)
    else:
        if isinstance(projects, dict):
            projects = [projects]
        for project in projects or []:
            if isinstance(project, dict):
                project_lines.append(project.get("name") or project.get("project_name") or "Project")
                if project.get("description") or project.get("project_description"):
                    project_lines.append(project.get("description") or project.get("project_description"))
                for bullet in project.get("bullets") or []:
                    project_lines.append(f"- {bullet}")
                if project.get("technologies"):
                    project_lines.append("Technologies: " + ", ".join(project["technologies"]) if isinstance(project["technologies"], list) else "Technologies: " + str(project["technologies"]))
            elif project:
                project_lines.append(str(project))

    skill_lines = []
    skills = getattr(rewrite, "skills", [])
    if isinstance(skills, dict):
        skills = [{"category": k, "items": v} for k, v in skills.items()]
    elif isinstance(skills, str):
        skills = [{"category": "Relevant Skills", "items": skills}]
    for group in skills or []:
        if isinstance(group, dict):
            items = group.get("items") or group.get("skills") or []
            if isinstance(items, str):
                items = [x.strip() for x in items.split(",") if x.strip()]
            skill_lines.append(f"{group.get('category', 'Relevant Skills')}: " + ", ".join(str(x) for x in items))
        elif group:
            skill_lines.append(str(group))

    export_text = "\n\n".join([
        "HIREMATE — ATS-OPTIMIZED RESUME REWRITE",
        "PROFESSIONAL SUMMARY\n" + _plain_text(getattr(rewrite, "professional_summary", "")),
        "EXPERIENCE\n" + _plain_text(getattr(rewrite, "experience", "")),
        "PROJECTS\n" + ("\n".join(project_lines) or "No project rewrite generated."),
        "SKILLS\n" + ("\n".join(skill_lines) or "No optimized skills generated."),
        "ATS ALIGNMENT\n" + _plain_text(getattr(rewrite, "ats_improvement", "")),
        "RECOMMENDED IMPROVEMENTS\n" + "\n".join(f"- {x}" for x in suggestions),
    ])

    st.divider()
    st.download_button(
        label="📥 Export ATS-Optimized Resume",
        data=export_text,
        file_name="HireMate_Resume_Rewrite.txt",
        mime="text/plain",
        use_container_width=True,
    )
=======
# ==========================================================
# Resume Rewrite Workspace
# ==========================================================


def render_rewrite_tab(
    rewrite,
):
    """
    Render the AI Resume Rewrite workspace.
    """

    st.title(
        "✨ AI Resume Rewrite"
    )

    st.caption(
        "Generate an ATS-optimized version of your resume while keeping all information truthful."
    )

    if rewrite is None:

        st.warning(
            "Resume rewrite is unavailable."
        )

        return

    # ======================================================
    # Professional Summary
    # ======================================================

    st.subheader(
        "📝 Professional Summary"
    )

    st.text_area(
        "",
        value=rewrite.professional_summary or "No summary generated.",
        height=160,
        disabled=True,
    )

    st.divider()

    # ======================================================
    # Experience
    # ======================================================

    st.subheader(
        "💼 Experience"
    )

    st.text_area(
        "",
        value=rewrite.experience or "No experience generated.",
        height=220,
        disabled=True,
    )

    st.divider()

# ======================================================
# Projects
# ======================================================

    st.subheader(
        "🚀 Projects"
    )

    projects_text = ""

    if isinstance(rewrite.projects, list):

        for project in rewrite.projects:

            if isinstance(project, dict):

                projects_text += (
                    f"• {project.get("project_name",project.get("name", ""))}\n"
                    f"  {project.get("project_description",project.get("description", ""))}\n\n"
                )

            else:

                projects_text += f"• {project}\n"

    else:

        projects_text = rewrite.projects or "No projects generated."

    st.text_area(
        "",
        value=projects_text,
        height=220,
        disabled=True,
    )
    st.divider()

# ======================================================
# Skills
# ======================================================

    st.subheader(
        "🛠 Optimized Skills"
    )

    if isinstance(rewrite.skills, list):

        skills_text = "\n".join(
            f"• {skill}"
            for skill in rewrite.skills
        )

    else:

        skills_text = rewrite.skills or "No skills generated."

    st.text_area(
        "",
        value=skills_text,
        height=180,
        disabled=True,
    )
    st.divider()

    # ======================================================
    # ATS Improvements
    # ======================================================

    st.subheader(
        "🎯 ATS Improvements"
    )

    st.success(
        rewrite.ats_improvement
        or "No ATS improvements available."
    )

    st.divider()

    # ======================================================
    # Suggestions
    # ======================================================

    st.subheader(
        "💡 AI Suggestions"
    )

    if rewrite.suggestions:

        for suggestion in rewrite.suggestions:

            st.markdown(
                f"✅ {suggestion}"
            )

    else:

        st.info(
            "No suggestions available."
        )

    st.divider()

    # ======================================================
    # Export
    # ======================================================

    st.subheader(
        "📄 Export"
    )

    rewritten_resume = f"""
=============================
HireMate AI Resume Rewrite
=============================

Professional Summary

{rewrite.professional_summary}


=================================

Experience

{rewrite.experience}


=================================

Projects

{rewrite.projects}


=================================

Skills

{rewrite.skills}


=================================

ATS Improvements

{rewrite.ats_improvement}


=================================

Suggestions

"""

    if rewrite.suggestions:

        for suggestion in rewrite.suggestions:

            rewritten_resume += (
                f"- {suggestion}\n"
            )

    st.download_button(
        label="📥 Export ATS-Optimized Resume",
        data=rewritten_resume,
        file_name="HireMate_Resume_Rewrite.txt",
        mime="text/plain",
        use_container_width=True,
    )
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
