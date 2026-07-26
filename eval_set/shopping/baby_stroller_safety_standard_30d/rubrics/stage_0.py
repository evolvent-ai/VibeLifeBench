"""Stage 0 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s0_servers(env) -> bool:
    """L1 调用正确：stage 0 至少命中 3 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 0, min_count=3):
        return False
    return True


def s0_args(env) -> bool:
    """L2 参数正确：stage 0 的工具入参引用了正确的订单/卡/挂牌等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(env, 0, ['ord_strr_0001', 'ord_strr_0002', 'usr_yan_ting', 'card_strr_01'], min_count=2)


def s0_result(env) -> bool:
    """L3 结果真值：stage 0 回复/记录出现只有真读后端才知道的真值 token。

    证据维度：🔧工具调用 💬回复
    """
    return H._stage_result_correct(env, 0, ['sf6693520001cn', 'ztostrr5520002cn', '6693'], min_count=1)


def s0_files(env) -> bool:
    """持久化：至少建好 3 个核心 workspace 跟踪文件。

    证据维度：📝持久化
    """
    return H._files_nonempty(env, H.CORE_WORKSPACE_PATHS, min_count=3)


CHECKS = guard_stage_checks(0, [
    ("s0_servers", s0_servers, 0.5),
    ("s0_args", s0_args, 1.0),
    ("s0_result", s0_result, 1.5),
    ("s0_files", s0_files, 0.5),
])
