"""Generate accurate, ATS-friendly resume rewrites."""

import json
import logging
import re
from typing import Any


from models.rewrite_model import RewriteResult
from services.groq_service import GroqService
from utils.prompts import REWRITE_SYSTEM_PROMPT, rewrite_prompt

logger = logging.getLogger(__name__)


class RewriteService:
    """AI resume rewrite service with tolerant response normalization."""
"""
AI Resume Rewrite Service.
"""

import json
import re

import streamlit as st

from models.rewrite_model import RewriteResult
from services.groq_service import GroqService
from utils.prompts import (
    REWRITE_SYSTEM_PROMPT,
    rewrite_prompt,
)


class RewriteService:
    """
    AI Resume Rewrite Service.
    """

    def __init__(self):
        self.groq = GroqService()

    def generate(self, resume_text: str, jd_text: str) -> RewriteResult:
        prompt = rewrite_prompt(resume_text, jd_text)
        try:
            # Resume rewrites contain several sections and structured skill groups;
            # allow more output than the default short analysis requests.
            response = self.groq.chat(REWRITE_SYSTEM_PROMPT, prompt, max_tokens=4096)
            data = self._parse_json_response(response)

            result = RewriteResult(
                professional_summary=self._as_text(data.get("professional_summary")),
                experience=self._as_text(data.get("experience")),
                projects=self._normalize_projects(data.get("projects", [])),
                skills=self._normalize_skills(data.get("skills", [])),
                suggestions=self._normalize_suggestions(data.get("suggestions", [])),
                ats_improvement=self._as_text(data.get("ats_improvement")),
            )

            # Avoid returning a blank-looking workspace if the model omitted fields.
            if not result.professional_summary:
                result.professional_summary = "A tailored summary could not be generated from the supplied resume."
            if not result.experience:
                result.experience = "No employment experience was returned. Keep academic and personal projects in the Projects section."
            if not result.ats_improvement:
                result.ats_improvement = "Review the suggestions below and add evidence for any job requirements not demonstrated in the resume."
            if not result.suggestions:
                result.suggestions = [
                    "Add measurable outcomes only where you can verify them.",
                    "Prioritize the skills and projects most relevant to the target role.",
                    "Include missing job requirements only after gaining and demonstrating those skills.",
                ]
            return result

        except Exception as error:
            logger.exception("Resume rewrite generation failed: %s", error)
            logger.error("The rewrite could not be generated. Check GROQ_API_KEY and the Groq connection.")
            return self._default_result()

    def _parse_json_response(self, response: str) -> dict:
        if not response or not response.strip():
            raise ValueError("AI returned an empty response.")
        cleaned = response.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            start, end = cleaned.find("{"), cleaned.rfind("}")
            if start < 0 or end <= start:
                raise ValueError("AI response did not contain a JSON object.")
            data = json.loads(cleaned[start:end + 1])
        if not isinstance(data, dict):
            raise ValueError("AI response JSON must be an object.")
        return data

    @staticmethod
    def _as_text(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, list):
            return "\n".join(str(item).strip() for item in value if item)
        if isinstance(value, dict):
            return "\n".join(f"{key}: {val}" for key, val in value.items() if val)
        return str(value).strip()

    @classmethod
    def _normalize_projects(cls, value: Any) -> list[dict]:
        if not value:
            return []
        if isinstance(value, str):
            return [{"name": "Projects", "description": value.strip(), "bullets": [], "technologies": []}]
        if isinstance(value, dict):
            value = [value]
        if not isinstance(value, list):
            return []
        projects = []
        for item in value:
            if isinstance(item, str):
                projects.append({"name": "", "description": item.strip(), "bullets": [], "technologies": []})
            elif isinstance(item, dict):
                projects.append({
                    "name": cls._as_text(item.get("name") or item.get("project_name") or item.get("title")),
                    "description": cls._as_text(item.get("description") or item.get("project_description")),
                    "bullets": cls._normalize_suggestions(item.get("bullets", [])),
                    "technologies": cls._normalize_suggestions(item.get("technologies", [])),
                })
        return [p for p in projects if p["name"] or p["description"] or p["bullets"]]

    @classmethod
    def _normalize_skills(cls, value: Any) -> list[dict]:
        """Accept categorized objects and legacy flat string lists."""
        if not value:
            return []
        if isinstance(value, str):
            # Legacy output may contain one category per line ("Tools: Git, VS Code").
            legacy_entries = []
            for line in value.splitlines():
                line = re.sub(r"^\s*[-•*]\s*", "", line).strip()
                if not line:
                    continue
                if ":" in line:
                    category, raw_items = line.split(":", 1)
                    legacy_entries.append({"category": category.strip(), "items": raw_items})
                else:
                    legacy_entries.extend(x.strip() for x in re.split(r"[,;|]", line) if x.strip())
            value = legacy_entries
        if isinstance(value, dict):
            value = [{"category": key, "items": val} for key, val in value.items()]
        if not isinstance(value, list):
            return []

        groups: dict[str, list[str]] = {}
        for entry in value:
            if isinstance(entry, str):
                # Handle older "Category: a, b" formats gracefully.
                if ":" in entry:
                    category, values = entry.split(":", 1)
                    items = re.split(r"[,;|]", values)
                else:
                    category, items = "Relevant Skills", [entry]
            elif isinstance(entry, dict):
                category = cls._as_text(entry.get("category") or entry.get("name") or "Relevant Skills")
                items = entry.get("items") or entry.get("skills") or entry.get("values") or []
            else:
                continue
            category = category.strip() or "Relevant Skills"
            if isinstance(items, str):
                items = re.split(r"[,;|\n]", items)
            if not isinstance(items, list):
                continue
            bucket = groups.setdefault(category, [])
            for skill in items:
                clean = cls._as_text(skill).strip(" •-*\t")
                if clean and clean.casefold() not in {x.casefold() for x in bucket}:
                    bucket.append(clean)
        return [{"category": name, "items": items} for name, items in groups.items() if items]

    @classmethod
    def _normalize_suggestions(cls, value: Any) -> list[str]:
        if not value:
            return []
        if isinstance(value, str):
            value = re.split(r"\n|(?<=[.!?])\s+(?=[A-Z])", value)
        if not isinstance(value, list):
            value = [value]
        return [cls._as_text(item).strip(" •-*\t") for item in value if cls._as_text(item).strip(" •-*\t")]

    def _default_result(self) -> RewriteResult:
        return RewriteResult(
            professional_summary="The AI rewrite is temporarily unavailable. Please retry after checking your API configuration.",
            experience="No rewritten experience is available. Your original employment details have not been changed.",
            projects=[],
            skills=[],
            suggestions=[
                "Check that GROQ_API_KEY is configured in your .env file.",
                "Make sure the uploaded resume contains selectable text.",
                "Try again with a clear job description for better targeting.",
            ],
            ats_improvement="No ATS analysis was generated because the rewrite request failed.",
        )
    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        resume_text: str,
        jd_text: str,
    ) -> RewriteResult:
        """
        Generate an ATS-optimized resume rewrite.
        """

        prompt = rewrite_prompt(
            resume_text,
            jd_text,
        )

        try:
            response = self.groq.chat(
                REWRITE_SYSTEM_PROMPT,
                prompt,
            )

            # ---------------------------------------------
            # Parse AI response safely
            # ---------------------------------------------
            data = self._parse_json_response(response)

            # ---------------------------------------------
            # Build RewriteResult
            # ---------------------------------------------
            result = RewriteResult()

            result.professional_summary = data.get(
                "professional_summary",
                "",
            )

            result.experience = data.get(
                "experience",
                "",
            )

            result.projects = data.get(
                "projects",
                "",
            )

            result.skills = data.get(
                "skills",
                "",
            )

            result.suggestions = data.get(
                "suggestions",
                [],
            )

            result.ats_improvement = data.get(
                "ats_improvement",
                "",
            )

            return result

        except Exception as error:
            st.error(
                "Resume Rewrite generation failed."
            )

            st.exception(error)

            return self._default_result()

    # =====================================================
    # JSON Parser
    # =====================================================

    def _parse_json_response(
        self,
        response: str,
    ) -> dict:
        """
        Safely extract and parse JSON from an AI response.

        Handles:
        - Normal JSON
        - Markdown ```json blocks
        - Extra text before/after JSON
        """

        if not response:
            raise ValueError(
                "AI returned an empty response."
            )

        cleaned = response.strip()

        # ---------------------------------------------
        # Remove Markdown code fences
        # ---------------------------------------------
        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        cleaned = cleaned.strip()

        # ---------------------------------------------
        # Try direct JSON parsing first
        # ---------------------------------------------
        try:
            data = json.loads(cleaned)

            if not isinstance(data, dict):
                raise ValueError(
                    "AI response JSON is not an object."
                )

            return data

        except json.JSONDecodeError:
            pass

        # ---------------------------------------------
        # Extract JSON object from surrounding text
        # ---------------------------------------------
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "AI response does not contain a valid JSON object."
            )

        json_text = cleaned[start:end + 1]

        try:
            data = json.loads(json_text)

        except json.JSONDecodeError as error:
            raise ValueError(
                "AI returned malformed JSON."
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                "AI response JSON is not an object."
            )

        return data

    # =====================================================
    # Default Result
    # =====================================================

    def _default_result(self) -> RewriteResult:
        """
        Return a fallback response.
        """

        result = RewriteResult()

        result.professional_summary = (
            "Unable to generate an optimized "
            "professional summary."
        )

        result.experience = (
            "Unable to rewrite the experience section."
        )

        result.projects = (
            "Unable to rewrite the projects section."
        )

        result.skills = (
            "Unable to optimize the skills section."
        )

        result.suggestions = [
            "Use action verbs.",
            "Quantify achievements where possible.",
            "Align keywords with the job description.",
        ]

        result.ats_improvement = (
            "Review your resume manually and add "
            "relevant keywords from the job description."
        )

        return result
