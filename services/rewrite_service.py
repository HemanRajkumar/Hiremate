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