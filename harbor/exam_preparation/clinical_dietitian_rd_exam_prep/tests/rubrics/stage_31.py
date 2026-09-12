from ._helpers import exam_booking_state, exam_calendar_confirmed, tool_used_with_args, workspace_contains

STAGE = 31

def s31_pre_exam_calendar_checked(env) -> bool:
    return (
        tool_used_with_args(env, STAGE, "calendar", None, ["cal_exam_day"])
        and exam_booking_state(env)
        and exam_calendar_confirmed(env)
        and workspace_contains(
            env,
            "final_review.md",
            [["authorization_to_test_status"], ["received"], ["pearson_vue_status"], ["booked"], ["2026-11-06"], ["building 3"], ["identification"], ["name"], ["route", "transportation"]],
            180,
        )
    )

CHECKS = [("s31_pre_exam_calendar_checked", s31_pre_exam_calendar_checked, 1.0)]
