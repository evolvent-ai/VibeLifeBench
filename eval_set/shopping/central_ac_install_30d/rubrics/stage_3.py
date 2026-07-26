"""Stage 3 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s3_servers(env) -> bool:
    """L1 调用正确：stage 3 至少命中 2 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 3, min_count=2):
        return False
    return H._stage_server_order_ok(env, 3, ['ecommerce', 'notification_hub'])


def s3_args(env) -> bool:
    """L2 参数正确：stage 3 的工具入参引用了正确的订单/卡/工单等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(
        env, 3, ['ord_iscac_0002', 'ref_iscac_b', 'ntf_iscac_b1'], min_count=1
    )


def s3_result(env) -> bool:
    """Persist the opened work order and require the backend submitted state."""
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['tracker', 'risk', 'decision']) + "\n" + H._agent_response(env, 3)
    described = H._thread_block_has_terms(
        text, tid, ['工单', '安装质量', '举证', '时限', '师傅响应', '凭证'], min_count=3, window=360
    )
    backend = H._backend_refund_status_is(env, 'ord_iscac_0002', 'ref_iscac_b', 'submitted')
    return described and backend is True


CHECKS = guard_stage_checks(3, [
    ("s3_servers", s3_servers, 0.5),
    ("s3_args", s3_args, 1.0),
    ("s3_result", s3_result, 2.0),
])
