const API_BASE = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

export type PreviewResult = {
  resume: { personal_info: { name: string; email: string; phone: string }; skills: string[]; projects?: unknown[]; education?: unknown[] };
  job: { job_info: { title: string }; skills: string[] };
  ats: { overall_score: number; skills_score: number; matched_skills: string[]; missing_skills: string[] };
  skill_gap: { overall_score: number; high_priority: Array<{ skill: string; priority: string; reason?: string }>; medium_priority: Array<{ skill: string; priority: string; reason?: string }>; low_priority: Array<{ skill: string; priority: string; reason?: string }> };
};

export type FullAnalysis = Record<string, any>;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(data.detail)
      ? data.detail.map((item: any) => item.msg || JSON.stringify(item)).join("; ")
      : data.detail;
    throw new Error(typeof detail === "string" ? detail : `Request failed (${response.status})`);
  }
  return data as T;
}

export const getHealth = () => request<{ status: string; service: string; version: string; ai_configured?: boolean }>("/api/health");
export const previewAnalysis = (resumeText: string, jobDescription: string) => request<PreviewResult>("/api/analysis/preview", {
  method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
});
export const fullAnalysis = (resumeText: string, jobDescription: string) => request<FullAnalysis>("/api/analysis/full", {
  method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
});
export async function extractResumePdf(file: File): Promise<{ text: string; resume: any }> {
  const form = new FormData(); form.append("file", file);
  const data = await request<{ extracted_text: string; resume: any }>("/api/resumes/parse", { method: "POST", body: form });
  return { text: data.extracted_text, resume: data.resume };
}

export const generateRewrite = (resumeText: string, jobDescription: string) => request<{ rewrite: any }>("/api/analysis/rewrite", {
  method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
});
