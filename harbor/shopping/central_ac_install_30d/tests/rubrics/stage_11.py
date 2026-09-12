"""Stage 11 checks — atomic Checker definitions and weights are in this module。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s11_decision(env) -> bool:
    """Update the decision using the actual third-party inspection report."""
    text = H.scoped_text(env, ['decision', 'gear', 'evidence'], idx=11)
    return (
        H._count_any(text, ['qi-sz-0625', 'drainage slope', 'refrigerant pipe', 'quality report']) >= 2
        and H._count_any(text, ['224', 'partial refund', 'platform review', 'continue submitting evidence', 'recommendation', 'rationale']) >= 3
    )


CHECKS = guard_stage_checks(11, [
    ("s11_decision", s11_decision, 4.0),
])
