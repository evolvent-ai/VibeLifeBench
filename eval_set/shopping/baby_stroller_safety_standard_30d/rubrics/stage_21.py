"""Stage 21 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s21_checklist(env) -> bool:
    """关键词命中：选定文件/回复中至少出现 5 个规定要素。

    证据维度：📝持久化 💬回复
    """
    return H._count_any(H.scoped_text(env, ['decision', 'tracker', 'summary'], idx=21), ['还款', '出运', '保修', '回款', '争议', '已完成', '待确认']) >= 5


CHECKS = guard_stage_checks(21, [
    ("s21_checklist", s21_checklist, 2.0),
])
