"""Stage 19 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s19_result(env) -> bool:
    """[后端锚定·终态] 线2退货：平台介入裁决退货成立、安排退款。持久化写清平台介入/退货成立/退款/凭证，
    且退款后端状态须为 approved（S19 mutation 将 ref_strr_b 置 approved），金额 == 53760 分。
    只写"退货成立"而后端未 approved（凭空宣称）→不得分。

    两值性：文本要素<3→False；后端必须可达，退款状态须为 approved 且金额 == 53760；不可达或不一致均失败。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['tracker', 'decision', 'evidence']) + "\n" + H._agent_response(env, 19)
    if not H._thread_block_has_terms(text, tid, ['平台介入', '退货成立', '举证', '退款', '凭证'], min_count=3, window=320):
        return False
    st = H._backend_refund_status_is(env, 'ord_strr_0002', 'ref_strr_b', 'approved')
    amt = H._refund_amount(env, 'ord_strr_0002', 'ref_strr_b')
    return st is True and amt == 53760


CHECKS = guard_stage_checks(19, [
    ("s19_result", s19_result, 2.5),
])
