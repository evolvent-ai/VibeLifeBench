"""Stage 15 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s15_servers(env) -> bool:
    """L1 调用正确：stage 15 至少命中 2 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 15, min_count=2):
        return False
    return True


def s15_result(env) -> bool:
    """[后端锚定] 线2退货举证时限窗口（7/9 前推动平台介入）。持久化写清平台介入/补证/时限，
    且此刻退款后端状态尚未 approved（仍在 submitted/rejected/need_more，裁决在 7/10 才落）——
    防止 agent 提前把"退货成立"编成已完成。

    两值性：文本要素<3→False；后端可达时状态须 ∈ {submitted, rejected}（若已 approved=提前泄露→False），
    不可达→宽松放行后端子条件。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['decision', 'tracker', 'gear']) + "\n" + H._agent_response(env, 15)
    if not H._thread_block_has_terms(text, tid, ['平台介入', '补证', '7/9', '退货', '时限', '举证'], min_count=3, window=320):
        return False
    st = H._backend_refund_status_is(env, 'ord_strr_0002', 'ref_strr_b', 'rejected')
    return bool(st)


CHECKS = guard_stage_checks(15, [
    ("s15_servers", s15_servers, 0.5),
    ("s15_result", s15_result, 3.0),
])
