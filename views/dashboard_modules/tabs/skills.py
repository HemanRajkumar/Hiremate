
"""
Skills Dashboard Tab.

Responsibilities:
- Display matched skills
- Display missing skills
- Display skill statistics
"""

import html as html_lib

import streamlit as st

from models.ats_model import ATSResult


def render_skill_chips(
    skills: list[str],
    color: str,
):
    """
    Render compact horizontal skill chips.
    """

    if not skills:
        st.info("None")
        return

    html_content = (
        '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
    )

    for skill in skills:
        html_content += (
            f'<span style="'
            f'background:rgba(37,99,235,.14);'
            f'color:#dbeafe;'
            f'border:1px solid {color};'
            f'padding:6px 14px;'
            f'border-radius:999px;'
            f'font-size:13px;'
            f'font-weight:600;'
            f'white-space:nowrap;'
            f'display:inline-block;'
            f'">'
            f'{html_lib.escape(str(skill))}'
            f'</span>'
        )

    html_content += "</div>"

    st.markdown(
        html_content,
        unsafe_allow_html=True,
    )


def render_skills_tab(
    ats_result: ATSResult,
):
    """
    Render the Skills dashboard tab.
    """

    left, right = st.columns(2)

    with left:
        st.subheader("✅ Matched Skills")

        render_skill_chips(
            ats_result.matched_skills,
            "#16a34a",
        )

    with right:
        st.subheader("❌ Missing Skills")

        render_skill_chips(
            ats_result.missing_skills,
            "#d97706",
        )

    st.divider()

    st.subheader("📈 Skills Overview")

    stat1, stat2, stat3 = st.columns(3)

    matched_count = len(ats_result.matched_skills)
    missing_count = len(ats_result.missing_skills)

    total = matched_count + missing_count

    match_rate = (
        round(matched_count / total * 100)
        if total
        else 100
    )

    with stat1:
        st.metric(
            "Matched",
            matched_count,
        )

    with stat2:
        st.metric(
            "Missing",
            missing_count,
        )

    with stat3:
        st.metric(
            "Match Rate",
            f"{match_rate}%",
        )

    st.divider()

    st.caption(
        "Skills were automatically extracted by comparing "
        "your resume with the uploaded job description."
    )
