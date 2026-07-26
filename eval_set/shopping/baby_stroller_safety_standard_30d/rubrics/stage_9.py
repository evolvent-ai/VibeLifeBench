"""Stage 9 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s9_servers(env) -> bool:
    """L1 调用正确：stage 9 同时复核商城退款状态和平台通知。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 9, min_count=2):
        return False
    return H._stage_server_order_ok(env, 9, ['ecommerce', 'notification_hub'])


def s9_args(env) -> bool:
    """L2 参数正确：stage 9 的工具入参引用了正确的订单/卡/挂牌等实体。

    证据维度：🔧工具调用
    """
    # P2 fix A: dropped phantom 'tkt_strr_1' (no ticket seeded at this stage; stage 9 = 退货补证 on delivery_logistics, ticket_seq=0). Remaining tokens all exist in env init.sql.
    return H._stage_tool_args_reference(
        env, 9, ['ord_strr_0002', 'ref_strr_b', 'ntf_strr_b2'], min_count=1
    )


def s9_result(env) -> bool:
    """[后端锚定·状态转移] 线2退货：商家有异议、退款被驳回需补证。持久化须写清补证/平台介入等要素，
    且退款后端状态须为 rejected（本阶段 mutation 将 ref_strr_b 置为 rejected）——体现真实状态转移，
    而不是只写"补证/开箱视频"关键词。

    两值性：文本要素<3→False；后端可达时状态须为 rejected（仍 submitted/已 approved/缺失→False），
    不可达→宽松放行后端子条件。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['decision', 'tracker', 'risk']) + "\n" + H._agent_response(env, 9)
    if not H._thread_block_has_terms(text, tid, ['补证', '开箱视频', '使用痕迹', '平台介入', '时限', '举证责任'], min_count=3, window=320):
        return False
    st = H._backend_refund_status_is(env, 'ord_strr_0002', 'ref_strr_b', 'rejected')
    return bool(st)


CHECKS = guard_stage_checks(9, [
    ("s9_servers", s9_servers, 0.5),
    ("s9_args", s9_args, 0.5),
    ("s9_result", s9_result, 2.5),
])
