"""Stage 19 checks — atomic Checker definitions and weights are in this module。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s19_result(env) -> bool:
    """Require the approved ¥224 service compensation in text and backend state."""
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['tracker', 'decision', 'evidence', 'budget']) + "\n" + H._agent_response(env, 19)
    described = H._thread_block_has_terms(
        text, tid, ['platform review', 'quality report', 'refund adjustment', '224', 'approved'], min_count=3, window=360
    )
    status = H._backend_refund_status_is(env, 'ord_iscac_0002', 'ref_iscac_b', 'approved')
    amount = H._refund_amount(env, 'ord_iscac_0002', 'ref_iscac_b')
    return described and status is True and amount == 22400


CHECKS = guard_stage_checks(19, [
    ("s19_result", s19_result, 2.5),
])
