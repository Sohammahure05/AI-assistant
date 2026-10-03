"""The assistant shell. Later phases plug the router, skills,
memory, and voice into this — the entry point never changes."""
import logging

from jarvis.core.config import load_config
from jarvis.core.logger import setup_logging
from jarvis.skills import REGISTRY, discover_skills

log = logging.getLogger(__name__)

EXIT_WORDS = {"exit", "quit", "bye"}


class Assistant:
    def __init__(self, config_path: str = "config.yaml") -> None:
        self.config = load_config(config_path)
        setup_logging(self.config["logging"]["level"])
        self.name = self.config["assistant"]["name"]
        discover_skills()
        log.info("Discovered skills: %s", sorted(REGISTRY))
        log.info("%s initialised.", self.name)

    def greet(self) -> None:
        print(f"{self.name}: At your service.")

    def run(self) -> None:
        """Read-Eval-Print Loop: read input, (soon: route it), print result."""
        self.greet()
        while True:
            try:
                text = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()  # tidy newline after Ctrl+C / Ctrl+Z
                break
            if not text:
                continue
            if text.lower() in EXIT_WORDS:
                print(f"{self.name}: Goodbye.")
                break
            # Step 5 builds the router; echo for now to prove the loop works.
            print(f"{self.name}: (router coming soon — you said {text!r})")
