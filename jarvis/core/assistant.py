"""The assistant shell. Later phases plug the router, skills,
memory, and voice into this — the entry point never changes."""
import logging

from jarvis.core.config import load_config
from jarvis.core.logger import setup_logging

log = logging.getLogger(__name__)


class Assistant:
    def __init__(self, config_path: str = "config.yaml") -> None:
        self.config = load_config(config_path)
        setup_logging(self.config["logging"]["level"])
        self.name = self.config["assistant"]["name"]
        log.info("%s initialised.", self.name)

    def greet(self) -> None:
        print(f"{self.name}: At your service.")
