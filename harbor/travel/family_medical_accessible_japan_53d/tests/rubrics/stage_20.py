from __future__ import annotations

from datetime import datetime, timedelta

from ._helpers import _tool_call_matches, _tool_call_results, _workspace_file_text, text_has

OID = "of_kansai_price_drop_20261008"


def s20_fresh_search_and_reprice(env) -> bool:
    return _tool_call_matches(env, ["flight_booking__search_flights"], lambda a: a.get("origin") == "PVG" and a.get("destination") == "KIX" and a.get("departure_date") == "2026-10-12" and a.get("adults") == 3, 20) and _tool_call_matches(env, ["flight_booking__price_offer"], lambda a: a.get("offer_id") == OID, 20) and _tool_call_matches(env, ["flight_booking__get_flight_offer"], lambda a: a.get("offer_id") == OID, 20)


def s20_backend_offer_exact(env) -> bool:
    priced = _tool_call_results(env, ["flight_booking__price_offer"], lambda a: a.get("offer_id") == OID, 20)
    details = _tool_call_results(env, ["flight_booking__get_flight_offer"], lambda a: a.get("offer_id") == OID, 20)
    valid_prices = []
    for row in priced:
        if not isinstance(row, dict) or row.get("offer_id") != OID or (row.get("priced_total") or {}).get("amount") != 9540 or (row.get("priced_total") or {}).get("currency") != "CNY":
            continue
        try:
            priced_at = datetime.fromisoformat(str(row.get("priced_at") or ""))
            guarantee = datetime.fromisoformat(str(row.get("price_guarantee_until") or ""))
        except ValueError:
            continue
        if guarantee == priced_at + timedelta(minutes=10):
            valid_prices.append(row)
    detail_ok = any(isinstance(detail, dict) and detail.get("offer_id") == OID and (detail.get("total_price") or {}).get("amount") == 9540 and (detail.get("total_price") or {}).get("currency") == "CNY" and any(s.get("flight_no") == "MU737" and s.get("origin") == "PVG" and s.get("destination") == "KIX" and str(s.get("depart_dt", "")).startswith("2026-10-12T10:00") and (s.get("fare_rules") or {}).get("refundable") is True for s in detail.get("segments") or []) for detail in details)
    log = _workspace_file_text(env, "decision_log.md")
    durable = any(text_has(log, [[OID], ["9540"], [str(row["price_guarantee_until"]).lower()], ["refundable", "eligible for refund"]]) for row in valid_prices)
    return bool(valid_prices and detail_ok and durable)


def s20_decision_supersedes_stale_offer(env) -> bool:
    text = _workspace_file_text(env, "decision_log.md")
    return text_has(text, [[OID], ["9540"], ["mu737"], ["daytime", "daytime nonstop flight"], ["refundable", "eligible for refund"], ["of_kansai_daytime_refundable_hold"], ["12840"], ["superseded", "stale", "old quote", "replaced"], ["owner", "responsible owner"], ["next action", "following action"]])


CHECKS = [("s20_fresh_search_and_reprice", s20_fresh_search_and_reprice, 0.5), ("s20_backend_offer_exact", s20_backend_offer_exact, 1.0), ("s20_decision_supersedes_stale_offer", s20_decision_supersedes_stale_offer, 0.5)]
