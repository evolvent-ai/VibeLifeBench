"""Stage 13 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s13_budget(env) -> bool:
    """关键词命中：选定文件/回复中至少出现 4 个规定要素。

    证据维度：📝持久化 💬回复
    """
    return H._count_any(H.scoped_text(env, ['budget'], idx=13), ['已付', '待退', '待回款', '预估', '回款', '冲销', 'estimated', 'ordered']) >= 4


CHECKS = guard_stage_checks(13, [
    ("s13_budget", s13_budget, 3.0),
])
