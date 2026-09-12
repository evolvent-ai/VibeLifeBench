from ._helpers import health_alert_available, health_fatigue_signal_present, tool_used, tool_used_with_args

STAGE = 17

def s17_health_metrics_checked(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "health_tracker", "get_metrics", ["sleep_minutes"])
        and tool_used(env, STAGE, "health_tracker", "list_health_alerts")
        and tool_used(env, STAGE, "calendar", None)
        and health_fatigue_signal_present(env)
        and health_alert_available(env)
    )

CHECKS = [("s17_health_metrics_checked", s17_health_metrics_checked, 1.5)]
