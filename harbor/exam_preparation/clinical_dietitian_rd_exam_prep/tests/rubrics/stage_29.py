from ._helpers import exam_booking_state, exam_calendar_confirmed, tool_used, tool_used_with_args, workspace_contains

STAGE = 29

def s29_exam_location_feed_checked(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "notification_hub", "get_account_feed", ["cdr_exam_updates"])
        and tool_used(env, STAGE, "notification_hub", "get_notification")
        and exam_booking_state(env)
        and workspace_contains(
            env,
            "official_evidence_log.md",
            [["post_exam_location_20261028"], ["notif_exam_location_20261028"], ["received"], ["booked"], ["2026-11-06"], ["building 3"]],
            320,
        )
    )

def s29_calendar_location_updated(env) -> bool:
    return tool_used_with_args(env, STAGE, "calendar", "update_event", ["cal_exam_day"]) and exam_booking_state(env) and exam_calendar_confirmed(env)

CHECKS = [
    ("s29_exam_location_feed_checked", s29_exam_location_feed_checked, 1.25),
    ("s29_calendar_location_updated", s29_calendar_location_updated, 1.5),
]
