import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { extractResumePdf, fullAnalysis, generateRewrite, getHealth, previewAnalysis, type FullAnalysis, type PreviewResult } from "./api";

type Page = "Dashboard" | "Resume" | "Rewrite" | "Career" | "Interview" | "Documents";
const pages: Array<{ name: Page; icon: string; hint: string }> = [
  { name: "Dashboard", icon: "⌂", hint: "Your career overview" }, { name: "Resume", icon: "▤", hint: "Profile and ATS analysis" },
  { name: "Rewrite", icon: "✦", hint: "Improve your resume" }, { name: "Career", icon: "↗", hint: "Roadmaps and opportunities" },
  { name: "Interview", icon: "◉", hint: "Practice with confidence" }, { name: "Documents", icon: "▧", hint: "Your career documents" },
];
const roles = ["Machine Learning Engineer", "AI Engineer", "Data Scientist", "Python Developer", "Full Stack Developer", "Frontend Developer", "Backend Developer", "Cloud Engineer", "DevOps Engineer", "Data Analyst"];
const starterSkills = ["Python", "Pandas", "SQL", "Scikit-learn", "Git", "NumPy"];

function App() {
  const [page, setPage] = useState<Page>("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);
  const [apiOnline, setApiOnline] = useState(false);
  const [apiLabel, setApiLabel] = useState("Connecting to HireMate API");
  const [role, setRole] = useState(roles[0]);
  const [skills, setSkills] = useState(starterSkills);
  const [skillDraft, setSkillDraft] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [resumeName, setResumeName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [preview, setPreview] = useState<PreviewResult | null>(null);
  const [analysis, setAnalysis] = useState<FullAnalysis | null>(null);
  const [busy, setBusy] = useState(false);
  const [busyLabel, setBusyLabel] = useState("");
  const [error, setError] = useState("");
  const [dark, setDark] = useState(false);
  const [dashboardCleared, setDashboardCleared] = useState(false);

  useEffect(() => { getHealth().then((h) => { setApiOnline(true); setApiLabel(h.ai_configured ? `API + AI connected · v${h.version}` : `API connected · add GROQ_API_KEY for AI reports`); }).catch(() => { setApiOnline(false); setApiLabel("Backend offline · start the API on port 8000"); }); }, []);
  const score = preview ? Math.round(preview.ats.overall_score) : dashboardCleared ? 0 : 67;
  const scoreLabel = dashboardCleared && !preview ? "—" : `${score}%`;
  const matched = preview?.ats.matched_skills ?? (dashboardCleared ? [] : ["Python", "NumPy", "Pandas", "Scikit-learn", "SQL", "Git"]);
  const gaps = preview?.ats.missing_skills ?? (dashboardCleared ? [] : ["Docker", "FastAPI", "MLOps"]);

  async function uploadResume(file?: File) {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) { setError("Please upload a PDF resume."); return; }
    setBusy(true); setBusyLabel("Reading your resume…"); setError("");
    try { const parsed = await extractResumePdf(file); setResumeText(parsed.text); setResumeName(file.name); setPage("Resume"); }
    catch (e) { setError(e instanceof Error ? e.message : "Resume upload failed."); }
    finally { setBusy(false); setBusyLabel(""); }
  }
  function addSkill(e?: FormEvent) { e?.preventDefault(); const value = skillDraft.trim(); if (value && !skills.some(s => s.toLowerCase() === value.toLowerCase())) setSkills([...skills, value]); setSkillDraft(""); }
  function removeSkill(value: string) { setSkills(skills.filter(s => s !== value)); }

  // The example is shown only on first load. Reset clears the dashboard completely.
  function resetDashboard() {
    setDashboardCleared(true);
    setRole("");
    setSkills([]);
    setSkillDraft("");
    setJobDescription("");
    setPreview(null);
    setAnalysis(null);
    setError("");
  }

  async function runPreview(e?: FormEvent) {
    e?.preventDefault();
    // Dashboard skill matching must use only the skills the candidate explicitly entered.
    // Including the target role here caused words such as "Machine Learning" to be
    // extracted as if they were candidate skills. Resume analysis remains on the Resume page.
    const text = `Candidate skills: ${skills.join(", ")}.`;
    const jd = jobDescription.trim() || `We are seeking a ${role}. Required skills include Python, SQL, NumPy, Pandas, Scikit-learn, Docker, FastAPI, MLOps, Git and cloud deployment.`;
    setBusy(true); setBusyLabel("Analyzing skills and experience…"); setError("");
    try { const result = await previewAnalysis(text, jd); setPreview(result); setDashboardCleared(false); setPage("Dashboard"); }
    catch (e) { setError(e instanceof Error ? e.message : "Analysis failed. Check that the backend is running."); }
    finally { setBusy(false); setBusyLabel(""); }
  }
  async function runResumePreview() {
    if (!resumeText.trim()) { setError("Upload or paste your resume before analyzing it."); return; }
    const jd = jobDescription.trim() || `We are seeking a ${role || "software professional"}. Required skills include Python, SQL, NumPy, Pandas, Scikit-learn, Docker, FastAPI, MLOps, Git and cloud deployment.`;
    setBusy(true); setBusyLabel("Analyzing your resume…"); setError("");
    try {
      const result = await previewAnalysis(resumeText, jd);
      setPreview(result);
      setAnalysis(null);
      setDashboardCleared(false);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Resume analysis failed. Check that the backend is running.");
    } finally { setBusy(false); setBusyLabel(""); }
  }

  async function runRewrite() {
    if (!resumeText.trim()) {
      setError("Upload a PDF resume or paste your resume text before generating an optimized resume.");
      setPage("Resume");
      return;
    }
    const targetRole = role || "Software Engineer";
    const jd = jobDescription.trim() || `Target role: ${targetRole}. Tailor this resume for the ${targetRole} role. Use only skills, projects, education, and experience supported by the resume.`;
    setBusy(true);
    setBusyLabel("Generating your optimized resume…");
    setError("");
    try {
      const result = await generateRewrite(resumeText.trim(), jd);
      if (!result.rewrite || result.rewrite.error) {
        throw new Error(result.rewrite?.error || "The resume rewrite could not be generated. Check your Groq API configuration and try again.");
      }
      setAnalysis(current => ({ ...(current || {}), rewrite: result.rewrite }));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Resume rewrite failed. Check the backend and Groq API configuration.");
    } finally {
      setBusy(false);
      setBusyLabel("");
    }
  }

  async function runFull() {
    if (!resumeText.trim()) { setError("Upload a PDF resume or paste your resume text before generating the report."); setPage("Resume"); return; }
    // A JD is helpful but not mandatory: provide a clearly labelled role-based brief
    // so users can still generate a report when they do not have a posting yet.
    const targetRole = role || "Software Engineer";
    const jd = jobDescription.trim() || `Target role: ${targetRole}. Analyze this resume for suitability for the ${targetRole} role. Assess relevant technical skills, experience, projects, education, strengths, gaps, and practical next steps. Do not assume experience or skills that are not present in the resume.`;
    setBusy(true); setBusyLabel("Generating your personalized AI report… This may take a minute."); setError("");
    setAnalysis(null);
    try {
      const data = await fullAnalysis(resumeText.trim(), jd);
      const required = ["resume", "job", "ats", "skill_gap"];
      const missing = required.filter(key => data[key] == null);
      if (missing.length) throw new Error(`The report response was incomplete (missing ${missing.join(", ")}). Check the backend logs and try again.`);
      setAnalysis(data);
      setPreview({ resume: data.resume, job: data.job, ats: data.ats, skill_gap: data.skill_gap } as PreviewResult);
      setDashboardCleared(false);
    } catch (e) { setError(e instanceof Error ? e.message : "Full AI analysis failed. Check the backend and Groq API configuration."); }
    finally { setBusy(false); setBusyLabel(""); }
  }
  function onFileChange(e: ChangeEvent<HTMLInputElement>) { void uploadResume(e.target.files?.[0]); }

  return <div className={`app ${dark ? "dark" : ""}`}>
    <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
      <a className="brand" href="#dashboard" onClick={() => setPage("Dashboard")}><span className="brand-mark">↗</span><span>Hire<span className="brand-accent">Mate</span><small>CAREER INTELLIGENCE</small></span></a>
      <div className="side-caption">WORKSPACE</div>
      <nav>{pages.map(item => <button key={item.name} className={`nav-item ${page === item.name ? "active" : ""}`} onClick={() => { setPage(item.name); setMenuOpen(false); }}><span className="nav-icon">{item.icon}</span><span>{item.name}</span>{page === item.name && <i />}</button>)}</nav>
      <div className="sidebar-bottom"><div className="upgrade-card"><span className="upgrade-icon">✦</span><b>Build your next chapter</b><p>Turn your skills into a career plan.</p><button onClick={() => setPage("Career")}>Explore career paths <span>→</span></button></div><div className="profile-mini"><div className="avatar">H</div><div><b>Welcome back</b><small>Candidate workspace</small></div><span className="profile-more">•••</span></div></div>
    </aside>
    {menuOpen && <button className="mobile-scrim" aria-label="Close menu" onClick={() => setMenuOpen(false)} />}
    <main className="main-area">
      <header className="topbar"><div className="top-left"><button className="hamburger" aria-label="Open navigation" onClick={() => setMenuOpen(!menuOpen)}><span/><span/><span/></button><div className="breadcrumb">Workspace <span>/</span> <b>{page}</b></div></div><div className="top-actions"><div className={`api-pill ${apiOnline ? "online" : "offline"}`}><i/>{apiLabel}</div><button className="icon-button" title="Toggle theme" onClick={() => setDark(!dark)}>{dark ? "☾" : "☼"}</button><div className="avatar top-avatar">H</div></div></header>
      <div className="content">
        <section className="page-heading"><div><p className="eyebrow">YOUR CAREER, IN FOCUS</p><h1>{page === "Dashboard" ? "Welcome back! 👋" : page === "Resume" ? "Your resume workspace" : page === "Rewrite" ? "Make your resume stand out" : page === "Career" ? "Plan your next move" : page === "Interview" ? "Prepare with confidence" : "Your documents"}</h1><p>{page === "Dashboard" ? "Let's bridge your skill gap and move closer to your goals." : pages.find(p => p.name === page)?.hint}</p></div><div className="match-badge"><strong>{scoreLabel}</strong><span>{dashboardCleared && !preview ? "No analysis" : "Overall ATS"}</span></div></section>
        {error && <div className="alert-error"><span>!</span>{error}<button onClick={() => setError("")}>×</button></div>}
        {page === "Dashboard" && <>
          <div className="dashboard-grid">
            <section className="card analyzer-card"><div className="card-title"><span className="title-icon">◎</span><div><h2>Skill gap analyzer</h2><p>Compare your skills with your target role</p></div></div>
              <form onSubmit={runPreview} className="analyzer-form"><label className="field-label">1. Select target role<select value={role} onChange={e => setRole(e.target.value)}><option value="">Select a target role…</option>{roles.map(r => <option key={r}>{r}</option>)}</select></label><label className="field-label">2. Your current skills</label><div className="skill-entry"><div className="chips">{skills.map(s => <span className="chip" key={s}>{s}<button type="button" onClick={() => removeSkill(s)}>×</button></span>)}<input value={skillDraft} onChange={e => setSkillDraft(e.target.value)} onKeyDown={e => { if (e.key === "Enter" || e.key === ",") { e.preventDefault(); addSkill(); } }} placeholder="Add a skill and press Enter…" /></div></div><p className="tip">💡 Add all the skills you currently know. You can also upload your resume in the Resume section.</p><label className="field-label">Job description <span className="optional">(optional)</span><textarea className="jd-input" value={jobDescription} onChange={e => setJobDescription(e.target.value)} placeholder="Paste a job description for a more accurate analysis…" /></label><div className="form-actions"><button className="primary-button" disabled={!apiOnline || busy || !role || skills.length === 0} type="submit">✦ {busy ? busyLabel || "Analyzing…" : "Analyze my skills"}</button><button type="button" className="secondary-button" onClick={resetDashboard}>↻ Reset</button></div></form>
            </section>
            <section className="card explainer-card"><div className="explainer-content"><span className="eyebrow">SMARTER CAREER DECISIONS</span><h2>AI-powered skill gap analysis</h2><p>Understand where you stand, discover the skills employers are looking for, and get a practical plan to become job-ready.</p><ul><li><span>✓</span> Match percentage and skill coverage</li><li><span>✓</span> Priority-based skill gap identification</li><li><span>✓</span> Personalized learning roadmap</li><li><span>✓</span> Resume and career recommendations</li></ul></div><div className="orbit-art"><div className="orbit orbit-one"/><div className="orbit orbit-two"/><div className="orbit-core">✦</div><span className="orbit-dot dot-a"/><span className="orbit-dot dot-b"/></div></section>
          </div>
          <div className="lower-grid"><section className="card results-card"><div className="section-head"><div className="card-title"><span className="title-icon">◷</span><div><h2>Your skill analysis</h2><p>{preview ? `Analysis for ${preview.job.job_info.title || role}` : dashboardCleared ? "Dashboard cleared · add details to start a new analysis" : "Sample preview · run an analysis to see your results"}</p></div></div><button className="text-button" onClick={() => setPage("Resume")}>Resume details →</button></div><div className="results-layout"><div className="score-wrap"><div className="score-ring" style={{background: `conic-gradient(#675be9 ${score}%, #e9eaf1 0)`}}><div><strong>{scoreLabel}</strong><small>{dashboardCleared && !preview ? "No analysis" : "Overall ATS"}</small></div></div><p>{dashboardCleared && !preview ? "Your dashboard is clear. Add a role and skills to begin." : score >= 75 ? "You're close to job-ready!" : "A good foundation to build on."}</p></div><div className="skill-columns"><div>{preview && <p className="muted-note">Skill match: <strong>{Math.round(preview.ats.skills_score)}%</strong> · based on required job-description skills</p>}<h3 className="matched-heading">✓ Matched skills <b>({matched.length})</b></h3>{matched.length ? matched.map(s => <div className="skill-row good" key={s}>✓ {s}</div>) : <p className="muted-note">{dashboardCleared ? "No matched skills yet. Add skills and analyze to begin." : "No matched skills yet."}</p>}</div><div><h3 className="gap-heading">△ Skill gaps <b>({gaps.length})</b></h3>{gaps.length ? gaps.map((s,i) => <div className="skill-row gap" key={s}>△ {s}<span className={`priority priority-${i===0?"high":"medium"}`}>{i===0?"High":"Medium"}</span></div>) : <p className="muted-note">{dashboardCleared ? "Skill gaps will appear after your analysis." : "No skill gaps yet."}</p>}</div></div></div></section>
            <section className="card roadmap-card"><div className="section-head"><div className="card-title"><span className="title-icon">⌁</span><div><h2>Personalized learning roadmap</h2><p>Your next steps, in the right order</p></div></div><button className="small-primary" onClick={() => { if (analysis?.roadmap) setPage("Career"); else void runFull(); }} disabled={busy}>Generate roadmap ✨</button></div>{analysis?.roadmap ? <div className="roadmap-preview">{(analysis.roadmap.tasks || []).slice(0,3).map((t:any,i:number)=><div className="roadmap-step" key={i}><span>{i+1}</span><div><b>{t.title || t.name}</b><small>{t.description || "Build this competency with guided practice."}</small></div></div>)}</div> : <div className="empty-roadmap"><div className="empty-illustration">⌁</div><p>Analyze your skills to create a personalized learning roadmap.</p><button className="outline-button" onClick={() => setPage("Career")}>Explore career roadmap →</button></div>}</section></div>
        </>}
        {page === "Resume" && <div className="single-column"><section className="card upload-card"><div className="card-title"><span className="title-icon">▤</span><div><h2>Upload your resume</h2><p>PDF format · up to 10 MB · your resume stays in your workspace</p></div></div><label className="dropzone"><input type="file" accept=".pdf,application/pdf" onChange={onFileChange}/><span className="upload-symbol">↑</span><b>{resumeName || "Drop your resume here or browse files"}</b><small>{busy ? busyLabel : "PDF document · Select a file to parse your profile"}</small></label><label className="field-label">Resume text <textarea className="large-textarea" value={resumeText} onChange={e => setResumeText(e.target.value)} placeholder="Upload a PDF or paste your resume text here…" /></label><label className="field-label">Target job description (optional — a role-based report can be generated without one) <textarea className="large-textarea" value={jobDescription} onChange={e => setJobDescription(e.target.value)} placeholder="Paste the job description you want to target…" /></label><div className="form-actions"><button className="primary-button" onClick={() => void runResumePreview()} disabled={!apiOnline || busy || !resumeText.trim()}>Analyze resume</button><button className="secondary-button" onClick={() => void runFull()} disabled={!apiOnline || busy || !resumeText.trim()}>{busy ? busyLabel : "Run full AI report ✦"}</button></div></section>{preview && <section className="card"><h2>Resume analysis results</h2><div className="metric-strip"><Metric label="Overall ATS" value={`${Math.round(preview.ats.overall_score)}%`}/><Metric label="Skill match" value={`${Math.round(preview.ats.skills_score)}%`}/><Metric label="Skills matched" value={preview.ats.matched_skills.length}/><Metric label="Skills to develop" value={preview.ats.missing_skills.length}/></div></section>}{analysis && <FullReport data={analysis}/>}</div>}
        {page === "Rewrite" && <div className="single-column"><section className="card rewrite-card"><div className="card-title"><span className="title-icon">✦</span><div><h2>AI resume rewrite</h2><p>Get clear, role-specific improvements grounded in your actual experience.</p></div></div><div className="rewrite-intro"><b>Ready to improve your resume?</b><p>Upload your resume and provide a target job description in the Resume section. HireMate will generate a professional summary, stronger project descriptions, organized skills and actionable ATS suggestions.</p><button className="primary-button" onClick={() => void runRewrite()} disabled={busy || !resumeText.trim()}>{busy ? busyLabel : "Generate optimized resume ✨"}</button><button className="text-button" onClick={() => setPage("Resume")}>Add or edit resume details →</button></div></section>{analysis?.rewrite && <RewriteResults data={analysis.rewrite}/>}</div>}
        {page === "Career" && <div className="single-column"><section className="card"><div className="card-title"><span className="title-icon">↗</span><div><h2>Career roadmap</h2><p>Prioritized learning steps based on your skill gaps.</p></div></div>{analysis?.roadmap ? <div className="roadmap-list">{(analysis.roadmap.tasks || []).map((t:any,i:number)=><div className="roadmap-step" key={i}><span>{i+1}</span><div><b>{t.title || t.name}</b><small>{t.description || "Practice and apply this skill in a project."}</small></div><em>{t.estimated_hours ? `${t.estimated_hours} hrs` : `Week ${t.week || i+1}`}</em></div>)}</div> : <EmptyState icon="⌁" title="Your roadmap starts with an analysis" text="Run a full AI report from the Resume section to generate a personalized learning path." action="Go to resume" onClick={() => setPage("Resume")}/>}</section>{analysis?.career && <CareerRecommendations data={analysis.career}/> }</div>}
        {page === "Interview" && <div className="single-column"><section className="card"><div className="card-title"><span className="title-icon">◉</span><div><h2>Interview preparation</h2><p>Practice questions and guidance tailored to your target role.</p></div></div>{analysis?.interview ? <InterviewPreparation data={analysis.interview}/> : <EmptyState icon="◉" title="Prepare for your next interview" text="Run a full AI report to generate role-specific interview questions and preparation tips." action="Generate AI report" onClick={() => setPage("Resume")}/>}</section></div>}
        {page === "Documents" && <div className="single-column"><section className="card"><div className="card-title"><span className="title-icon">▧</span><div><h2>Career documents</h2><p>Keep your resume and generated career materials together.</p></div></div><div className="document-tile"><span className="doc-icon">PDF</span><div><b>{resumeName || "Your resume"}</b><small>{resumeText ? `${resumeText.length.toLocaleString()} characters parsed` : "No resume uploaded yet"}</small></div><button className="text-button" onClick={() => setPage("Resume")}>{resumeText ? "View / edit" : "Upload"} →</button></div>{analysis?.rewrite && <div className="document-tile"><span className="doc-icon purple">AI</span><div><b>Optimized resume content</b><small>Generated for {preview?.job.job_info.title || role}</small></div><button className="text-button" onClick={() => setPage("Rewrite")}>View →</button></div>}</section></div>}
        {busy && <div className="busy-bar"><span/>{busyLabel || "Working on your request…"}</div>}
        <footer className="footer"><span>© 2026 HireMate</span><span>Built to help you move forward <b>✦</b></span><span className={apiOnline ? "footer-online" : ""}>● {apiOnline ? "Services operational" : "API disconnected"}</span></footer>
      </div>
    </main>
  </div>;
}
function FullReport({data}:{data:FullAnalysis}) {
  const sections: Array<[string,string]> = [
    ["review", "AI resume review"], ["recommendations", "Actionable recommendations"],
    ["roadmap", "Personalized learning roadmap"], ["career", "Career recommendations"],
    ["hireability", "Hireability assessment"], ["projects", "Recommended projects"],
    ["career_coach", "Career coaching"], ["company_matches", "Company matches"],
    ["certifications", "Recommended certifications"], ["personalization", "Personalized insights"],
    ["interview", "Interview preparation"], ["cover_letter", "Generated cover letter"],
    ["rewrite", "Optimized resume rewrite"],
  ];
  const available = sections.filter(([key]) => data[key] !== undefined && data[key] !== null);
  return <section className="card full-report"><div className="section-head"><div><h2>Your full AI report</h2><p>{available.length} report sections generated from your resume and target job description.</p></div><span className="report-status">AI report ready</span></div>{available.length ? available.map(([key,title]) => <ReportSection key={key} title={title} value={data[key]}/>) : <p className="muted-note">The API returned no report sections. Check the backend logs and Groq configuration.</p>}</section>;
}
function ReportSection({title,value}:{title:string;value:any}) {
  const [open,setOpen] = useState(true);
  return <section className="report-section"><button className="report-toggle" onClick={() => setOpen(!open)} aria-expanded={open}><b>{title}</b><span>{open ? "−" : "+"}</span></button>{open && <div className="report-content">{title === "Hireability assessment" ? <HireabilityAssessment data={value}/> : title === "Company matches" ? <CompanyMatches data={value}/> : title === "Recommended certifications" ? <CertificationCards data={value}/> : title === "Personalized learning roadmap" ? <RoadmapCards data={value}/> : title === "Recommended projects" ? <ProjectCards data={value}/> : <ReportValue value={value}/>}</div>}</section>;
}
function CompanyMatches({data}:{data:any}) {
  const items = Array.isArray(data) ? data : [];
  if (!items.length) return <div className="section-empty"><h3>No company profiles available</h3><p>HireMate could not load its company skill profiles. Check the company profile data source.</p></div>;
  return <div className="company-match-grid">{items.map((item:any,index:number)=>{
    const matched:string[] = Array.isArray(item.matched_skills) ? item.matched_skills : [];
    const missing:string[] = Array.isArray(item.missing_skills) ? item.missing_skills : [];
    const required:string[] = Array.isArray(item.required_skills) ? item.required_skills : [];
    const score = Math.max(0,Math.min(100,Number(item.skill_match)||0));
    return <article className="company-match-card" key={`${item.company || "company"}-${index}`}>
      <div className="company-match-heading"><div><span className="company-match-eyebrow">COMPANY PROFILE</span><h3>{item.company || "Company"}</h3><span className={`company-match-status ${score>=80?"high":score>=60?"medium":"low"}`}>{item.recommendation || "Profile compatibility estimate"}</span></div><div className="company-match-score"><strong>{item.overall_match ?? 0}%</strong><small>Overall match</small></div></div>
      <div className="company-match-metrics"><div><b>{item.skill_match ?? 0}%</b><span>Skill match</span></div><div><b>{item.ats_match ?? 0}%</b><span>ATS match</span></div><div><b>{item.hireability_match ?? 0}%</b><span>Hireability</span></div></div>
      <div className="company-match-progress"><div><span>Required profile skills covered</span><b>{matched.length}/{required.length || matched.length+missing.length}</b></div><div className="company-match-track"><i style={{width:`${score}%`}}/></div></div>
      <div className="company-match-skill-columns">
        <div><h4><span className="skill-dot good"/>Matched skills <small>{matched.length}</small></h4>{matched.length ? <div className="hireability-chips">{matched.map((skill:string)=><span className="hireability-chip matched" key={skill}>✓ {skill}</span>)}</div> : <p className="muted-note">No required skills from this profile were found in your resume.</p>}</div>
        <div><h4><span className="skill-dot gap"/>Skills to develop <small>{missing.length}</small></h4>{missing.length ? <div className="hireability-chips">{missing.map((skill:string)=><span className="hireability-chip missing" key={skill}>＋ {skill}</span>)}</div> : <p className="muted-note">All listed profile skills are covered.</p>}</div>
      </div>
      {required.length>0 && <details className="company-requirements"><summary>View all profile requirements ({required.length})</summary><div className="hireability-chips">{required.map((skill:string)=>{const isMatched=matched.some(value=>value.toLowerCase()===skill.toLowerCase());return <span className={`hireability-chip ${isMatched?"matched":"missing"}`} key={skill}>{isMatched?"✓":"＋"} {skill}</span>;})}</div></details>}
      <p className="company-match-advice">{item.recommendation_details || (missing.length ? `Focus on ${missing.slice(0,4).join(", ")} to improve your alignment with this company profile.` : "Your resume covers this profile's listed skills. Prepare project examples that demonstrate your experience.")}</p>
    </article>;
  })}</div>;
}

function CertificationCards({data}:{data:any}) {
  const items = Array.isArray(data) ? data : [];
  if (!items.length) return <div className="section-empty"><h3>No certification suggestions available</h3><p>Add a target role or job description to receive certifications related to the skills you want to develop.</p></div>;
  return <div className="certification-grid">{items.map((item:any,index:number)=>{
    const covered:string[] = Array.isArray(item.skills_covered) ? item.skills_covered : [];
    const companies:string[] = Array.isArray(item.target_companies) ? item.target_companies : [];
    return <article className="certification-card" key={`${item.name||"certification"}-${index}`}><div className="certification-top"><span className="certification-icon">✦</span><span className="certification-priority">{item.priority || "Suggested"} priority</span></div><h3>{item.name || "Recommended certification"}</h3><p className="certification-provider">{item.provider || "Provider not specified"}</p><p className="certification-description">{item.description || "Build practical skills relevant to your target role."}</p><div className="certification-facts"><div><small>Difficulty</small><b>{item.difficulty || "Not specified"}</b></div><div><small>Estimated duration</small><b>{item.estimated_duration || "Self-paced"}</b></div><div><small>Potential score gain</small><b>+{item.expected_score_gain ?? 0}</b></div></div><div className="certification-meta"><b>Skills covered</b>{covered.length ? <div className="hireability-chips">{covered.map(skill=><span className="hireability-chip neutral" key={skill}>{skill}</span>)}</div> : <p className="muted-note">Related skills are described above.</p>}</div><div className="certification-meta"><b>Relevant companies</b>{companies.length ? <div className="hireability-chips">{companies.map(company=><span className="hireability-chip neutral" key={company}>{company}</span>)}</div> : <p className="muted-note">Useful across employers hiring for this skill area.</p>}</div></article>;
  })}</div>;
}


function RoadmapCards({data}:{data:any}) {
  const tasks = Array.isArray(data?.tasks) ? data.tasks : [];
  const duration = Number(data?.duration_weeks) || Math.max(1, ...tasks.map((task:any)=>Number(task.week)||1));
  if (!tasks.length) return <div className="section-empty"><h3>Your learning plan is being prepared</h3><p>Run the full report with a resume and target role to generate practical weekly learning tasks.</p></div>;
  const weeks = Array.from(new Set(tasks.map((task:any,index:number)=>Number(task.week)||index+1))).sort((a,b)=>a-b);
  return <div className="roadmap-report"><div className="roadmap-overview"><div><span>PLAN LENGTH</span><strong>{duration} {duration===1?"week":"weeks"}</strong></div><div><span>LEARNING TASKS</span><strong>{tasks.length}</strong></div><div><span>ESTIMATED EFFORT</span><strong>{tasks.reduce((sum:number,task:any)=>sum+(Number(task.estimated_hours)||0),0)} hrs</strong></div></div><div className="roadmap-timeline">{weeks.map((week:number)=>{const weekly=tasks.filter((task:any,index:number)=>(Number(task.week)||index+1)===week);return <section className="roadmap-week" key={week}><div className="roadmap-week-marker"><span>{week}</span><small>WEEK</small></div><div className="roadmap-week-content"><h3>Week {week}</h3><div className="roadmap-task-list">{weekly.map((task:any,index:number)=><article className="roadmap-task" key={`${task.title||task.name||"task"}-${index}`}><div className="roadmap-task-check">✓</div><div className="roadmap-task-copy"><h4>{task.title||task.name||`Learning task ${index+1}`}</h4><p>{task.description||"Practice this topic and apply it in a small hands-on exercise."}</p></div><span className="roadmap-hours">{Number(task.estimated_hours)||6} hrs</span></article>)}</div></div></section>})}</div></div>;
}

function ProjectCards({data}:{data:any}) {
  const items = Array.isArray(data) ? data : data && typeof data === "object" ? Object.values(data) : [];
  if (!items.length) return <div className="section-empty"><h3>No project ideas available yet</h3><p>Add a target role or complete your resume analysis to receive portfolio projects tailored to your skills and career direction.</p></div>;
  return <div className="project-recommendation-grid">{items.map((item:any,index:number)=>{
    const technologies:string[] = Array.isArray(item.technologies) ? item.technologies : [];
    const covered:string[] = Array.isArray(item.skills_covered) ? item.skills_covered : [];
    const skills = Array.from(new Set([...technologies,...covered]));
    return <article className="project-recommendation-card" key={`${item.title||"project"}-${index}`}><div className="project-card-top"><span className="project-card-icon">{index+1}</span><span className={`project-priority ${(item.priority||"medium").toLowerCase()}`}>{item.priority||"Suggested"} priority</span></div><h3>{item.title||"Portfolio project"}</h3><p className="project-card-description">{item.description||"Build a practical project that demonstrates skills relevant to your target role."}</p><div className="project-card-facts"><div><small>Difficulty</small><b>{item.difficulty||"Intermediate"}</b></div><div><small>Estimated duration</small><b>{item.estimated_duration||"2–3 weeks"}</b></div><div><small>Potential score gain</small><b>+{item.expected_score_gain??0}</b></div></div><div className="project-card-skills"><h4>Technologies & skills</h4>{skills.length?<div className="project-skill-chips">{skills.map(skill=><span key={skill}>{skill}</span>)}</div>:<p className="muted-note">Use the technologies listed in your learning plan.</p>}</div></article>;
  })}</div>;
}

function HireabilityAssessment({data}:{data:any}) {
  const matched:string[] = Array.isArray(data.matched_skills) ? data.matched_skills : [];
  const missing:string[] = Array.isArray(data.missing_skills) ? data.missing_skills : [];
  const candidate:string[] = Array.isArray(data.candidate_skills) ? data.candidate_skills : [];
  const required:string[] = Array.isArray(data.required_skills) ? data.required_skills : [];
  const breakdown = data.assessment_breakdown && typeof data.assessment_breakdown === "object" ? Object.entries(data.assessment_breakdown) : [];
  const actions:string[] = Array.isArray(data.next_actions) ? data.next_actions : [];
  const strengths:string[] = Array.isArray(data.strengths) ? data.strengths : [];
  const weaknesses:string[] = Array.isArray(data.weaknesses) ? data.weaknesses : [];
  return <div className="hireability-report">
    <div className="hireability-summary"><div><small>Hireability score</small><strong>{data.overall ?? 0}%</strong><span>Grade {data.grade || "—"}</span></div><div className="hireability-skill-score"><small>Required skill match</small><strong>{data.skill_match_percentage === null || data.skill_match_percentage === undefined ? "—" : `${data.skill_match_percentage}%`}</strong><span>{data.skill_match_status || "No skill comparison available"}</span></div></div>
    {required.length > 0 ? <>
      <h4>Required skills matched <span className="hireability-count">{matched.length}/{required.length}</span></h4>
      {matched.length ? <div className="hireability-chips">{matched.map(skill=><span className="hireability-chip matched" key={skill}>✓ {skill}</span>)}</div> : <p className="muted-note">None of the detected resume skills match the listed job requirements yet.</p>}
      <h4>Missing skills — what you need to learn <span className="hireability-count">{missing.length}</span></h4>
      {missing.length ? <div className="hireability-chips">{missing.map(skill=><span className="hireability-chip missing" key={skill}>＋ {skill}</span>)}</div> : <p className="muted-note">All detected job-description skills are present in your resume.</p>}
      <h4>All required skills</h4><div className="hireability-chips">{required.map(skill=><span className={`hireability-chip ${matched.includes(skill) ? "matched" : "missing"}`} key={skill}>{matched.includes(skill) ? "✓" : "＋"} {skill}</span>)}</div>
    </> : <div className="hireability-no-jd"><h4>Skill comparison not available yet</h4><p className="muted-note">No target job-description skills were detected, so HireMate cannot honestly label any skill as matched or missing. Add the full job description to see an exact comparison.</p></div>}
    <h4>Your detected skills <span className="hireability-count">{candidate.length}</span></h4>
    {candidate.length ? <div className="hireability-chips">{candidate.map(skill=><span className="hireability-chip neutral" key={skill}>{skill}</span>)}</div> : <p className="muted-note">No resume skills were detected.</p>}
    <h4>Hireability breakdown</h4><div className="hireability-breakdown">{breakdown.map(([label,raw])=>{const value=Number(raw)||0;return <div className="hireability-metric" key={String(label)}><div><span>{String(label)}</span><b>{value}%</b></div><div className="hireability-track"><i style={{width:`${Math.max(0,Math.min(100,value))}%`}}/></div></div>})}</div>
    {strengths.length>0 && <><h4>What you are doing well</h4><ul className="hireability-list">{strengths.map((item,i)=><li key={i}>{item}</li>)}</ul></>}
    {weaknesses.length>0 && <><h4>Areas to improve</h4><ul className="hireability-list">{weaknesses.map((item,i)=><li key={i}>{item}</li>)}</ul></>}
    {actions.length>0 && <><h4>Your next steps</h4><ol className="hireability-list">{actions.map((item,i)=><li key={i}>{item}</li>)}</ol></>}
  </div>;
}

function ReportValue({value}:{value:any}) {
  if (value === null || value === undefined) return <p className="muted-note">Not available.</p>;
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") return <p className="report-text">{String(value)}</p>;
  if (Array.isArray(value)) return value.length ? <ul className="report-list">{value.map((item:any,index:number) => <li key={index}><ReportValue value={item}/></li>)}</ul> : <p className="muted-note">No items returned.</p>;
  if (typeof value === "object") return <div className="report-fields">{Object.entries(value).map(([key,item]) => <div className="report-field" key={key}><b>{key.replace(/_/g," ")}</b><ReportValue value={item}/></div>)}</div>;
  return <p className="report-text">{String(value)}</p>;
}
function Metric({label,value}:{label:string;value:string|number}) { return <div className="metric"><strong>{value}</strong><span>{label}</span></div>; }
function EmptyState({icon,title,text,action,onClick}:{icon:string;title:string;text:string;action:string;onClick:()=>void}) { return <div className="empty-state"><span>{icon}</span><h3>{title}</h3><p>{text}</p><button className="outline-button" onClick={onClick}>{action} →</button></div>; }
function RewriteResults({data}:{data:any}) { const skills = Array.isArray(data.skills) ? data.skills : []; return <section className="card rewrite-output"><div className="section-head"><div><h2>Optimized resume content</h2><p>Review every section before using it in your resume.</p></div><button className="secondary-button" onClick={() => navigator.clipboard?.writeText([data.professional_summary,data.experience,...(data.projects||[]).map((p:any)=>p.description)].filter(Boolean).join("\n\n"))}>Copy content</button></div><h3>Professional summary</h3><p>{data.professional_summary}</p><h3>Experience</h3><p className="preserve-lines">{data.experience}</p>{(data.projects||[]).length>0 && <><h3>Projects</h3>{data.projects.map((p:any,i:number)=><div className="project-output" key={i}><b>{p.name}</b><p>{p.description}</p>{(p.bullets||[]).map((b:string,j:number)=><p key={j}>• {b}</p>)}</div>)}</>}{skills.length>0 && <><h3>Optimized skills</h3><div className="optimized-skills">{skills.map((group:any,i:number)=><div className="skill-group" key={i}><b>{group.category}</b><div>{(group.items||[]).map((s:string)=><span className="chip" key={s}>{s}</span>)}</div></div>)}</div></>}<h3>ATS improvement suggestions</h3><p>{data.ats_improvement}</p>{(data.suggestions||[]).map((s:string,i:number)=><div className="suggestion" key={i}>✓ {s}</div>)}</section>; }
function asItems(value:any): string[] { if (Array.isArray(value)) return value.map(v => typeof v === "string" ? v : v?.title || v?.name || JSON.stringify(v)); if (typeof value === "string" && value.trim()) return [value]; return []; }
function CareerRecommendations({data}:{data:any}) {
  const strengths=asItems(data.strengths), improvements=asItems(data.improvement_areas || data.improvementAreas), steps=asItems(data.next_steps || data.nextSteps), projects=asItems(data.recommended_projects || data.recommendedProjects), certs=asItems(data.recommended_certifications || data.recommendedCertifications);
  const score=Number(data.readiness_score ?? data.readinessScore);
  const groups=[{title:"Your strengths",items:strengths,icon:"✓",tone:"good"},{title:"Areas to improve",items:improvements,icon:"↗",tone:"focus"},{title:"Your next steps",items:steps,icon:"→",tone:"action"},{title:"Recommended projects",items:projects,icon:"⌘",tone:"project"},{title:"Recommended certifications",items:certs,icon:"✦",tone:"cert"}];
  return <section className="card career-recommendations"><div className="career-head"><div><h2>Career recommendations</h2><p>{data.summary || "A practical plan to strengthen your profile and move toward your target role."}</p></div>{Number.isFinite(score) && <div className="career-score"><strong>{score}%</strong><span>Readiness</span></div>}</div><div className="career-meta">{(data.stage || data.confidence || data.estimated_duration) && <>{data.stage && <span><small>Career stage</small><b>{data.stage}</b></span>}{data.confidence && <span><small>Confidence</small><b>{data.confidence}</b></span>}{data.estimated_duration && <span><small>Estimated plan</small><b>{data.estimated_duration}</b></span>}</>}</div><div className="career-groups">{groups.map(group=><section className="career-group" key={group.title}><h3><span className={`career-group-icon ${group.tone}`}>{group.icon}</span>{group.title}<em>{group.items.length}</em></h3>{group.items.length ? <ul>{group.items.map((item,i)=><li key={i}>{item}</li>)}</ul> : <p className="muted-note">No recommendations available for this section yet.</p>}</section>)}</div></section>;
}
function InterviewPreparation({data}:{data:any}) {
  const questions=data.questions && typeof data.questions === "object" ? data.questions : data;
  const tips=asItems(data.overall_tips || data.overallTips);
  const categories=Object.entries(questions || {}).filter(([key,value])=>!(["overall_tips","overallTips"].includes(key)) && (Array.isArray(value) || typeof value === "string"));
  return <section className="card interview-card"><div className="interview-head"><div><h2>Your interview preparation</h2><p>Practice these questions aloud and prepare examples from your own experience.</p></div><span className="interview-count">{categories.reduce((n,[,v])=>n+asItems(v).length,0)} questions</span></div>{categories.length ? <div className="interview-categories">{categories.map(([category,raw],index)=>{const items=asItems(raw);return <section className="interview-category" key={category}><div className="interview-category-head"><span>{String(index+1).padStart(2,"0")}</span><h3>{category.replace(/_/g," ")}</h3><em>{items.length} questions</em></div><ol>{items.map((question,i)=><li key={i}><span>{question}</span></li>)}</ol></section>})}</div> : <p className="muted-note">Interview questions are not available. Run the full AI report again to generate them.</p>}{tips.length>0 && <section className="interview-tips"><h3>Preparation tips</h3><ul>{tips.map((tip,i)=><li key={i}>{tip}</li>)}</ul></section>}</section>;
}
function DataCard({title,data}:{title:string;data:any}) { return <section className="card data-card"><h2>{title}</h2><pre>{JSON.stringify(data,null,2)}</pre></section>; }

export default App;
