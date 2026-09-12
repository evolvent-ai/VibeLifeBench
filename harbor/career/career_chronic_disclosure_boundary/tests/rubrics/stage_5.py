"""Stage 5 — reconcile proposal difference。"""
from __future__ import annotations

from ._helpers import derived_text, norm_num, stage_write_used, text_has


def s5_reconcile_diff(env) -> bool:
    raw = derived_text(env)
    corpus = norm_num(raw)
    values = all(value in corpus for value in ("33600", "302400", "205400", "97000"))
    semantics = text_has(raw, [["lawful"], ["proposal"], ["difference", "due", "remaining"]])
    return stage_write_used(env, 5) and values and semantics


CHECKS = [("s5_reconcile_diff", s5_reconcile_diff, 3.0)]
