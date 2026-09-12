"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

_s21_final_handoff_complete = _mk(21, _S[21][0])
s21_terminal_state_safe = _mk(21, _S[21][1])


def s21_final_handoff_complete(env):
    return _s21_final_handoff_complete(env)

CHECKS = [
    ('s21_final_handoff_complete', s21_final_handoff_complete, 2.0),
    ('s21_terminal_state_safe', s21_terminal_state_safe, 2.0),
]
