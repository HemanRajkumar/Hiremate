"""
AI Interview Preparation Service.
"""

import json
import re

from models.interview_model import InterviewResult
from services.groq_service import GroqService
from utils.interview_prompt import (
    INTERVIEW_SYSTEM_PROMPT,
    interview_prompt,
)


class InterviewService:
    """
    Generate AI interview questions.
    """

    def __init__(self):
        self.groq = GroqService()

    # =====================================================
    # JSON Extraction
    # =====================================================

    def _extract_json(self, response: str) -> dict:
        """
        Extract JSON object from an AI response.

        Handles:
        - Normal JSON
        - ```json ... ``` blocks
        - Extra text surrounding the JSON
        """

        if not response:
            raise ValueError(
                "AI returned an empty response."
            )

        cleaned = response.strip()

        # Remove markdown code fences
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

        # Try normal JSON first
        try:
            data = json.loads(cleaned)

            if not isinstance(data, dict):
                raise ValueError(
                    "AI response is not a JSON object."
                )

            return data

        except json.JSONDecodeError:
            pass

        # Find JSON object inside surrounding text
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "No valid JSON object found in AI response."
            )

        json_text = cleaned[start:end + 1]

        data = json.loads(json_text)

        if not isinstance(data, dict):
            raise ValueError(
                "Extracted response is not a JSON object."
            )

        return data

    # =====================================================
    # Generate Interview
    # =====================================================

    def generate(
        self,
        resume_data,
        jd_text: str,
    ) -> InterviewResult:
        """
        Generate personalized interview questions.
        """

        prompt = interview_prompt(
            resume_data,
            jd_text,
        )

        result = InterviewResult()

        try:
            response = self.groq.chat(
                INTERVIEW_SYSTEM_PROMPT,
                prompt,
            )

            print(
                "\n========== GROQ RESPONSE =========="
            )
            print(response)
            print(
                "===================================\n"
            )

            data = self._extract_json(response)

            result.questions = data.get(
                "questions",
                {},
            )

            result.overall_tips = data.get(
                "overall_tips",
                [],
            )

            return result

        except Exception as error:
            print(
                "\n========== INTERVIEW ERROR =========="
            )
            print(
                "Error type:",
                type(error).__name__,
            )
            print(
                "Error:",
                error,
            )
            print(
                "======================================\n"
            )

            result.questions = {
                "AI Response": [
                    "Unable to generate interview questions."
                ]
            }

            result.overall_tips = [
                "Please try generating interview questions again."
            ]

            return result