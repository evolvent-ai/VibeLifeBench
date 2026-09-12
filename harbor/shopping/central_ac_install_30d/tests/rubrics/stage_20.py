"""Stage 20 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s20_servers(env) -> bool:
    """L1: stage 20 must reconcile card posting and platform notification."""
    if not H._stage_servers_correct(env, 20, min_count=2):
        return False
    return H._stage_server_order_ok(env, 20, ['credit_card', 'notification_hub'])


def s20_result(env) -> bool:
    """Require the ¥224 compensation posting in the budget and credit-card backend."""
    text = H.scoped_text(env, ['budget', 'summary'], idx=20)
    semantic = (
        H._count_any(text, ['refund adjustment', 'credited', 'refunded', 'net spend', 'reconciliation']) >= 3
        and H._count_any(text, ['224', 'tx_iscac_pp']) >= 2
    )
    posted = H._backend_reversal_present(env, 'card_iscac_01', amount_minor=-22400)
    return semantic and posted is True


CHECKS = guard_stage_checks(20, [
    ("s20_servers", s20_servers, 0.5),
    ("s20_result", s20_result, 2.5),
])
