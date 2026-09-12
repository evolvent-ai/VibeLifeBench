"""Stage 7: keep the reemployment board warm during a quiet period."""
from __future__ import annotations

from ._helpers import derived_text, text_has


def s7_quiet_monitor(env) -> bool:
    """Continuity check: preserve reemployment clues or a follow-up plan."""
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    return text_has(corpus, [["position", "application", "applications", "jobs", "search", "plan", "followup"]])


CHECKS = [
    ("s7_quiet_monitor", s7_quiet_monitor, 1.5),
]
