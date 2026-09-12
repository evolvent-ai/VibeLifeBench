"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

def s08_redacted_external_reply(env):
    return _mk(8, _S[8][0])(env)


def s08_no_external_sensitive_leak(env):
    return _mk(8, _S[8][1])(env)

CHECKS = [
    ('s08_redacted_external_reply', s08_redacted_external_reply, 5.0),
    ('s08_no_external_sensitive_leak', s08_no_external_sensitive_leak, 5.0),
]
