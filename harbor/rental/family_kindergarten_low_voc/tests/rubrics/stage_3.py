from ._helpers import *

def r038_check_027_scheduled_checks(env) -> bool:
    return bool(
        tool_stage_result_has(env, 3, 'listing_platform', 'get_listing', [C.A], [C.A, 'active'])
        and tool_stage_result_has(env, 3, 'listing_platform', 'get_listing', [C.B], [C.B, 'active'])
        and workspace_has(env, [C.A, C.B, 'last_checked', 'stage_3'], ['rental_tracker.md'])
    )

CHECKS = [
    ("r038_check_027_scheduled_checks", r038_check_027_scheduled_checks, 1.25),
]
