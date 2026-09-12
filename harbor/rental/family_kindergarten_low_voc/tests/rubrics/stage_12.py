from ._helpers import *


def r038_check_021_mutation_kindergarten_calendar(env) -> bool:
    return bool(
        kindergarten_schedule_backend_ready(env)
        and tool_stage_result_has(env, 12, 'email', None, result_parts=['msg_kindergarten_changed'])
        and tool_stage_result_has(
            env, 12, 'calendar', None,
            result_parts=['cal_evt_kindergarten_intro', '2026-08-12T09:30', '2026-08-12T11:00'],
        )
        and state_evidence(env, 12, ['kindergarten', 'August 12', '09:30', '11:00'], ['rental_tracker.md', 'moving_plan.md'])
        and state_evidence(env, 12, ['pickup/drop-off drill', 'separately notified'], ['rental_tracker.md', 'moving_plan.md'])
        and no_calendar_write(env)
    )


def r038_check_026_calendar_conflict_stage12(env) -> bool:
    return bool(
        kindergarten_schedule_backend_ready(env)
        and tool_stage_result_has(
            env, 12, 'calendar', None,
            result_parts=['cal_evt_kindergarten_intro', '2026-08-12T09:30', '2026-08-12T11:00'],
        )
        and state_evidence(env, 12, ['information session', '09:30', '11:00', 'schedule'], ['rental_tracker.md', 'moving_plan.md'])
        and no_calendar_write(env)
    )


CHECKS = [
    ("r038_check_021_mutation_kindergarten_calendar", r038_check_021_mutation_kindergarten_calendar, 1.25),
    ("r038_check_026_calendar_conflict_stage12", r038_check_026_calendar_conflict_stage12, 1.25),
]
