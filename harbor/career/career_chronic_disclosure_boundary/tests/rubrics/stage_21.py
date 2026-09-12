"""Stage 21: write the severance, privacy, and reemployment wrap-up to the board."""
from __future__ import annotations

from ._helpers import derived_text, norm_num, stage_write_used, text_has


def s21_wrapup_severance(env) -> bool:
    if not stage_write_used(env, 21):
        return False
    raw = derived_text(env)
    values = all(value in norm_num(raw) for value in ("33600", "302400", "205400", "97000"))
    outcome = text_has(raw, [["credited", "deposited", "paid"], ["difference", "arbitration", "outstanding"], ["severance", "compensation", "difference"]])
    health = text_has(raw, [["health-information", "medical", "history", "physical", "records"], ["privacy", "not shared externally", "not disclosed", "not authorized"]])
    return values and outcome and health


def s21_wrapup_reemploy(env) -> bool:
    if not stage_write_used(env, 21):
        return False
    raw = derived_text(env)
    progress = text_has(raw, [["application", "applications"], ["interview", "interviews"], ["offer", "offers"], ["Meituan"], ["Poizon"]])
    nextstep = text_has(raw, [["outstanding", "unresolved"], ["next step", "followup"], ["preference", "decision"]])
    return progress and nextstep


CHECKS = [
    ("s21_wrapup_severance", s21_wrapup_severance, 2.5),
    ("s21_wrapup_reemploy", s21_wrapup_reemploy, 2.0),
]
