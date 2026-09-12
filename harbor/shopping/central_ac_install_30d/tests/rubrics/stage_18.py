"""Stage 18 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s18_servers(env) -> bool:
    """L1: stage 18 must query the expected MCP server."""
    if not H._stage_servers_correct(env, 18, min_count=1):
        return False
    return True


def s18_result(env) -> bool:
    """Require persisted dispute resolution plus real backend approval and reversal."""
    text = H.scoped_text(env, ['budget', 'decision', 'tracker'], idx=18)
    semantic = (
        H._count_any(text, ['dispute', 'approved', 'reversal', 'reversed', 'amount due', '216']) >= 3
        and H._count_any(text, ['tx_iscac_rev']) >= 1
    )
    dispute = H._backend_dispute_status_is(env, 'card_iscac_01', 'disp_iscac_01', 'approved')
    reversal = H._backend_reversal_present(env, 'card_iscac_01', amount_minor=-21600)
    return semantic and dispute is True and reversal is True


CHECKS = guard_stage_checks(18, [
    ("s18_servers", s18_servers, 0.5),
    ("s18_result", s18_result, 2.0),
])
