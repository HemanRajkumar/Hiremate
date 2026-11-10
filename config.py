import os

from dotenv import load_dotenv

load_dotenv()

# ======================================================
# Application
# ======================================================

APP_NAME = "HireMate"

APP_VERSION = "0.4.0"

# ======================================================
# Supported Upload Types
# ======================================================

SUPPORTED_RESUME_TYPES = [
    "pdf",
]

SUPPORTED_JD_TYPES = [
    "pdf",
    "txt",
]

# ======================================================
# Groq Configuration
# ======================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "openai/gpt-oss-120b"

TEMPERATURE = 0.3

MAX_TOKENS = 2048
