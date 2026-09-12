"""Stage 23 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s23_structured(env) -> bool:
    """Require at least five prescribed archive keywords."""
    return H._count_any(H.scoped_text(env, ['summary'], idx=23), ['resolved', 'in progress', 'awaiting confirmation', 'credit pending', 'lessons', 'template']) >= 5


def s23_threads(env) -> bool:
    """Require distinct archive sections for all three workstreams."""
    text = H.files_text(env, ['summary', 'tracker']).lower()
    return H._thread_sections_distinct(text)


CHECKS = guard_stage_checks(23, [
    ("s23_structured", s23_structured, 2.0),
    ("s23_threads", s23_threads, 1.0),
])
