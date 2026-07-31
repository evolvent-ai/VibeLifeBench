"""Stage 9 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s9_servers(env) -> bool:
    """L1 调用正确：stage 9 同时复核商城工单状态和平台通知。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 9, min_count=2):
        return False
    return H._stage_server_order_ok(env, 9, ['ecommerce', 'notification_hub'])


def s9_args(env) -> bool:
    """L2 参数正确：stage 9 的工具入参引用了正确的订单/卡/工单等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(
        env, 9, ['ord_iscac_0002', 'ref_iscac_b', 'ntf_iscac_b2'], min_count=1
    )


def s9_result(env) -> bool:
    """Require a persisted补证 plan and the backend need-more-evidence state."""
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['decision', 'tracker', 'risk']) + "\n" + H._agent_response(env, 9)
    described = H._thread_block_has_terms(
        text, tid, ['补证', '上门视频', '问题照片', '收费凭证', '平台核对', '时限'], min_count=3, window=360
    )
    backend = H._backend_refund_status_is(env, 'ord_iscac_0002', 'ref_iscac_b', 'rejected')
    return described and backend is True


CHECKS = guard_stage_checks(9, [
    ("s9_servers", s9_servers, 0.5),
    ("s9_args", s9_args, 0.5),
    ("s9_result", s9_result, 2.5),
])
