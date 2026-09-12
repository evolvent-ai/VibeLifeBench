"""Stage 1: log the position notice, legal basis, and last working day."""
from __future__ import annotations

from ._helpers import derived_text, norm_num, stage_write_used, text_has, trace_result_text, used_tool


def s1_notice_logged(env) -> bool:
    """Require source email evidence and a durable stage-local record."""
    if not (used_tool(env, "read_email", stage=1) or used_tool(env, "get_email", stage=1)):
        return False
    evidence = trace_result_text(env, 1, "email")
    source_bound = text_has(evidence, [
        ["organization and position arrangement notice", "position optimization notice"],
        ["LuminaBio", "liyaobio"],
        ["article 40", "section 40", "law-lcl-040-n3s2ei6mx"],
        ["2026-06-30", "June 30, 2026"],
    ])
    corpus = derived_text(env)
    basis = text_has(corpus, [["article 40", "section 40", "law-lcl-040-n3s2ei6mx"]])
    last_day = any(x in corpus for x in ("2026-06-30", "6-30", "june 30", "june30")) or "0630" in norm_num(corpus)
    return source_bound and stage_write_used(env, 1) and basis and last_day


CHECKS = [("s1_notice_logged", s1_notice_logged, 3.5)]
