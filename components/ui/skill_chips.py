
"""Accessible, escaped skill chips."""

import html

import streamlit as st


def render_skill_chips(skills: list[str]):
    """Render compact horizontal skill tags."""
    if not skills:
        st.caption("No skills found.")
        return

    chips = "".join(
        (
            '<span style="padding:6px 12px;border-radius:999px;'
            'background:rgba(37,99,235,.13);'
            'border:1px solid rgba(129,140,248,.28);'
            'color:#dbeafe;font-size:12px;font-weight:600;'
            'white-space:nowrap;display:inline-block">'
            f'{html.escape(str(skill))}</span>'
        )
        for skill in skills
    )
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 12px">{chips}</div>',
        unsafe_allow_html=True,
    )
