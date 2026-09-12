"""Stage 5 — establish the initial agent/merchant reputation snapshot."""
from __future__ import annotations
from ._helpers import DOWNGRADED_MERCHANT, TARGET_AGENT_MERCHANT, agent_queried_reviews, file_has, merchant_rating_tenths, merchant_tags, tool_call_arg_has


def s5_reputation_queried(env) -> bool:
    return agent_queried_reviews(env, stage=5)


def s5_target_and_decoy_reputation_recorded(env) -> bool:
    target_called = tool_call_arg_has(env, 'review_platform', 'get_merchant', [TARGET_AGENT_MERCHANT], stage=5)
    decoy_called = tool_call_arg_has(env, 'review_platform', 'get_merchant', [DOWNGRADED_MERCHANT], stage=5)
    target_rt = merchant_rating_tenths(env, TARGET_AGENT_MERCHANT)
    decoy_rt = merchant_rating_tenths(env, DOWNGRADED_MERCHANT)
    target_ok = target_rt == 47 and 'platform verified' in merchant_tags(env, TARGET_AGENT_MERCHANT)
    decoy_initial = decoy_rt == 44 and 'platform verified' in merchant_tags(env, DOWNGRADED_MERCHANT)
    durable = file_has(env, 'audit_journal.md', ['Zhou Min', '4.7', 'Li Qiang', '4.4', 'platform verified'], minimum=4)
    return target_called and decoy_called and target_ok and decoy_initial and durable

CHECKS = [('s5_reputation_queried', s5_reputation_queried, 0.1863799283154122), ('s5_target_and_decoy_reputation_recorded', s5_target_and_decoy_reputation_recorded, 3.727598566308244)]
