"""Stage 22 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s22_consistency(env) -> bool:
    """Persist cross-service reconciliation without flattening unresolved differences."""
    return H._count_any(
        H.scoped_text(env, ['tracker', 'decision', 'risk'], idx=22),
        ['一致', '对账', '冲突', '时间差', '商城', '送装', '信用卡', '邮件', '通知'],
    ) >= 5


CHECKS = guard_stage_checks(22, [
    ("s22_consistency", s22_consistency, 2.0),
])
