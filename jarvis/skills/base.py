"""The Skill contract — the most important file in the project.

Every capability JARVIS gains is a Skill. The core never imports a
skill directly; skills register themselves, and the router picks.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class RiskLevel(str, Enum):
    SAFE = "safe"        # read-only: no side effects, runs freely
    CONFIRM = "confirm"  # side effects: JARVIS must ask first (Phase 6)
    BLOCKED = "blocked"  # never auto-runs


@dataclass
class SkillResult:
    ok: bool
    message: str                       # what the user sees
    data: dict = field(default_factory=dict)  # structured data for later phases


class Skill(ABC):
    name = "unnamed"
    description = ""
    examples = []            # example phrases, used by the router in Step 3
    risk_level = RiskLevel.SAFE

    @abstractmethod
    def handle(self, text: str) -> SkillResult:
        """Run the skill on the raw user input."""
