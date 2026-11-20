"""Parse training/course entries and their bullet-point details."""
import re
from models.resume_model import Training

DATE_RE = re.compile(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\s*[-–—]\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})", re.I)

class TrainingParser:
    def parse(self, resume):
        lines = [x.strip() for x in resume.sections.get("training", "").splitlines() if x.strip()]
        items = []
        current = None
        pending_bullet = False
        for source in lines:
            if source.strip() in {"•", "-", "*", "▪", "●"}:
                pending_bullet = True
                continue
            is_bullet = source.startswith(("•", "-", "*", "▪", "●")) or pending_bullet
            line = source.lstrip("•*-▪● ").strip()
            if not line:
                continue
            if current is None:
                match = DATE_RE.search(line)
                date = match.group(1) if match else ""
                heading = line.replace(date, "").strip(" |:-") if date else line
                parts = [x.strip() for x in heading.split("|") if x.strip()]
                current = Training(title=parts[0] if parts else heading, provider=parts[1] if len(parts) > 1 else "", date=date)
            else:
                if is_bullet or not current.bullets:
                    current.bullets.append(line)
                else:
                    current.bullets[-1] += " " + line
            pending_bullet = False
        if current:
            current.bullets = [re.sub(r"\s+", " ", x).strip() for x in current.bullets if x.strip()]
            items.append(current)
        resume.training = items
