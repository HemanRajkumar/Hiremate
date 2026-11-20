import os

from dotenv import load_dotenv
from groq import Groq

from config import GROQ_MODEL, MAX_TOKENS, TEMPERATURE

load_dotenv()


class GroqService:
    """
    Generic wrapper around the Groq Chat API.
    """

    def __init__(self):
        # Read the key at runtime rather than relying on a value captured when
        # config.py was first imported. This also supports environment injection
        # by Docker, IDEs, and deployment platforms.
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is missing. Add a valid Groq API key to the project-root .env file or backend environment."
            )

        self.client = Groq(
            api_key=api_key,
            timeout=60.0,
            max_retries=2,
        )

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int | None = None,
    ) -> str:
        """
        Send a chat request to Groq.
        """

        try:
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                temperature=TEMPERATURE,
                max_tokens=max_tokens or MAX_TOKENS,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )

            content = response.choices[0].message.content
            if not content or not content.strip():
                raise RuntimeError("Groq returned an empty response. Try again or reduce the input size.")
            return content.strip()

        except Exception as error:
            print("\n========== GROQ ERROR ==========")
            print("Error type:", type(error).__name__)
            print("Error:", error)
            print("Model:", GROQ_MODEL)
            print("Temperature:", TEMPERATURE)
            print("Max tokens:", MAX_TOKENS)
            print("System prompt length:", len(system_prompt))
            print("User prompt length:", len(user_prompt))
            print("================================\n")

            raise