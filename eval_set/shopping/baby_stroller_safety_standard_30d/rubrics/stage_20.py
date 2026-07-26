"""Stage 20 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s20_servers(env) -> bool:
    """L1 调用正确：stage 20 至少命中 1 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 20, min_count=1):
        return False
    return True


def s20_result(env) -> bool:
    """[后端锚定·二手成交下架] 旧推车经平台担保成交、挂牌下架、回款到账。预算表写清回款/已到账/净支出/对账要素，
    且后端须真实反映：listing lst_strr_0001 状态 == delisted（S20 mutation）。
    只写"已回款"而挂牌后端仍 active（凭空宣称成交）→不得分。

    两值性：预算要素<4→False；后端可达时挂牌须 delisted（仍 active/其它→False），不可达→宽松放行。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    if H._count_any(H.scoped_text(env, ['budget'], idx=20), ['回款', '已到账', 'resale_received', '冲销', '净支出', '对账']) < 4:
        return False
    st = H._backend_listing_status_is(env, 'lst_strr_0001', 'delisted')
    return bool(st)


CHECKS = guard_stage_checks(20, [
    ("s20_servers", s20_servers, 0.5),
    ("s20_result", s20_result, 2.5),
])
