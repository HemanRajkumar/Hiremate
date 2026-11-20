
"""HireMate product information page."""

import streamlit as st


def show_product_info():
    st.markdown(
        """
        <section class="hm-hero">
          <div class="hm-eyebrow">About the platform</div>
          <h1>One workspace.<br><span>A clearer career direction.</span></h1>
          <p>HireMate is an AI-powered resume intelligence platform that helps candidates
          understand job fit, improve their resumes, identify skill gaps and prepare for interviews.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="hm-section-kicker">Platform capabilities</div>', unsafe_allow_html=True)
    st.subheader("Everything you need to prepare with confidence")
    features = [
        ("🎯", "ATS Resume Matching", "Compare resume content with job requirements and review match signals."),
        ("🧠", "AI Resume Review", "Surface strengths, weaknesses and actionable improvement suggestions."),
        ("🛠️", "Skill Gap Analysis", "Identify missing skills and prioritize what to learn next."),
        ("🗺️", "Personalized Roadmap", "Turn skill gaps into a structured learning path."),
        ("🏢", "Company Matching", "Explore company and role alignment insights."),
        ("📜", "Certification Intelligence", "Discover certifications relevant to your career direction."),
        ("🎤", "Interview Preparation", "Practice technical, behavioral and resume-based questions."),
        ("📄", "Document Generation", "Generate an optimized resume rewrite and tailored cover letter."),
    ]
    for start in range(0, len(features), 2):
        cols = st.columns(2, gap="large")
        for col, item in zip(cols, features[start:start + 2]):
            with col:
                with st.container(border=True):
                    st.markdown(f"### {item[0]} {item[1]}")
                    st.caption(item[2])

    st.markdown('<div class="hm-section-kicker" style="margin-top:1.5rem">Technology</div>', unsafe_allow_html=True)
    st.subheader("Built with a modular AI stack")
    tech_cols = st.columns(4)
    for col, title, detail in zip(
        tech_cols,
        ("Python", "Streamlit", "Groq AI", "NLP & Parsing"),
        ("Core application", "Interactive interface", "Language model layer", "Resume intelligence"),
    ):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(detail)
    st.markdown(
        '<div class="hm-footer">HireMate · AI-powered resume intelligence</div>',
        unsafe_allow_html=True,
    )
