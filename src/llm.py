"""Cliente Groq (sin LangChain)."""

from __future__ import annotations

from groq import Groq

from src import config


class GroqLLM:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        key = api_key or config.GROQ_API_KEY
        if not key:
            raise ValueError(
                "Falta GROQ_API_KEY. Configurala en .env o pasá api_key=..."
            )
        self.model = model or config.GROQ_MODEL
        self.client = Groq(api_key=key)

    def chat(self, system: str, user: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        choice = completion.choices[0]
        content = choice.message.content
        return (content or "").strip()
