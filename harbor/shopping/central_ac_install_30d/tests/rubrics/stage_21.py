"""Stage 21 checks — atomic Checker definitions and weights are in this module。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s21_checklist(env) -> bool:
    """Close the five real pre-deadline work items."""
    return H._count_any(
        H.scoped_text(env, ['decision', 'tracker', 'summary'], idx=21),
        ['payment', 'installer credentials', 'rework work order', 'refund adjustment', 'dispute', 'completed', 'awaiting confirmation'],
    ) >= 5


CHECKS = guard_stage_checks(21, [
    ("s21_checklist", s21_checklist, 2.0),
])
