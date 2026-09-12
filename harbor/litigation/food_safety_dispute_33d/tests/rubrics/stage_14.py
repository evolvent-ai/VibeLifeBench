"""Stage 14: hearing response."""
from __future__ import annotations
from ._helpers import _food_journal_text

def s14_responds_hearing(env) -> bool:
    text = _food_journal_text(env)
    return bool(text) and any(k in text for k in ("hearing", "trial hearing", "at the hearing", "court")) and sum(k in text for k in ("cross-examination", "tenfold", "knowingly buying counterfeit goods", "Chinese label", "unlawful additive")) >= 2 and any(k in text for k in ("await judgment", "await the court judgment", "judgment to be announced later", "judgment pending service"))
CHECKS = [("s14_responds_hearing", s14_responds_hearing, 0.5)]

