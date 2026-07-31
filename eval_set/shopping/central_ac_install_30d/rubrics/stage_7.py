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
    """Stage 7 must query the work-order offer or its notification."""
    return H._stage_tool_args_reference(
        env, 7, ['ord_iscac_0002', 'ntf_iscac_cp', 'usr_luo_wei'], min_count=1
    )


def s7_result(env) -> bool:
    """Record the partial-offer amount and the closure consequence in the funds thread."""
    tid = THREAD_IDS[2]
    text = H.files_text(env, ['tracker', 'decision', 'gear', 'budget']) + "\n" + H._agent_response(env, 7)
    return H._thread_block_has_terms(
        text, tid, ['140', '部分退费', '和解', '关闭工单', '继续核对', '退补差'], min_count=3, window=360
    )


CHECKS = guard_stage_checks(7, [
    ("s7_servers", s7_servers, 0.5),
    ("s7_args", s7_args, 0.5),
    ("s7_result", s7_result, 1.0),
])
