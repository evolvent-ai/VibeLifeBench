from ._helpers import exam_booking_state, exam_calendar_confirmed, used_all_tools, workspace_contains

STAGE = 30

def s30_admission_checklist_created(env) -> bool:
    return (
        used_all_tools(env, STAGE, [("notification_hub", None), ("calendar", None)])
        and exam_booking_state(env)
        and exam_calendar_confirmed(env)
        and workspace_contains(
            env,
            "official_evidence_log.md",
            [["appointment"], ["confirmation", "booked"], ["2026-11-06"], ["building 3"], ["identification"], ["name"], ["route", "transportation"], ["authorization to test", "att"]],
            360,
        )
    )

CHECKS = [("s30_admission_checklist_created", s30_admission_checklist_created, 1.25)]
