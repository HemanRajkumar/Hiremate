
"""Premium HireMate metric card component."""

import html

import streamlit as st


def render_metric_card_v2(
    *,
    title: str,
    value: str,
    subtitle: str = "",
    icon: str = "📊",
):
    """Render a compact metric card using the HireMate visual system."""
    safe_title = html.escape(str(title))
    safe_value = html.escape(str(value))
    safe_subtitle = html.escape(str(subtitle))
    safe_icon = html.escape(str(icon))
    st.markdown(
        f"""
        <div style="
          background:linear-gradient(145deg,#17213a,#10182a);
          padding:20px;border-radius:16px;
          border:1px solid rgba(148,163,184,.18);
          text-align:center;min-height:158px;height:100%;
          box-shadow:0 10px 28px rgba(0,0,0,.16);
        ">
          <div style="font-size:28px">{safe_icon}</div>
          <div style="font-size:13px;color:#9ba8c2;margin-top:9px;font-weight:600">{safe_title}</div>
          <div style="font:800 32px Manrope,sans-serif;color:#f8fafc;margin-top:8px">{safe_value}</div>
          <div style="font-size:12px;color:#bfdbfe;margin-top:8px">{safe_subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
