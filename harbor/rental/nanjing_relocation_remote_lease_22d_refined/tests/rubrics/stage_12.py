"""Stage 12 — cross-check the target's rent against market stats."""
from __future__ import annotations
from ._helpers import MARKET_BAND_HI, MARKET_BAND_LO, TARGET_COMMUNITY, TARGET_LISTING, agent_used_tool, file_has, has_any, listing_price_minor, market_avg_minor, stage_corpus, tool_call_arg_has

def s12_market_cross_check(env) -> bool:
    called = agent_used_tool(env, 'listing_platform', 'get_market_stats', stage=12)
    avg = market_avg_minor(env, TARGET_COMMUNITY)
    price = listing_price_minor(env, TARGET_LISTING)
    band_ok = avg is not None and price is not None and MARKET_BAND_LO * avg <= price <= MARKET_BAND_HI * avg
    judged = has_any(stage_corpus(env, 12), ['market price', 'average price', 'market average', 'inflated', 'deviation', 'compare with market', 'market price'])
    return called and band_ok and judged

def s12_market_near_misses_compared(env) -> bool:
    target = tool_call_arg_has(env, 'listing_platform', 'get_market_stats', [TARGET_COMMUNITY], stage=12)
    high = tool_call_arg_has(env, 'listing_platform', 'get_market_stats', ['Xuri Shangcheng'], stage=12)
    cheap_or_other = tool_call_arg_has(env, 'listing_platform', 'get_market_stats', ['Hongyang Plaza Apartments'], stage=12) or tool_call_arg_has(env, 'listing_platform', 'get_market_stats', ['Jiangshan Hui'], stage=12)
    avg = market_avg_minor(env, TARGET_COMMUNITY)
    price = listing_price_minor(env, TARGET_LISTING)
    target_band = avg is not None and price is not None and MARKET_BAND_LO * avg <= price <= MARKET_BAND_HI * avg
    durable = file_has(env, 'audit_journal.md', ['Mingfa', 'Xuri', 'average price', 'inflated'], minimum=3)
    return target and high and cheap_or_other and target_band and durable
CHECKS = [('s12_market_cross_check', s12_market_cross_check, 0.1863799283154122), ('s12_market_near_misses_compared', s12_market_near_misses_compared, 0.1863799283154122)]
