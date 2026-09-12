from __future__ import annotations
from ._helpers import derived_text, has_exact_number, text_has

def s21_wrapup_severance(env) -> bool:
    raw = derived_text(env)
    if not raw.strip():
        return False
    nums = sum(has_exact_number(raw, value) for value in (33800, 297800, 97000, 200800))
    return nums >= 2 and text_has(raw, [['compensation', 'shortfall', 'deposited', 'conclusion']])

def s21_wrapup_reemploy(env) -> bool:
    raw = derived_text(env)
    if not raw.strip():
        return False
    closing = text_has(raw, [['closing review', 'closing summary', 'closing overview', 'phase review']])
    progress = text_has(raw, [['application', 'interview', 'offer', 'Meituan', 'Dewu']])
    nextstep = text_has(raw, [['unresolved', 'next', 'pending', 'follow-up', 'tracking', 'plan']])
    return closing and progress and nextstep
CHECKS = [('s21_wrapup_severance', s21_wrapup_severance, 2.5), ('s21_wrapup_reemploy', s21_wrapup_reemploy, 2.0)]
