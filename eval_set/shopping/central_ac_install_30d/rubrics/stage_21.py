"""Stage 21 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s21_checklist(env) -> bool:
    """Close the five real pre-deadline work items."""
    return H._count_any(
        H.scoped_text(env, ['decision', 'tracker', 'summary'], idx=21),
        ['还款', '安装资质', '返工工单', '退补差', '争议', '已完成', '待确认'],
    ) >= 5


CHECKS = guard_stage_checks(21, [
    ("s21_checklist", s21_checklist, 2.0),
])
