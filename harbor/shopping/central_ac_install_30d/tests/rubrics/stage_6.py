"""Stage 6 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s6_servers(env) -> bool:
    """L1: stage 6 must query the expected MCP server."""
    if not H._stage_servers_correct(env, 6, min_count=1):
        return False
    return True


def s6_args(env) -> bool:
    """L2: stage 6 tool arguments must reference expected entities."""
    return H._stage_tool_args_reference(env, 6, ['card_iscac_01', 'tx_iscac_fx', '2074'], min_count=1)


def s6_result(env) -> bool:
    """Require both keyword groups in the persisted decision."""
    text = H.scoped_text(env, ['budget', 'decision', 'risk'], idx=6)
    return (
        H._count_any(text, ['paypal', 'overseas purchase', 'US dollars', 'foreign currency']) >= 1
        and H._count_any(text, ['216']) >= 1
        and H._count_any(text, ['foreign currency', 'exchange rate', 'pending posting', 'reconcile', 'normal']) >= 1
    )


CHECKS = guard_stage_checks(6, [
    ("s6_servers", s6_servers, 0.5),
    ("s6_args", s6_args, 0.5),
    ("s6_result", s6_result, 1.5),
])
