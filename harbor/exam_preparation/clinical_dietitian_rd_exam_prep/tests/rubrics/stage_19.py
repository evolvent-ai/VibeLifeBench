from ._helpers import health_alert_available, health_fatigue_signal_present, tool_used, workspace_contains

STAGE = 19

def s19_fatigue_response_grounded(env) -> bool:
    return (
        tool_used(env, STAGE, "health_tracker", None)
        and health_fatigue_signal_present(env)
        and health_alert_available(env)
        and workspace_contains(
            env,
            "mock_score_log.md",
            [["fatigue_signal"], ["205"], ["104"], ["late-night", "midnight"], ["enteral", "parenteral"], ["stop", "adjust"]],
            120,
        )
    )

CHECKS = [("s19_fatigue_response_grounded", s19_fatigue_response_grounded, 1.25)]
