"""Stage 7 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s7_servers(env) -> bool:
    """L1 调用正确：stage 7 至少命中 1 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 7, min_count=1):
        return False
    return True


def s7_args(env) -> bool:
    """L2 参数正确：stage 7 的工具入参引用了正确的订单/卡/挂牌等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(env, 7, ['lst_strr_0001', 'usr_yan_ting', 'ntf_strr_buyer_20260621'], min_count=1)


def s7_result(env) -> bool:
    """第 3 条线的关键结论落到持久化文件/当阶段回复，且锚定在该线标题块内。

    证据维度：📝持久化 💬回复
    """
    tid = THREAD_IDS[2]
    text = H.files_text(env, ['tracker', 'decision', 'gear']) + "\n" + H._agent_response(env, 7)
    return H._thread_block_has_terms(text, tid, ['买家', '询价', '压价', '当面', '平台担保', '比价'], min_count=2, window=320)


CHECKS = guard_stage_checks(7, [
    ("s7_servers", s7_servers, 0.5),
    ("s7_args", s7_args, 0.5),
    ("s7_result", s7_result, 1.0),
])
