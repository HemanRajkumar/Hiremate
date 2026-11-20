import re
from typing import List

import pandas as pd


class SkillService:
    """
    Extract technical skills from resume text.
    """

    def __init__(self, csv_path: str = "data/skills.csv"):

        try:
            skills = pd.read_csv(csv_path)

            self.skill_list = skills["skill"].dropna().astype(str).str.lower().tolist()

        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Skills database not found: {csv_path}") from exc

    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from resume text.
        """

        text = text.lower()

        detected = []

        for skill in self.skill_list:

<<<<<<< HEAD
            # Word boundaries fail for symbols such as C++ and C#. Use
            # alphanumeric lookarounds, and prevent the C token matching C++.
            pattern = rf"(?<![a-z0-9_]){re.escape(skill)}(?![a-z0-9_])"
            if skill.lower() == "c":
                pattern += r"(?!\+\+)"
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(skill.upper() if skill.lower() == "c++" else skill.title())
=======
            pattern = rf"\b{re.escape(skill)}\b"

            if re.search(pattern, text):
                detected.append(skill.title())
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029

        return sorted(set(detected))
