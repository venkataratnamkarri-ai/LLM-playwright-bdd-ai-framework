import os
from pathlib import Path
from dotenv import load_dotenv
import cohere

class CohereHelper:
    """Helper service providing unified access to Cohere Command models."""

    def __init__(self):
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
        load_dotenv()
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise RuntimeError("COHERE_API_KEY is missing; set it in .env or the environment.")
        self.client = cohere.ClientV2(api_key=api_key)

    def ask(self, prompt: str, model: str = "command-a-03-2025") -> str:
        response = self.client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return "".join(
            item.text for item in response.message.content
            if getattr(item, "text", None)
        ).strip()
