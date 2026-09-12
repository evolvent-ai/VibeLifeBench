"""Stage 4: read and record the employer proposal."""
from __future__ import annotations
from ._helpers import derived_text, norm_num, used_tool


def s4_plan_logged(env) -> bool:
    if not used_tool(env, "read_email", stage=4, server="email"):
        return False
    raw = derived_text(env)
    compact = norm_num(raw)
    return bool(raw.strip()) and ("204500" in compact or "20.45w" in raw) and any(value in raw for value in ("2026-06-22", "June 22", "6-22"))


CHECKS = [("s4_plan_logged", s4_plan_logged, 4.0)]
