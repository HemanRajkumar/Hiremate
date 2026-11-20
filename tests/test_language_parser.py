from types import SimpleNamespace
from services.parsers.language_parser import LanguageParser


def test_programming_languages_are_read_from_skills_section():
    resume = SimpleNamespace(sections={
        "skills": "Languages: C, C++, Python, Java, SQL\\nLibraries/Frameworks: NumPy, Pandas\\n",
        "languages": "",
    })
    LanguageParser().parse(resume)
    assert resume.programming_languages == ["C", "C++", "Python", "Java", "SQL"]
    assert resume.languages == []


def test_spoken_languages_remain_separate():
    resume = SimpleNamespace(sections={
        "skills": "Languages: Python, Java\\n",
        "languages": "English, Hindi\\n",
    })
    LanguageParser().parse(resume)
    assert resume.programming_languages == ["Python", "Java"]
    assert resume.languages == ["English", "Hindi"]
