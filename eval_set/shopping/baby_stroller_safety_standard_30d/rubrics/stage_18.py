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
    """[后端锚定·争议冲销] 信用卡重复扣费争议通过、款项冲销。持久化写清争议/通过/冲销/应还等要素，
    且后端须真实反映：dispute disp_strr_01 状态 == approved，且未出账里存在一笔冲销 -25800 分（争议冲销）。
    只写"争议已通过"而后端未 approved/无冲销行→不得分。

    两值性：文本要素<3→False；后端必须可达，且 dispute 须为 approved 并存在 -25800 冲销行；不可达或不一致均失败。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    if H._count_any(H.scoped_text(env, ['budget', 'decision', 'tracker'], idx=18), ['争议', '通过', '冲销', '已冲销', '应还', '归档', '258']) < 3:
        return False
    dstat = H._backend_dispute_status_is(env, 'card_strr_01', 'disp_strr_01', 'approved')
    rev = H._backend_reversal_present(env, 'card_strr_01', amount_minor=-25800)
    return dstat is True and rev is True


CHECKS = guard_stage_checks(18, [
    ("s18_servers", s18_servers, 0.5),
    ("s18_result", s18_result, 2.0),
])
