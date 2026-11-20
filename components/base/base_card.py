
import html

import streamlit as st


def render_base_card(title: str, body: str = "", icon: str = ""):
    """Render a reusable HireMate content card."""
    safe_title = html.escape(str(title))
    safe_icon = html.escape(str(icon))
    st.markdown(
        f"""
        <div style="
          background:linear-gradient(145deg,rgba(22,31,52,.96),rgba(13,20,35,.96));
          padding:22px;border-radius:18px;border:1px solid rgba(148,163,184,.18);
          box-shadow:0 12px 32px rgba(0,0,0,.16);margin-bottom:18px;
        ">
          <h3 style="margin:0 0 12px;color:#f3f5ff">{safe_icon} {safe_title}</h3>
          <div style="color:#cbd5e1;line-height:1.65">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
