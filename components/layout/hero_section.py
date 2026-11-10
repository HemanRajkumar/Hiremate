
"""Premium HireMate dashboard hero."""

import streamlit as st


def render_hero_section() -> None:
    st.markdown(
        """
        <section class="hm-hero">
          <div class="hm-eyebrow">✦ AI career intelligence platform</div>
          <h1>Make your next move<br><span>your strongest one.</span></h1>
          <p>
            Turn your resume into a career advantage. Evaluate ATS compatibility,
            uncover skill gaps, strengthen your profile and prepare with focused,
            AI-powered guidance.
          </p>
        </section>
        <div class="hm-feature-grid">
          <div class="hm-feature"><div class="hm-feature-icon">🎯</div><div class="hm-feature-title">ATS matching</div><div class="hm-feature-note">Understand job fit</div></div>
          <div class="hm-feature"><div class="hm-feature-icon">🧠</div><div class="hm-feature-title">AI resume review</div><div class="hm-feature-note">Find ways to improve</div></div>
          <div class="hm-feature"><div class="hm-feature-icon">🗺️</div><div class="hm-feature-title">Career roadmap</div><div class="hm-feature-note">Plan your next skills</div></div>
          <div class="hm-feature"><div class="hm-feature-icon">🎤</div><div class="hm-feature-title">Interview prep</div><div class="hm-feature-note">Practice with purpose</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
