<<<<<<< HEAD
"""Reusable project card with structured dates, locations and bullet details."""
import streamlit as st
from components.ui.skill_chips import render_skill_chips


def render_project_card(project):
    with st.container(border=True):
        st.markdown(f"### 🚀 {project.title or 'Untitled Project'}")
        if getattr(project, "date", ""):
            st.caption(f"📅 {project.date}")
        if getattr(project, "location", ""):
            st.caption(f"📍 {project.location}")
        bullets = getattr(project, "bullets", []) or ([project.description] if project.description else [])
        for bullet in bullets:
            st.markdown(f"- {bullet}")
        if getattr(project, "github_url", ""):
            st.markdown(f"[GitHub repository]({project.github_url})")
        if project.technologies:
            st.markdown("**Technologies**")
            render_skill_chips(project.technologies)
=======
"""
Reusable Project Card.
"""

import streamlit as st

from components.ui.skill_chips import (
    render_skill_chips,
)


def render_project_card(project):
    """
    Render a project as a premium card.
    """

    with st.container(border=True):

        st.markdown(
            f"### 🚀 {project.title or 'Untitled Project'}"
        )

        if project.description:

            st.write(
                project.description
            )

        if project.technologies:

            st.markdown("**Technologies**")

            render_skill_chips(
                project.technologies,
            )
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
