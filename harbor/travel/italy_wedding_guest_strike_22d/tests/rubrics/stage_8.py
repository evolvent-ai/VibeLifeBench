from __future__ import annotations

from ._helpers import *

def s8_rail_strike_rechecked(env) -> bool:
    return (trace_any(env, 8, [(S_RAIL, "get_train_status", [["FR9403"], ["2026-09-11"]])]) and rail_status_is(env, "FR9403", "2026-09-11", "STRIKE_NOTICE", 240))

def s8_strike_recorded_no_stale_lock(env) -> bool:
    # Mutation follow-up context: rail_booking; cross-service with calendar and maps buffers.
    return (trace_any(env, 8, [(S_RAIL, "get_train_status", [["FR9403"], ["2026-09-11"]])]) and backend_rail_strike_state(env) and evidence_recorded(env, [["FR9403"], ["strike", "labor", "disruption"], ["240", "delay"]]))

CHECKS = [
    ("s8_strike_recorded_no_stale_lock", s8_strike_recorded_no_stale_lock, 1.0),
]
