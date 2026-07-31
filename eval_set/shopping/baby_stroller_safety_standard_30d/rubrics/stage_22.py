"""Stage 22 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s22_consistency(env) -> bool:
    """关键词命中：选定文件/回复中至少出现 4 个规定要素。

    证据维度：📝持久化 💬回复
    """
    return H._count_any(H.scoped_text(env, ['tracker', 'decision', 'risk'], idx=22), ['一致', '对账', '冲突', '核对', '商城', '转运', '信用卡']) >= 4


CHECKS = guard_stage_checks(22, [
    ("s22_consistency", s22_consistency, 2.0),
])
