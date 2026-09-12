"""Stage 16: judgment response and appeal window."""
from __future__ import annotations
from ._helpers import _stage_corpus
from .cross_stage import d_appeal_window_15d

def s16_responds_judgment(env) -> bool:
    text = _stage_corpus(env, 16)
    return any(k in text for k in ("judgment", "prevail", "support", "refund plus tenfold compensation", "tenfold compensation")) and any(k in text for k in ("medical expense", "medical treatment", "320")) and any(k in text for k in ("appeal period", "15 days", "enforcement", "apply for enforcement", "you decide"))
CHECKS = [("d_appeal_window_15d", d_appeal_window_15d, 0.5)]

