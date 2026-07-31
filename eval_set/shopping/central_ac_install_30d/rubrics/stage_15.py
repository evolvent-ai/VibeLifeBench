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
    """Persist a deadline-aware online-evidence and visit-rescheduling plan."""
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['decision', 'tracker', 'gear']) + "\n" + H._agent_response(env, 15)
    return H._thread_block_has_terms(
        text, tid, ['平台核对', '在线提交', '改期', '上门', '时限', '举证'], min_count=3, window=360
    )


def s15_weather(env) -> bool:
    """Require a weather-aware action plan backed by the live weather environment."""
    text = H.scoped_text(env, ['decision', 'risk', 'tracker'], idx=15)
    semantic = (
        H._count_any(text, ['暴雨', '橙色预警', '强降水']) >= 2
        and H._count_any(text, ['改期', '错峰', '在线提交', '远程举证', '备选']) >= 1
        and H._count_any(text, ['工单时限', '举证窗口', '截止']) >= 1
    )
    alert = H._backend_state_has(
        env, 'weather', 'get_alerts', ['alr_iscac_storm_20260702', 'orange'], min_count=2, geo='深圳市'
    )
    forecast = H._backend_state_has(
        env, 'weather', 'get_forecast_daily', ['2026-07-02', 'rainstorm', '2026-07-03'], min_count=3,
        geo='深圳市', days=3,
    )
    return semantic and alert is True and forecast is True


CHECKS = guard_stage_checks(15, [
    ("s15_servers", s15_servers, 0.5),
    ("s15_result", s15_result, 3.0),
    ("s15_weather", s15_weather, 2.5),
])
