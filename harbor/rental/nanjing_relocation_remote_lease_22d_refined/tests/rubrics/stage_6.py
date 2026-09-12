"""Stage 6 — re-check reputation after the merchant profile update."""
from __future__ import annotations
from ._helpers import DOWNGRADED_MERCHANT, file_has, merchant_rating_tenths, merchant_tags, tool_call_arg_has


def s6_reputation_recheck_after_drop(env) -> bool:
    rechecked = tool_call_arg_has(env, 'review_platform', 'get_merchant', [DOWNGRADED_MERCHANT], stage=6)
    rt = merchant_rating_tenths(env, DOWNGRADED_MERCHANT)
    backend_ok = rt == 33 and 'platform verified' not in merchant_tags(env, DOWNGRADED_MERCHANT)
    durable = file_has(env, 'audit_journal.md', ['Li Qiang', '4.4', '3.3', 'verification removed'], minimum=3)
    return rechecked and backend_ok and durable

CHECKS = [('s6_reputation_recheck_after_drop', s6_reputation_recheck_after_drop, 3.727598566308244)]
