"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s16_budget_camp_calendar_created = _mk(16, _S[16][0])
s16_action_followups_calendar = _mk(16, _S[16][1])

CHECKS = [
    ('s16_budget_camp_calendar_created', s16_budget_camp_calendar_created, 1.75),
    ('s16_action_followups_calendar', s16_action_followups_calendar, 1.5),
]
