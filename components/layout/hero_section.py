<<<<<<< HEAD
"""Compact welcome header and feature overview for the HireMate workspace."""
=======

"""Premium HireMate dashboard hero."""
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

import streamlit as st


def render_hero_section() -> None:
    st.markdown(
        """
        <section class="hm-hero">
<<<<<<< HEAD
          <div class="hm-eyebrow">✦ YOUR AI CAREER WORKSPACE</div>
          <h1>Welcome back! <span>Let’s build your next opportunity.</span></h1>
          <p>Upload your resume and a target job description to uncover your strengths, close skill gaps and prepare a more compelling application.</p>
        </section>
        <div class="hm-feature-grid">
          <div class="hm-feature"><div class="hm-feature-icon">🎯</div><div class="hm-feature-title">ATS match</div><div class="hm-feature-note">See how your resume aligns</div></div>
          <div class="hm-feature"><div class="hm-feature-icon">🧠</div><div class="hm-feature-title">AI resume review</div><div class="hm-feature-note">Get clear, useful feedback</div></div>
          <div class="hm-feature"><div class="hm-feature-icon">🗺️</div><div class="hm-feature-title">Career roadmap</div><div class="hm-feature-note">Prioritize your next skills</div></div>
          <div class="hm-feature"><div class="hm-feature-icon">🎤</div><div class="hm-feature-title">Interview prep</div><div class="hm-feature-note">Practice with confidence</div></div>
=======
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
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
        </div>
        """,
        unsafe_allow_html=True,
    )
