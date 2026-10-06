from jarvis.core.llm import LLMClient
from jarvis.core.tools import build_tools
from jarvis.skills import REGISTRY, discover_skills

LLM_CONFIDENCE = 0.95

def llm_route(text, threshold=0.6):
    """Route via LLM tool calling. Returns (skill_cls, confidence)."""
    discover_skills()
    client = LLMClient(model="openai/gpt-oss-20b")  # from config when we wire into assistant.py
    calls = client.choose_tool([{"role": "user", "content": text}], build_tools())
    if not calls:
        return None, 0.0
    skill_cls = REGISTRY.get(calls[0].function.name)
    if skill_cls is None:
        return None, 0.0
    return skill_cls, LLM_CONFIDENCE
