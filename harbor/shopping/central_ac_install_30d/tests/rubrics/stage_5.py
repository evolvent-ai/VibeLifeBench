"""Stage 5 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s5_evidence(env) -> bool:
    """Require a complete evidence chain for all three workstreams."""
    text = H.files_text(env, ['evidence']).lower()
    return all(H._thread_evidence_complete(text, tid) for tid in THREAD_IDS)


CHECKS = guard_stage_checks(5, [
    ("s5_evidence", s5_evidence, 4.0),
])
