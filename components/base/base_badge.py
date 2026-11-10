
import html

import streamlit as st


def render_badge(text: str, color: str = "#3B82F6"):
    """Render a compact badge."""
    safe_text = html.escape(str(text))
    st.markdown(
        f"""
        <span style="
          background:rgba(37,99,235,.16);color:#c7d2fe;
          border:1px solid rgba(129,140,248,.32);
          padding:6px 12px;border-radius:999px;font-size:12px;
          font-weight:700;display:inline-block;margin:4px;
        ">{safe_text}</span>
        """,
        unsafe_allow_html=True,
    )
