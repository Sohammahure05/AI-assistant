"""The assistant shell. Later phases plug the router, skills,
memory, and voice into this — the entry point never changes."""
import logging
from jarvis.core.router import route
from functools import partial


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
        self._router = self._build_router()

        log.info("%s initialised.", self.name)

    def _build_router(self):
        """Pick the routing strategy from config; default is keyword."""
        method = self.config["router"].get("method", "keyword")
        if method == "semantic":
            from jarvis.core.semantic_router import semantic_route
            model_name = self.config["router"].get("model_name", "all-MiniLM-L6-v2")
            log.info("Using semantic router (%s)", model_name)
            return partial(semantic_route, model_name=model_name)
        from jarvis.core.router import route
        log.info("Using keyword router")
        return route


    def greet(self) -> None:
        print(f"{self.name}: At your service.")

    def run(self) -> None:
        """Read-Eval-Print Loop: read input, route it, print the result."""
        self.greet()
        threshold = self.config["router"]["confidence_threshold"]
        while True:
            try:
                text = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not text:
                continue
            if text.lower() in EXIT_WORDS:
                print(f"{self.name}: Goodbye.")
                break
            skill, confidence = self._router(text, threshold)

            if skill is None:
                print(f"{self.name}: I don't understand that yet.")
                log.info("No skill matched for %r", text)
                continue
            log.info("Routed %r -> %s (confidence=%.2f)", text, skill.name, confidence)
            result = skill.handle(text)
            print(f"{self.name}: {result.message}")

