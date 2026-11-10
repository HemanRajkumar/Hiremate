from groq import Groq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
)


class GroqService:
    """
    Generic wrapper around the Groq Chat API.
    """

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found in .env"
            )

        self.client = Groq(
            api_key=GROQ_API_KEY,
            timeout=60.0,
            max_retries=2,
        )

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Send a chat request to Groq.
        """

        try:
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
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

            return response.choices[0].message.content

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