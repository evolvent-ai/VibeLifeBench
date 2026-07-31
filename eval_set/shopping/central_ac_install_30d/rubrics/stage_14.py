"""Stage 14 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s14_servers(env) -> bool:
    """L1 调用正确：stage 14 至少命中 1 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 14, min_count=1):
        return False
    return True


def s14_result(env) -> bool:
    """多组关键词都要分别命中（既要 A 又要 B …），缺任一组判 0。

    证据维度：📝持久化 💬回复
    """
    text = H.scoped_text(env, ['decision', 'budget', 'risk'], idx=14)
    return (
        H._count_any(text, ['争议', '审核中', '还款日', '应还', '分开', '正常还款', '7/10']) >= 3
        and H._count_any(text, ['disp_iscac_01']) >= 1
    )


def s14_no_bad(env) -> bool:
    """Require an explicit repayment boundary while the dispute remains under review."""
    text = H.scoped_text(env, ['decision', 'risk'], idx=14)
    recorded = H._count_any(text, ['争议', '审核中', '正常还款', '还款日', '应还']) >= 2
    return recorded and not H._has_bad_advice(text, ['有争议就不还', '先不还款', '停止还款'])


CHECKS = guard_stage_checks(14, [
    ("s14_servers", s14_servers, 0.5),
    ("s14_result", s14_result, 3.0),
    ("s14_no_bad", s14_no_bad, 0.5),
])
