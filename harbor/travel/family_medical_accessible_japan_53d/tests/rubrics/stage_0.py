from __future__ import annotations

from ._helpers import _workspace_file_exists, _workspace_file_text, text_has


def s0_initial_state_files(env) -> bool:
    required = ("trip_plan.md", "budget_ledger.md", "risk_register.md", "decision_log.md")
    if not all(_workspace_file_exists(env, name) for name in required):
        return False
    trip = _workspace_file_text(env, "trip_plan.md")
    budget = _workspace_file_text(env, "budget_ledger.md")
    risk = _workspace_file_text(env, "risk_register.md")
    decision = _workspace_file_text(env, "decision_log.md")
    return bool(
        text_has(trip, [["osaka", "Osaka"], ["kyoto", "Kyoto"], ["nara", "Nara"], ["arima", "Arima Onsen"], ["option", "candidate"]])
        and text_has(budget, [["estimate", "estimated"], ["status", "state"], ["evidence", "supporting evidence"]])
        and text_has(risk, [["mobility", "accessibility", "walking"], ["owner", "responsible"], ["next review", "review"]])
        and text_has(decision, [["unpaid", "do not pay", "payment pending"], ["authorization", "authority"], ["next action", "action"]])
    )


CHECKS = [("s0_initial_state_files", s0_initial_state_files, 2.0)]
