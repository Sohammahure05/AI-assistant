"""Time skill: tells the current time and date."""
from datetime import datetime

from jarvis.skills import register
from jarvis.skills.base import RiskLevel, Skill, SkillResult


@register
class TimeSkill(Skill):
    name = "time"
    description = "Tells the current time and date."
    examples = [
        "what time is it",
        "what's the date today",
        "current time",
    ]
    risk_level = RiskLevel.SAFE

    def handle(self, text: str) -> SkillResult:
        now = datetime.now()
        return SkillResult(
            ok=True,
            message=f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}.",
        )
