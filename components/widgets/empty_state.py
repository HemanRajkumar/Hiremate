
import streamlit as st


def render_empty_state() -> None:
    st.markdown(
        """
        <section class="hm-empty">
          <div class="hm-eyebrow">Your career workspace</div>
          <h2 style="margin:.85rem 0 .35rem">Your next opportunity starts here.</h2>
          <p style="color:#9ba8c2;max-width:700px;line-height:1.7">
            Add a resume and a job description above. HireMate will turn them into
            a clear picture of your fit, strengths and next steps.
          </p>
          <div class="hm-empty-grid">
            <div class="hm-empty-item">🎯 &nbsp; ATS match score</div>
            <div class="hm-empty-item">🧩 &nbsp; Skill gap analysis</div>
            <div class="hm-empty-item">🤖 &nbsp; AI resume review</div>
            <div class="hm-empty-item">📈 &nbsp; Career recommendations</div>
            <div class="hm-empty-item">🎤 &nbsp; Interview questions</div>
            <div class="hm-empty-item">📄 &nbsp; Export-ready documents</div>
          </div>
          <div style="color:#60a5fa;font-size:.82rem;font-weight:650">↑ Upload both files to begin your analysis</div>
        </section>
        """,
        unsafe_allow_html=True,
    )
