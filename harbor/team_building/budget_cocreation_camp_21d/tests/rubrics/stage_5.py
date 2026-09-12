"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s05_group_plan_created = _mk(5, _S[5][0])
s05_action_owner_shell = _mk(5, _S[5][1])

CHECKS = [
    ('s05_group_plan_created', s05_group_plan_created, 1.5),
    ('s05_action_owner_shell', s05_action_owner_shell, 1.25),
]
