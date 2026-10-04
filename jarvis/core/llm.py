"""Thin LLM client: the ONLY place that talks to Groq.

Everything else uses chat() — switching providers later means
rewriting this file, nothing else.
"""
import logging
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # dev convenience: loads .env into os.environ (harmless if absent)

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are JARVIS, a precise personal AI assistant.
Answer concisely. When asked to pick something, pick exactly one
and explain your choice briefly."""


class LLMClient:
    def __init__(self, model: str, api_key: str | None = None) -> None:
        key = api_key or os.environ.get("GROQ_API_KEY")
        if not key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Put it in your .env file "
                "and restart."
            )
        self._client = Groq(api_key=key)
        self.model = model
        log.info("LLM client ready (model=%s)", model)

    def chat(self, messages: list[dict], **kwargs) -> str:
        """Send messages, get the assistant's reply text back."""
        resp = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],
            **kwargs,
        )
        return resp.choices[0].message.content
