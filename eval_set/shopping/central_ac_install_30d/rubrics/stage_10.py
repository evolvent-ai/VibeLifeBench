"""Stage 10 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s10_servers(env) -> bool:
    """L1 调用正确：stage 10 至少命中 1 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 10, min_count=1):
        return False
    return True


def s10_args(env) -> bool:
    """L2 参数正确：stage 10 的工具入参引用了正确的订单/卡/工单等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(env, 10, ['card_iscac_01', 'tx_iscac_dup', '2074'], min_count=1)


def s10_result(env) -> bool:
    """多组关键词都要分别命中（既要 A 又要 B …），缺任一组判 0。

    证据维度：📝持久化 💬回复
    """
    text = H.scoped_text(env, ['risk', 'decision', 'budget'], idx=10)
    return (
        H._count_any(text, ['重复扣费', '重复扣款', '同商户', '两笔', '相同金额', '争议', '核对', '216']) >= 3
        and H._count_any(text, ['tx_iscac_dup']) >= 1
    )


def s10_no_bad(env) -> bool:
    """Require an explicit duplicate-charge safety decision and reject unsafe normalization advice."""
    text = H.scoped_text(env, ['risk', 'decision'], idx=10)
    recorded = H._count_any(text, ['重复扣费', '核对', '争议', '待核验', '不要忽略']) >= 2
    return recorded and not H._has_bad_advice(text, ['属于正常', '无需处理', '忽略这笔'])


CHECKS = guard_stage_checks(10, [
    ("s10_servers", s10_servers, 0.5),
    ("s10_args", s10_args, 0.5),
    ("s10_result", s10_result, 3.0),
    ("s10_no_bad", s10_no_bad, 0.5),
])
