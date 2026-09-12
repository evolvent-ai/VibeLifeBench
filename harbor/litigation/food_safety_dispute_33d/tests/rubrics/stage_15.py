"""Stage 15: post-hearing summary."""
from __future__ import annotations
from ._helpers import _food_journal_text

def s15_post_hearing_notion(env) -> bool:
    text = _food_journal_text(env)
    return bool(text) and any(k in text for k in ("post-hearing", "hearing summary")) and any(k in text for k in ("issues", "focus")) and any(k in text for k in ("our claims", "plaintiff's claims", "claims")) and any(k in text for k in ("basis", "Food Safety Law", "precedent")) and any(k in text for k in ("defense response", "cross-examination", "rebuttal"))
CHECKS = [("s15_persisted_post_hearing_summary", s15_post_hearing_notion, 0.75)]

