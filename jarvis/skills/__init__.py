"""Skill registry: the router looks skills up here, never by direct import."""
from jarvis.skills.base import Skill

REGISTRY: dict[str, Skill] = {}


def register(skill_cls):
    """Class decorator: instantiate a Skill subclass and register it by name."""
    instance = skill_cls()
    if instance.name in REGISTRY:
        raise ValueError(f"Duplicate skill name: {instance.name!r}")
    REGISTRY[instance.name] = instance
    return skill_cls


import importlib
import pkgutil


def discover_skills() -> None:
    """Import every skill module in this package, so @register runs for each."""
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name == "base":
            continue  # base holds the contract, not a skill
        importlib.import_module(f"{__name__}.{module_info.name}")
