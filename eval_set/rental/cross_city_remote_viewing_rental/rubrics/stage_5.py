from __future__ import annotations
from ._helpers import *


def s5_night_shift_recheck(env) -> bool:
    return (
        tool_stage(env, 5, "maps", None, (C.DESTINATION,))
        and tool_stage(env, 5, "calendar", None, ("租房",))
        and calendar_has_event_parts(env, ("租房",))
        and maps_route_available(env, C.PLACE_C, C.DESTINATION)
        and stage_any_structured_evidence(env, 5, [(C.PLACE_C,), (C.LIST_C,), (C.LIST_C_NAME,)])
    )


def s5_roommate_and_elevator_risk(env) -> bool:
    return (
        stage_b_listing_review_email_mapping(env, 5)
        and listing_b_has_private_payment_and_gate_risk(env)
        and review_has(env, C.MER_B, ("锁房款", "服务费"))
        and stage_structured_evidence(env, 5, ("资料", "风险"))
    )


CHECKS = [
    ("s5_night_shift_recheck", s5_night_shift_recheck, 1.5),
    ("s5_roommate_and_elevator_risk", s5_roommate_and_elevator_risk, 1.25),
]
