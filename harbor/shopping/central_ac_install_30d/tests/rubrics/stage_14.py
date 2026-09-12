"""Stage 14 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s14_servers(env) -> bool:
    """L1: stage 14 must query the expected MCP server."""
    if not H._stage_servers_correct(env, 14, min_count=1):
        return False
    return True


def s14_result(env) -> bool:
    """Require both keyword groups in the persisted decision."""
    text = H.scoped_text(env, ['decision', 'budget', 'risk'], idx=14)
    return (
        H._count_any(text, ['dispute', 'under review', 'due date', 'amount due', 'separate', 'regular payment', '7/10']) >= 3
        and H._count_any(text, ['disp_iscac_01']) >= 1
    )


def s14_no_bad(env) -> bool:
    """Require an explicit repayment boundary while the dispute remains under review."""
    text = H.scoped_text(env, ['decision', 'risk'], idx=14)
    recorded = H._count_any(text, ['dispute', 'under review', 'regular payment', 'due date', 'amount due']) >= 2
    return recorded and not H._has_bad_advice(text, ['do not pay because of a dispute', 'no payment first', 'stop payment'])


CHECKS = guard_stage_checks(14, [
    ("s14_servers", s14_servers, 0.5),
    ("s14_result", s14_result, 3.0),
    ("s14_no_bad", s14_no_bad, 0.5),
])
