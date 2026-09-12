"""Stage 2 — search the listing platform from the requirement set."""
from __future__ import annotations
from ._helpers import file_has, tool_calls_matching


def _has_rows(result) -> bool:
    if isinstance(result, list):
        return bool(result)
    if isinstance(result, dict):
        return any(isinstance(result.get(k), list) and bool(result[k]) for k in ('listings','items','results'))
    return False


def s2_search_listings_called(env) -> bool:
    qualified = False
    for call in tool_calls_matching(env, 'listing_platform', 'search_listings', stage=2):
        args = call.get('arguments') or call.get('args') or {}
        city_ok = 'Nanjing' in str(args.get('city') or '')
        rent_ok = str(args.get('category') or '').lower() in {'rent','rental','entire-unit rental'}
        try:
            budget_ok = int(args.get('max_price_minor')) <= 420000
            rooms_ok = int(args.get('min_rooms')) == 1 and int(args.get('max_rooms')) == 2
        except (TypeError, ValueError):
            budget_ok = rooms_ok = False
        if city_ok and rent_ok and budget_ok and rooms_ok and _has_rows(call.get('result')):
            qualified = True
            break
    durable = file_has(env, 'candidates.md', ['lst_njr_0500','lst_njr_0518','lst_njr_0519','4200'], minimum=3)
    return qualified and durable

CHECKS = [('s2_search_listings_called', s2_search_listings_called, 0.1863799283154122)]
