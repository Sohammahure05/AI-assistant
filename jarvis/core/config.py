"""Config loading with safe defaults (works even without config.yaml)."""
import copy
import logging
from pathlib import Path

log = logging.getLogger(__name__)

DEFAULTS = {
    "assistant": {"name": "JARVIS", "version": "0.1.0"},
    "logging": {"level": "INFO"},
    "router": {"confidence_threshold": 0.6},
}



def _deep_update(base: dict, override: dict) -> dict:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = value
    return base


def load_config(path: str = "config.yaml") -> dict:
    config = copy.deepcopy(DEFAULTS)
    p = Path(path)
    if p.exists():
        import yaml
        with p.open(encoding="utf-8") as f:
            _deep_update(config, yaml.safe_load(f) or {})
        log.info("Loaded config from %s", p)
    else:
        log.warning("No config file at %s — using defaults.", p)
    return config
