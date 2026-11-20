# HireMate Frontend Refresh

## What changed
- Replaced the light default styling with a responsive dark navy, indigo, violet and cyan design system.
- Updated the global Streamlit styling for navigation, tabs, metrics, cards, forms, uploaders, alerts, charts and mobile layouts.
- Redesigned the sidebar, dashboard hero, upload section, empty state and Product Info page.
- Refreshed shared metric, KPI, badge, card and skill-chip components.
- Added HTML escaping to user-controlled text in the refreshed badge and skill-chip components.

## What was intentionally preserved
- Resume parsing and upload keys.
- Analysis pipeline, AI prompts, models, services and session-state contracts.
- Existing dashboard workspace/tab functions and document-generation logic.

## Apply / run
This archive contains the updated project. Replace your local project folder with this folder, configure your own API key using the project's existing environment setup, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The uploaded archive contained local uploaded documents and Python cache files. Those were intentionally excluded from this refreshed archive; they are runtime artifacts, not application source.
