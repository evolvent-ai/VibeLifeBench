"""Stage 9: deadlines and food testing."""
from __future__ import annotations
from ._helpers import _stage_corpus, _all_events_text
from .cross_stage import d_import_chinese_label, d_limitation_three_years

def s9_deadlines_in_calendar(env) -> bool:
    text = _all_events_text(env)
    return text is not None and any(k in text for k in ("evidence submission", "testing", "trial hearing", "appeal", "defense", "deadline", "case filing"))

def s9_apply_inspection(env) -> bool:
    text = _stage_corpus(env, 9)
    return any(k in text for k in ("testing", "apply for testing", "submit for testing", "CMA", "unlawful additive", "label compliance"))
CHECKS = [("d_import_chinese_label", d_import_chinese_label, 1), ("d_limitation_three_years", d_limitation_three_years, 0.5)]

