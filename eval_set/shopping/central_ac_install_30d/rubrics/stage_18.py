"""Stage 18 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s18_servers(env) -> bool:
    """L1 调用正确：stage 18 至少命中 1 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 18, min_count=1):
        return False
    return True


def s18_result(env) -> bool:
    """Require persisted dispute resolution plus real backend approval and reversal."""
    text = H.scoped_text(env, ['budget', 'decision', 'tracker'], idx=18)
    semantic = (
        H._count_any(text, ['争议', '通过', '冲销', '已冲销', '应还', '216']) >= 3
        and H._count_any(text, ['tx_iscac_rev']) >= 1
    )
    dispute = H._backend_dispute_status_is(env, 'card_iscac_01', 'disp_iscac_01', 'approved')
    reversal = H._backend_reversal_present(env, 'card_iscac_01', amount_minor=-21600)
    return semantic and dispute is True and reversal is True


CHECKS = guard_stage_checks(18, [
    ("s18_servers", s18_servers, 0.5),
    ("s18_result", s18_result, 2.0),
])
