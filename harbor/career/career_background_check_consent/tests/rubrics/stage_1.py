"""Stage 1: record the restructuring basis and last-day."""
from __future__ import annotations
from ._helpers import derived_text, norm_num, text_has, used_tool


def s1_notice_logged(env) -> bool:
    if not used_tool(env, "read_email", stage=1, server="email"):
        return False
    corpus = derived_text(env)
    basis = text_has(corpus, [["article40", "article 40", "art40", "no-fault", "elimination", "restructuring"]])
    last_day = any(value in corpus for value in ("2026-06-30", "6-30", "June 30", "0630")) or "0630" in norm_num(corpus)
    return bool(corpus.strip()) and basis and last_day


CHECKS = [("s1_notice_logged", s1_notice_logged, 3.5)]
