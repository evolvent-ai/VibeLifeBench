"""Stage 18 — re-check listing status after a silent delist (M1)."""
from __future__ import annotations
from ._helpers import DELISTED_DECOY, TARGET_LISTING, agent_used_any_tool, file_has, listing_status, tool_call_arg_has

def s18_status_recheck_after_delist(env) -> bool:
    rechecked = tool_call_arg_has(env, 'listing_platform', 'get_listing', [DELISTED_DECOY], stage=18) or tool_call_arg_has(env, 'listing_platform', 'get_listing_detail', [DELISTED_DECOY], stage=18) or agent_used_any_tool(env, [('listing_platform', 'search_listings')], stage=18)
    decoy_status = listing_status(env, DELISTED_DECOY)
    backend_ok = decoy_status == 'delisted'
    tgt_status = listing_status(env, TARGET_LISTING)
    tgt_ok = tgt_status == 'active'
    durable = file_has(env, 'audit_journal.md', ['Venice Water City', 'delisted', 'Mingfa', 'active'], minimum=3) or file_has(env, 'audit_journal.md', [DELISTED_DECOY, 'delisted', TARGET_LISTING], minimum=2)
    return rechecked and backend_ok and tgt_ok and durable
CHECKS = [('s18_status_recheck_after_delist', s18_status_recheck_after_delist, 0.1863799283154122)]
