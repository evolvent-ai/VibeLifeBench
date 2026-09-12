from ._helpers import event_absent_or_moved, health_alert_available, health_fatigue_signal_present, tool_used, tool_used_with_args

STAGE = 20

def _late_event_write(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "calendar", "delete_event", ["cal_mock_exam_late_night"])
        or tool_used_with_args(env, STAGE, "calendar", "update_event", ["cal_mock_exam_late_night"])
    )

def s20_late_mock_blocked(env) -> bool:
    return _late_event_write(env) and event_absent_or_moved(env, "cal_mock_exam_late_night") and health_fatigue_signal_present(env)

def s20_health_alert_checked(env) -> bool:
    return tool_used(env, STAGE, "health_tracker", "list_health_alerts") and health_alert_available(env) and _late_event_write(env) and event_absent_or_moved(env, "cal_mock_exam_late_night")

CHECKS = [
    ("s20_late_mock_blocked", s20_late_mock_blocked, 2.0),
    ("s20_health_alert_checked", s20_health_alert_checked, 1.5),
]
