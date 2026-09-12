from ._helpers import *


def r038_check_008_poi_child_context(env) -> bool:
    clinic = (
        tool_stage_result_has(env, 6, 'maps', 'search_places', result_parts=['pl_binjiang_night_clinic', 'clinic'])
        or tool_stage_result_has(env, 6, 'maps', 'search_places', result_parts=['pl_children_clinic', 'clinic'])
    )
    family_facility = (
        tool_stage_result_has(env, 6, 'maps', 'search_places', result_parts=['pl_jianghan_indoor_play', 'sports_center'])
        or tool_stage_result_has(env, 6, 'maps', 'search_places', result_parts=['pl_baima_lake_park', 'park'])
        or tool_stage_result_has(env, 6, 'maps', 'search_places', result_parts=['pl_puyan_family_restroom', 'public_service'])
    )
    return bool(
        clinic
        and family_facility
        and (
            state_evidence(env, 6, [C.B, 'pl_binjiang_night_clinic'], ['rental_tracker.md', 'child_safety_checklist.md'])
            or state_evidence(env, 6, [C.B, 'pl_children_clinic'], ['rental_tracker.md', 'child_safety_checklist.md'])
        )
        and (
            state_evidence(env, 6, [C.B, 'pl_jianghan_indoor_play'], ['rental_tracker.md', 'child_safety_checklist.md'])
            or state_evidence(env, 6, [C.B, 'pl_baima_lake_park'], ['rental_tracker.md', 'child_safety_checklist.md'])
            or state_evidence(env, 6, [C.B, 'pl_puyan_family_restroom'], ['rental_tracker.md', 'child_safety_checklist.md'])
        )
        and no_external_side_effect(env)
    )


CHECKS = [
    ("r038_check_008_poi_child_context", r038_check_008_poi_child_context, 1.25),
]
