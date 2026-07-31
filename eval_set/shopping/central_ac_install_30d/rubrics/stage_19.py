"""Stage 19 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s19_result(env) -> bool:
    """Require the approved ¥224 service compensation in text and backend state."""
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['tracker', 'decision', 'evidence', 'budget']) + "\n" + H._agent_response(env, 19)
    described = H._thread_block_has_terms(
        text, tid, ['平台核对', '质检报告', '退补差', '224', '获批'], min_count=3, window=360
    )
    status = H._backend_refund_status_is(env, 'ord_iscac_0002', 'ref_iscac_b', 'approved')
    amount = H._refund_amount(env, 'ord_iscac_0002', 'ref_iscac_b')
    return described and status is True and amount == 22400


CHECKS = guard_stage_checks(19, [
    ("s19_result", s19_result, 2.5),
])
