from __future__ import annotations
from ._helpers import derived_text, has_exact_number, used_tool

def s4_plan_logged(env) -> bool:
    read_ok = used_tool(env, 'read_email') or used_tool(env, 'get_email')
    raw = derived_text(env)
    if not raw.strip():
        return False
    plan_amt = has_exact_number(raw, 200800)
    folded = raw.casefold()
    deadline = any(needle in folded for needle in ('2026-06-22', '6-22', 'june 22', '22 june', '0622'))
    return read_ok and (plan_amt and deadline)
CHECKS = [('s4_plan_logged', s4_plan_logged, 4.0)]
