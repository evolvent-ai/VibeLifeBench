"""Stage 19: maintain both workstreams through a quiet gap."""
from __future__ import annotations

from ._helpers import derived_text, text_has


def s19_maintains_state(env) -> bool:
    """Continuity check: the board retains unresolved severance and reemployment items."""
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    return (text_has(corpus, [["severance", "difference", "arbitration", "negotiate"]])
            and text_has(corpus, [["offer", "interview", "application", "reemployment"]]))


CHECKS = [
    ("s19_maintains_state", s19_maintains_state, 1.5),
]
