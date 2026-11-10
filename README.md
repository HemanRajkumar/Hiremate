<div align="center">

# HireMate

### AI-Powered Resume Intelligence Platform

**Understand your resume. Identify skill gaps. Prepare for your next opportunity.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI%20Integration-111827?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-2563EB?style=for-the-badge)

</div>

---

## Overview

HireMate is a resume intelligence application built with Python and Streamlit. It helps job seekers evaluate how their resume aligns with a target role, understand missing skills, improve resume content, and prepare for interviews.

The application combines resume parsing, job-description analysis, ATS-oriented comparisons, career guidance, and AI-assisted content generation in one workspace.

## Design

HireMate uses a **black, white, and blue** visual theme:

- Near-black backgrounds for the main application.
- White typography for clear hierarchy and readability.
- Electric blue accents for primary actions, active navigation, and highlights.
- Charcoal surfaces and subtle borders for cards and content sections.
- Responsive layouts intended for desktop, tablet, and mobile screens.

## Features

### Resume analysis
- Upload and parse a PDF resume.
- Extract candidate information, education, experience, projects, and skills.
- Review resume content and detected profile information.

### Target-role and ATS analysis
- Upload a target job description as a PDF or TXT file.
- Compare resume skills with the requirements in the job description.
- View matched skills and missing skills.
- Review ATS-oriented scores and analysis results.

### Resume improvement
- Review resume strengths and areas that may need improvement.
- Get AI-assisted suggestions for improving resume content.
- Generate an ATS-oriented rewrite of resume sections.

### Career intelligence
- Explore skill gaps related to a target role.
- Review learning-roadmap recommendations.
- Explore career guidance, company-match suggestions, and certification recommendations where available in the application.

### Interview preparation
- Generate role- and resume-related interview practice questions.
- Prepare for technical, behavioral, and HR interview topics.

### Documents
- Generate supporting application content, including AI-assisted cover-letter content where configured.
- Review and export generated content using the available document actions.

> Feature availability and generated results depend on the configured services, uploaded documents, and the current application implementation.

## Technology stack

| Area | Technologies |
|---|---|
| Application UI | Streamlit |
| Core language | Python |
| AI integration | Groq API |
| Resume and document parsing | PDF parsing utilities |
| Data processing | Pandas, NumPy |
| Visualisation | Plotly and Streamlit components |
| Configuration | Python environment variables and `python-dotenv` |

## Project structure

```text
HireMate/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── components/
│   ├── dashboard/
│   ├── layout/
│   ├── ui/
│   └── widgets/
├── data/
├── models/
├── services/
├── styles/
├── utils/
├── views/
│   └── dashboard_modules/
│       └── tabs/
└── docs/
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/HemanRajkumar/Hiremate.git
cd Hiremate
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell does not allow activation, you can run the environment's Python executable directly using `.venv\Scripts\python.exe`.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a file named `.env` in the project root. Add your own Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The project reads this value from the environment. Keep `.env` private and never commit it to GitHub. The `.env.example` file is provided as a configuration template.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will print a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that address in your browser.

## How to use HireMate

1. Start the application.
2. Open the Dashboard.
3. Upload your resume in PDF format.
4. Upload the target job description in PDF or TXT format.
5. Run the analysis.
6. Review the ATS-oriented results, matched skills, and missing skills.
7. Explore the Resume, Rewrite, Career, Interview, and Documents workspaces.
8. Use the recommendations to plan improvements to your resume and preparation.

For best results, use a readable, text-based PDF resume and a job description that clearly lists responsibilities and required qualifications.

## Configuration

Application configuration is defined in `config.py`.

| Setting | Description |
|---|---|
| `GROQ_API_KEY` | API key used for Groq-powered AI features |
| `GROQ_MODEL` | Groq model configured by the application |
| `TEMPERATURE` | Generation temperature |
| `MAX_TOKENS` | Maximum response token setting |
| `SUPPORTED_RESUME_TYPES` | Accepted resume upload types |
| `SUPPORTED_JD_TYPES` | Accepted target job-description upload types |

The current configuration accepts PDF resumes and PDF or TXT job descriptions.

## Troubleshooting

### `streamlit` command is not recognized

Run Streamlit through Python instead:

```bash
python -m streamlit run app.py
```

### Windows blocks `streamlit.exe`

If Windows Application Control blocks the executable, do not attempt to bypass your organization's security policy. Try the Python module command above. If the policy also blocks Python execution, contact your device administrator.

### `GROQ_API_KEY not found in .env`

- Confirm that `.env` is in the same directory as `app.py`.
- Confirm the variable is spelled exactly as `GROQ_API_KEY`.
- Restart the Streamlit application after changing the file.
- Do not add quotation marks unless required by your environment setup.

### Dependency installation fails

Confirm that the intended virtual environment is active and that the correct Python version is installed. Then retry:

```bash
python -m pip install -r requirements.txt
```

## Security and privacy

- Do not commit `.env`, API keys, passwords, or Streamlit secrets.
- Do not commit private resumes, uploaded job descriptions, or generated documents containing personal information.
- Review `.gitignore` before pushing changes.
- Use API credentials only in your local environment or an appropriately secured deployment secret store.

## Development

Before committing changes, check the working tree:

```bash
git status
```

Run the application locally and test the resume upload, job-description upload, analysis flow, and each dashboard workspace affected by your changes.

## Contributing

Contributions and suggestions are welcome. For a change:

1. Create a branch.
2. Make a focused update.
3. Test the affected workflow.
4. Commit with a descriptive message.
5. Open a pull request describing the change.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**HireMate — make every application more intentional.**

Built with Python, Streamlit, and AI.

</div>
