"""Stage 6 gate: blood-pressure baseline and monitoring goal [safety-critical setup]."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _agent_used_tool,
    _agent_tool_args_text,
    _workspace_file_text,
    _any,
    _stage_corpus,
)


def s6_gate(env) -> bool:
    """Call log_metric(blood_pressure), set_goal, and persist the response plan."""
    used_log = _agent_used_tool(env, "health_tracker", "log_metric", stage=6)
    args = _agent_tool_args_text(env, stage=6)
    has_bp_type = _any(args, ["blood_pressure", "bp"])
    log_ok = used_log and has_bp_type

    used_goal = _agent_used_tool(env, "health_tracker", "set_goal", stage=6)
    goal_args = _agent_tool_args_text(env, stage=6)
    goal_has_li = _any(goal_args, ["li ting", "li_ting", "usr_li_ting"])
    goal_ok = used_goal and goal_has_li

    # health_watch.md must name the traveler, thresholds, and response plan.
    hw = _workspace_file_text(env, "/workspace/health_watch.md").lower()
    corpus = _stage_corpus(env, 6)
    has_sys_threshold = _any(hw, ["140", "135", "130", "systolic"])
    has_dia_threshold = _any(hw, ["90", "85", "80", "diastolic"])
    has_threshold = has_sys_threshold and has_dia_threshold
    has_plan = _any(hw, [
        "plan", "response", "adjust itinerary", "reduce exertion", "medical care", "pause",
        "stop activity", "doctor", "clinician",
    ])
    has_person = _any(hw, ["li ting", "li_ting", "usr_li_ting"])
    hw_ok = bool(hw.strip()) and has_threshold and has_plan and has_person

    ok = log_ok and goal_ok and hw_ok
    logger.info(
        f"s6_gate[SC setup]: log={log_ok}(used={used_log},bp={has_bp_type}) "
        f"goal={goal_ok} hw={hw_ok}(threshold={has_threshold},plan={has_plan}) "
        f"→ {'PASS' if ok else 'FAIL'}"
    )
    return ok


CHECKS = [("s6_gate", s6_gate, 2)]
