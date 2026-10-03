"""Semantic router: matches by meaning, not keywords.

Embeds the input and each skill's description + examples, then picks
the highest cosine similarity. Same (skill, confidence) interface
as the keyword router — they're interchangeable strategies.
"""
import logging

from jarvis.skills import REGISTRY
from jarvis.skills.base import Skill

log = logging.getLogger(__name__)

_model = None
_skill_vectors = {}  # skill name -> (skill, embedding tensor)


def _get_model(model_name: str):
    """Lazy-load: don't pay seconds of load time + RAM unless it's used."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        log.info("Loading embedding model '%s' (one-time cost)...", model_name)
        _model = SentenceTransformer(model_name)
    return _model


def _index_skills(model) -> None:
    """Embed every skill's description + examples ONCE, at startup."""
    _skill_vectors.clear()
    for skill in REGISTRY.values():
        texts = [t for t in [skill.description, *skill.examples] if t.strip()]
        vectors = model.encode(texts or [skill.name], convert_to_tensor=True)
        _skill_vectors[skill.name] = (skill, vectors)


def semantic_route(text: str, threshold: float = 0.6,
                   model_name: str = "all-MiniLM-L6-v2") -> tuple[Skill | None, float]:
    from sentence_transformers import util

    model = _get_model(model_name)
    if not _skill_vectors:
        _index_skills(model)

    query_vec = model.encode(text, convert_to_tensor=True)
    best_skill, best_score = None, 0.0
    for skill, vectors in _skill_vectors.values():
        score = float(util.cos_sim(query_vec, vectors)[0].max())
        log.debug("semantic router: skill=%s score=%.2f", skill.name, score)
        if score > best_score:
            best_skill, best_score = skill, score

    if best_skill is not None and best_score >= threshold:
        return best_skill, best_score
    return None, 0.0
