"""Stage 6 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s6_servers(env) -> bool:
    """L1 调用正确：stage 6 至少命中 1 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 6, min_count=1):
        return False
    return True


def s6_args(env) -> bool:
    """L2 参数正确：stage 6 的工具入参引用了正确的订单/卡/挂牌等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(env, 6, ['card_strr_01', 'tx_strr_fx', '6693'], min_count=1)


def s6_result(env) -> bool:
    """多组关键词都要分别命中（既要 A 又要 B …），缺任一组判 0。

    证据维度：📝持久化 💬回复
    """
    text = H.scoped_text(env, ['budget', 'decision', 'risk'], idx=6)
    return (
        H._count_any(text, ['babyjogger', '海淘', '美元', '外币']) >= 1
        and H._count_any(text, ['258']) >= 1
        and H._count_any(text, ['外币', '汇率', '待入账', '核对', '正常']) >= 1
    )


CHECKS = guard_stage_checks(6, [
    ("s6_servers", s6_servers, 0.5),
    ("s6_args", s6_args, 0.5),
    ("s6_result", s6_result, 1.5),
])
