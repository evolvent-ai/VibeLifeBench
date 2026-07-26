"""Stage 5 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s5_evidence(env) -> bool:
    """证据链完整：三条线在 evidence_log.md 内各自覆盖该线关键证据要素。

    证据维度：📝持久化 🔗跨阶段
    """
    text = H.files_text(env, ['evidence']).lower()
    return all(H._thread_evidence_complete(text, tid) for tid in THREAD_IDS)


CHECKS = guard_stage_checks(5, [
    ("s5_evidence", s5_evidence, 4.0),
])
