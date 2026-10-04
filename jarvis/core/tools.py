"""LLM tool schemas, generated from the skill registry.

A skill describes itself once (name, description, examples).
Everything — keyword router, semantic router, LLM tools — reads
from the registry. Add a skill, and the LLM can call it with
zero extra wiring.
"""

from jarvis.skills import REGISTRY
  


def skill_to_tool(skill_cls) -> dict:
    """Convert one Skill class into an OpenAI-style function schema."""
    return {
        "type": "function",
        "function": {
            "name": skill_cls.name,
            "description": (
                f"{skill_cls.description} "
                f"Example phrases: {', '.join(skill_cls.examples)}"
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }


def build_tools() -> list[dict]:
    """Build tool schemas for every registered skill."""
    return [skill_to_tool(cls) for cls in REGISTRY.values()]

