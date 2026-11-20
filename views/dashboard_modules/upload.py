
"""
Dashboard upload module.

Renders the resume and job-description upload controls and loads their text.
"""

from typing import Tuple

import streamlit as st

from components.uploader import save_uploaded_file
from config import SUPPORTED_JD_TYPES, SUPPORTED_RESUME_TYPES
from utils.parser import extract_pdf_data


def render_upload_section():
    st.markdown(
        """
        <div style="margin:.2rem 0 1rem">
          <div class="hm-section-kicker">Start your analysis</div>
          <h2 style="margin:.3rem 0">Add your documents</h2>
          <p style="color:#9ba8c2;margin:0">Upload your resume and the job description you want to target.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("#### 📄 Your resume")
            st.caption("Upload the latest version of your CV or resume.")
            resume = st.file_uploader(
                "Choose resume file",
                type=SUPPORTED_RESUME_TYPES,
                key="resume",
                help="Supported formats are configured by HireMate.",
                label_visibility="collapsed",
            )
            if resume:
                st.caption(f"✓ {resume.name} · {resume.size / 1024:.0f} KB")
    with right:
        with st.container(border=True):
            st.markdown("#### 💼 Target job description")
            st.caption("Add the role requirements to compare against your profile.")
            jd = st.file_uploader(
                "Choose job description",
                type=SUPPORTED_JD_TYPES,
                key="jd",
                help="Supported formats are configured by HireMate.",
                label_visibility="collapsed",
            )
            if jd:
                st.caption(f"✓ {jd.name} · {jd.size / 1024:.0f} KB")
    return resume, jd


def load_documents(resume, jd) -> Tuple[dict, str, str]:
    resume.seek(0)
    jd.seek(0)
    resume_path = save_uploaded_file(resume)
    jd_path = save_uploaded_file(jd)
    resume_pdf = extract_pdf_data(resume_path)
    resume_text = resume_pdf["text"]
    if jd.name.lower().endswith(".pdf"):
        jd_pdf = extract_pdf_data(jd_path)
        jd_text = jd_pdf["text"]
    else:
        with open(jd_path, "r", encoding="utf-8") as file:
            jd_text = file.read()
    return resume_pdf, resume_text, jd_text
