"""Stage 11 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s11_decision(env) -> bool:
    """Update the decision using the actual third-party inspection report."""
    text = H.scoped_text(env, ['decision', 'gear', 'evidence'], idx=11)
    return (
        H._count_any(text, ['qi-sz-0625', '排水坡度', '冷媒管', '质检报告']) >= 2
        and H._count_any(text, ['224', '部分退费', '平台核对', '继续举证', '建议', '理由']) >= 3
    )


CHECKS = guard_stage_checks(11, [
    ("s11_decision", s11_decision, 4.0),
])
