
import html

import streamlit as st

from styles.colors import PRIMARY


def render_kpi_card(title: str, value: str, color: str = PRIMARY):
    """Render a reusable KPI card."""
    safe_title = html.escape(str(title))
    safe_value = html.escape(str(value))
    st.markdown(
        f"""
        <div style="
          background:linear-gradient(145deg,#202b49,#131d33);
          padding:20px;border-radius:16px;
          border:1px solid rgba(148,163,184,.18);
          color:#f8fafc;text-align:center;
          box-shadow:0 10px 28px rgba(0,0,0,.16);height:100%;
        ">
          <div style="color:#60a5fa;font-size:13px;font-weight:700">{safe_title}</div>
          <div style="font:800 30px Manrope,sans-serif;margin-top:10px">{safe_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
