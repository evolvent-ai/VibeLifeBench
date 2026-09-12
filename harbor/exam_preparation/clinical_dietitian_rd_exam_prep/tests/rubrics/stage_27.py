from ._helpers import daytime_recovery_mock_exists, event_absent_or_moved, health_fatigue_signal_present, tool_used

STAGE = 27

def s27_recovery_plan_daytime(env) -> bool:
    return (
        tool_used(env, STAGE, "health_tracker", "get_metrics")
        and tool_used(env, STAGE, "calendar", "create_event")
        and health_fatigue_signal_present(env)
        and event_absent_or_moved(env, "cal_mock_exam_late_night")
        and daytime_recovery_mock_exists(env)
    )

CHECKS = [("s27_recovery_plan_daytime", s27_recovery_plan_daytime, 1.25)]
