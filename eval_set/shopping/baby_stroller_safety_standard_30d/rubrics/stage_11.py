"""Stage 11 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s11_decision(env) -> bool:
    """关键词命中：选定文件/回复中至少出现 4 个规定要素。

    证据维度：📝持久化 💬回复
    """
    return H._count_any(H.scoped_text(env, ['decision', 'gear'], idx=11), ['压价', '1500', '低于', '二手', '更新', '建议', '理由']) >= 4


CHECKS = guard_stage_checks(11, [
    ("s11_decision", s11_decision, 4.0),
])
