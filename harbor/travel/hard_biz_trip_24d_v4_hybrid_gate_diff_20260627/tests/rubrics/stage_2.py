"""Stage 2: hotel search - persist comparable hotels, prices, and refund analysis."""
from __future__ import annotations
from loguru import logger
from ._helpers import _amount_in_text, _any, _agent_used_tool, _successful_tool_results, _workspace_file_text


def _searched_hotel_rows(env) -> list[dict]:
    rows: list[dict] = []
    for result in _successful_tool_results(env, "hotel_booking", "search_hotels", stage=2):
        # The live mock returns {"items": [...]}; accept either key so the
        # check does not depend on an alias only the reference solution injects.
        if isinstance(result, list):
            candidates = result
        elif isinstance(result, dict):
            candidates = result.get("results") or result.get("hotels") or result.get("items") or []
        else:
            candidates = []
        rows.extend(row for row in candidates if isinstance(row, dict))
    return rows


def _hotel_result(rows: list[dict], hotel_ids: set[str], names: list[str]) -> dict | None:
    """Pick the searched row by id, else by the most specific name phrase.

    Name aliases are prefixes of one another ("roppongi" vs "roppongi
    business hotel"), so a loose substring match can land on a decoy row
    (e.g. "Roppongi Capsule Inn"); the longest matching phrase wins.
    """
    best: tuple[int, dict] | None = None
    for row in rows:
        blob = f"{row.get('hotel_id') or ''} {row.get('name') or ''}".lower()
        if str(row.get("hotel_id") or "") in hotel_ids:
            return row
        matched = max((len(str(w)) for w in names if str(w).lower() in blob), default=0)
        if matched and (best is None or matched > best[0]):
            best = (matched, row)
    return best[1] if best else None


def _comparison_rows(env) -> tuple[dict | None, dict | None]:
    rows = _searched_hotel_rows(env)
    roppongi = _hotel_result(rows, {"hotel_roppongi_biz"}, ["roppongi business hotel", "roppongi"])
    comparator = _hotel_result(rows, {"hotel_shinagawa_value", "hotel_ariake_bay", "hotel_narita_transit"}, ["shinagawa", "ariake", "narita"])
    return roppongi, comparator


def s2_must_name_hotels(env) -> bool:
    text = (_workspace_file_text(env, "/workspace/decision_log.md") + "\n" + _workspace_file_text(env, "/workspace/budget.md")).lower()
    roppongi, comparator = _comparison_rows(env)
    has_names = isinstance(roppongi, dict) and isinstance(comparator, dict) and _any(text, [str(roppongi.get("name") or ""), str(roppongi.get("hotel_id") or "")]) and _any(text, [str(comparator.get("name") or ""), str(comparator.get("hotel_id") or "")])
    prices = [row.get("nightly_price_from") for row in (roppongi, comparator) if isinstance(row, dict)]
    has_price = len(prices) == 2 and all(isinstance(x, (int, float)) and _amount_in_text(text, int(x)) for x in prices) and _any(text, ["jpy"])
    has_refund = _any(text, ["flex", "prepaid", "refundable", "non-refundable", "approval"])
    policy_split = isinstance(roppongi, dict) and isinstance(comparator, dict) and isinstance(roppongi.get("refundable"), bool) and isinstance(comparator.get("refundable"), bool) and roppongi.get("refundable") is not comparator.get("refundable")
    ok = has_names and has_price and has_refund and policy_split
    logger.info(f"s2_must: names={has_names} price={has_price} refund={has_refund} split={policy_split} -> {ok}")
    return ok


def s2_tool_used(env) -> bool:
    roppongi, comparator = _comparison_rows(env)
    ok = _agent_used_tool(env, "hotel_booking", "search_hotels", stage=2) and isinstance(roppongi, dict) and isinstance(comparator, dict)
    logger.info(f"s2_tool_backend_results: {ok}")
    return ok


CHECKS = [("s2_must_name_hotels", s2_must_name_hotels, 2.5), ("s2_tool_used", s2_tool_used, 1.0)]
