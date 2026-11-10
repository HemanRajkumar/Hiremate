
"""HireMate application navigation."""

import streamlit as st


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="hm-brand">
                <div class="hm-brand-mark">H</div>
                <div>
                    <div class="hm-brand-name">HireMate</div>
                    <div class="hm-brand-sub">Career intelligence</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("YOUR WORKSPACE")
        st.divider()
        page = st.radio(
            "Navigation",
            ("🏠 Dashboard", "📘 Product Info"),
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown(
            """
            <div style="padding:.45rem .2rem">
              <div style="color:#60a5fa;font-size:.7rem;font-weight:750;letter-spacing:.12em">AI-POWERED</div>
              <div style="color:#8492ad;font-size:.78rem;line-height:1.6;margin-top:.35rem">
                Resume intelligence, career insights and interview readiness in one place.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hm-footer" style="text-align:left;border:0;margin-top:1.2rem;padding:.5rem 0">HireMate · v1.0.0</div>',
            unsafe_allow_html=True,
        )
    return page
