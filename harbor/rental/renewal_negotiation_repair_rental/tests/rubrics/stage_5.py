from __future__ import annotations
from ._helpers import *

def s5_family_schedule_backfill(env) -> bool:
    return bool(
        tool_stage(env, 5, 'calendar', None, ('family', 'internal'))
        and calendar_has_event_parts(env, ('family', 'internal'), '2026-07-17T00:00:00+08:00', '2026-08-01T00:00:00+08:00')
        and derived_stage_has(env, 5, ('family', 'repair', 'deposit'), ('CANDIDATE_TRACKER.md', 'AUTH_LOG.md'))
    )

def s5_deposit_and_repair_risk_backfilled(env) -> bool:
    return bool(
        email_message_has(env, '101', ('existing deposit', 'water heater', 'dampness'))
        and derived_stage_has(env, 5, (C.LIST_A, 'deposit', 'repair', 'written', 'pending confirmation'), ('RISK_LOG.md', 'LEASE_CHECKLIST.md', 'AUTH_LOG.md'))
    )

CHECKS = [
    ("s5_family_schedule_backfill", s5_family_schedule_backfill, 1.5),
    ("s5_deposit_and_repair_risk_backfilled", s5_deposit_and_repair_risk_backfilled, 1.25),
]
