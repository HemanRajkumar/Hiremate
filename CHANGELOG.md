# Changelog

All notable changes to HireMate will be documented in this file.

---

## [0.1.0] - Resume Intelligence Engine

### Added
- Modular project architecture
- Resume upload functionality
- PDF text extraction
- Resume preview
- Resume metadata extraction
- Resume intelligence engine
- Skill extraction using knowledge base
- Dashboard
- GitHub repository
- Version tag v0.1.0

---

## Upcoming

### 0.2.0
- Job Description Parser
- ATS Matching Engine
- Skill Gap Analysis
## [0.2.0] - ATS Matching Engine

### Added
- Job Description parser (PDF/TXT)
- JobData model
- ATS comparison engine
- AnalysisService orchestration layer
- Skill matching
- Missing skill detection
- Additional skill detection
- ATS score calculation
- Dashboard integration
# Changelog

## [v0.3.0] - 2026-07-05

### Added
- Modular component architecture
- Dashboard analytics
- ATS score engine
- Gauge chart visualization
- Skill comparison chart
- Resume statistics
- Candidate information panel
- Resume preview widget
- Hero section
- Custom sidebar navigation

### Improved
- Refactored services into modular architecture
- Organized reusable UI components
- Enhanced dashboard responsiveness
- Improved ATS scoring workflow

### Fixed
- Streamlit multipage navigation conflict
- Import path issues after folder restructuring
- SkillService initialization bug
- Package initialization errors
## Company matching and recommendation completeness
- Added role-based baseline skill requirements for short target-role inputs such as `Data Science`, so ATS and hireability comparisons no longer show an empty 0% skill result for a role-only target.
- Company match records now include matched, missing, and full required skill lists plus an explanation of the recommendation.
- Replaced the empty project recommendation placeholder with domain-aware portfolio projects.
- Added domain-relevant certification fallbacks when no missing-skill-specific certification is found.
- Ensured the learning roadmap includes practical steps when there are no detected skill gaps.
- Added a dedicated company match card layout with separate skill, ATS, and hireability scores.
