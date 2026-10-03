"""Deterministic keyword router (v1).

Scores each skill by token overlap between the input and the skill's
name + examples. Returns the best skill and its confidence.
Phase 2 will add an LLM router behind the same interface.
"""
import logging
import re

from jarvis.skills import REGISTRY
from jarvis.skills.base import Skill

log = logging.getLogger(__name__)


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _skill_tokens(skill: Skill) -> set[str]:
    tokens = _tokens(skill.name)
    for example in skill.examples:
        tokens |= _tokens(example)
    return tokens


def route(text: str, threshold: float = 0.6) -> tuple[Skill | None, float]:
    """Return (best_skill, confidence); (None, 0.0) if nothing qualifies."""
    input_tokens = _tokens(text)
    if not input_tokens:
        return None, 0.0

    best_skill, best_score = None, 0.0
    for skill in REGISTRY.values():
        skill_tokens = _skill_tokens(skill)
        if not skill_tokens:
            continue
        score = len(input_tokens & skill_tokens) / len(input_tokens)
        log.debug("router: skill=%s score=%.2f", skill.name, score)
        if score > best_score:
            best_skill, best_score = skill, score

    if best_skill is not None and best_score >= threshold:
        return best_skill, best_score
    return None, 0.0
