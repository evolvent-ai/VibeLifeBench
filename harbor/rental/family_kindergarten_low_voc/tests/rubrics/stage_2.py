from ._helpers import *

def r038_check_006_kindergarten_route_maps(env) -> bool:
    return bool(
        route_candidates_at_most(env, 2, (C.PL_A, C.PL_B, C.PL_C), C.PL_KG, ('walking', 'bicycling'), 20, min_count=2)
        and workspace_has(env, [C.A, C.B, 'kindergarten_route', '20'], ['rental_tracker.md'])
    )

def r038_check_007_cbd_peak_commute(env) -> bool:
    return bool(
        route_candidates_at_most(env, 2, (C.PL_A, C.PL_B, C.PL_C), C.PL_CBD, ('driving', 'transit'), 60, min_count=2, depart_hour='08:')
        and workspace_has(env, [C.A, C.B, 'cbd_peak_commute', '60'], ['rental_tracker.md'])
    )

CHECKS = [
    ("r038_check_006_kindergarten_route_maps", r038_check_006_kindergarten_route_maps, 1.75),
    ("r038_check_007_cbd_peak_commute", r038_check_007_cbd_peak_commute, 1.75),
]
