<<<<<<< HEAD
"""Extract programming languages from the Skills section and spoken languages from Languages."""
import re

class LanguageParser:
    PROGRAMMING_LABELS = {"languages", "programming languages", "coding languages"}

    def parse(self, resume):
        programming = []
        waiting_for_programming_values = False
        skills_text = resume.sections.get("skills", "").replace("\\n", "\n")
        for raw in skills_text.splitlines():
            line = raw.strip().lstrip("•*-▪● ").strip()
            if not line:
                continue
            if ":" in line:
                label, values = line.split(":", 1)
                if label.strip().lower() in self.PROGRAMMING_LABELS:
                    waiting_for_programming_values = True
                    if values.strip():
                        programming.extend(x.strip() for x in values.split(",") if x.strip())
                        waiting_for_programming_values = False
                    continue
                waiting_for_programming_values = False
            elif waiting_for_programming_values:
                programming.extend(x.strip() for x in line.split(",") if x.strip())
                waiting_for_programming_values = False
        resume.programming_languages = list(dict.fromkeys(programming))

        spoken = []
        languages_text = resume.sections.get("languages", "").replace("\\n", "\n")
        for raw in languages_text.splitlines():
            line = raw.strip().lstrip("•*-▪● ").strip()
            if not line:
                continue
            line = re.sub(r"^(?:spoken languages|languages)\s*:\s*", "", line, flags=re.I)
            spoken.extend(x.strip() for x in line.split(",") if x.strip())
        resume.languages = list(dict.fromkeys(spoken))
=======
"""
Language Parser.
"""


class LanguageParser:

    def parse(
        self,
        resume,
    ):

        section = resume.sections.get(
            "languages",
            "",
        )

        if not section:
            return

        for line in section.splitlines():

            line = line.strip()

            if line:

                resume.languages.append(
                    line,
                )
>>>>>>> 0ae423da1a6854376a84145ea976d8dd03502029
