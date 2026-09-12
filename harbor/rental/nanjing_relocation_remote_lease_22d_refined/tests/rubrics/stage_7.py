"""Stage 7 — pull owner/property identity from the listing detail."""
from __future__ import annotations
from ._helpers import TARGET_LISTING, TARGET_OWNER, agent_used_tool, file_has, has_any, listing_attr, stage_corpus, tool_call_arg_has

def s7_owner_identity_pulled(env) -> bool:
    pulled = agent_used_tool(env, 'listing_platform', 'get_listing_detail', stage=7)
    noted = has_any(stage_corpus(env, 7), ['property owner', 'property certificate', 'owner name'])
    return pulled and noted

def s7_target_owner_exact_recorded(env) -> bool:
    pulled_target = tool_call_arg_has(env, 'listing_platform', 'get_listing_detail', [TARGET_LISTING], stage=7)
    owner = listing_attr(env, TARGET_LISTING, 'property owner name')
    cert = listing_attr(env, TARGET_LISTING, 'property-certificate number')
    durable = file_has(env, 'audit_journal.md', [TARGET_LISTING, str(owner), 'property certificate'], minimum=2) or file_has(env, 'audit_journal.md', ['Mingfa', str(owner), 'property certificate'], minimum=3)
    return pulled_target and str(owner) == TARGET_OWNER and bool(cert) and durable
CHECKS = [('s7_owner_identity_pulled', s7_owner_identity_pulled, 0.1863799283154122), ('s7_target_owner_exact_recorded', s7_target_owner_exact_recorded, 3.727598566308244)]
