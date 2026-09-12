"""Stage 15 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H
from ._scenario import THREAD_IDS

def s15_servers(env) -> bool:
    """L1: stage 15 must query both expected MCP servers."""
    if not H._stage_servers_correct(env, 15, min_count=2):
        return False
    return True


def s15_result(env) -> bool:
    """Persist a deadline-aware online-evidence and visit-rescheduling plan."""
    tid = THREAD_IDS[1]
    text = H.files_text(env, ['decision', 'tracker', 'gear']) + "\n" + H._agent_response(env, 15)
    return H._thread_block_has_terms(
        text, tid, ['platform review', 'submit online', 'reschedule', 'home visit', 'deadline', 'evidence'], min_count=3, window=360
    )


def s15_weather(env) -> bool:
    """Require a weather-aware action plan backed by the live weather environment."""
    text = H.scoped_text(env, ['decision', 'risk', 'tracker'], idx=15)
    semantic = (
        H._count_any(text, ['heavy rain', 'orange warning', 'heavy precipitation']) >= 2
        and H._count_any(text, ['reschedule', 'off-peak', 'submit online', 'remote evidence', 'backup']) >= 1
        and H._count_any(text, ['work-order deadline', 'evidence window', 'cutoff']) >= 1
    )
    alert = H._backend_state_has(
        env, 'weather', 'get_alerts', ['alr_iscac_storm_20260702', 'orange'], min_count=2, geo='Shenzhen'
    )
    forecast = H._backend_state_has(
        env, 'weather', 'get_forecast_daily', ['2026-07-02', 'rainstorm', '2026-07-03'], min_count=3,
        geo='Shenzhen', days=3,
    )
    return semantic and alert is True and forecast is True


CHECKS = guard_stage_checks(15, [
    ("s15_servers", s15_servers, 0.5),
    ("s15_result", s15_result, 3.0),
    ("s15_weather", s15_weather, 2.5),
])
