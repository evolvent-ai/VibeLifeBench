"""Stage 15 rubric — explicit CHECKS literal (platform-static-parseable)."""
from __future__ import annotations

from .stage_specs import STAGE_SPECS as _S
from .stage_specs import _make_check as _mk

s15_dispute_filed_before_deadline = _mk(15, _S[15][0])
s15_claim_amount_stated_for_user_decision = _mk(15, _S[15][1])

CHECKS = [
    ("s15_dispute_filed_before_deadline", s15_dispute_filed_before_deadline, 2.0),
    ("s15_claim_amount_stated_for_user_decision", s15_claim_amount_stated_for_user_decision, 1.0),
]
