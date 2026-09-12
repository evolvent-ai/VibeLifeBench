"""Stage 21: final ticketing must match authorization, backend state, and the price-drop option."""
from __future__ import annotations

from ._helpers import _call_json, _flight_bookings, _tool_calls, _workspace_file_text


def _ticketed_details(env) -> list[dict]:
    details: list[dict] = []
    for row in _flight_bookings(env, status="TICKETED"):
        pnr = row.get("pnr")
        if not pnr:
            continue
        detail = _call_json(env, "flight_booking", "get_booking", pnr=pnr)
        if isinstance(detail, dict):
            details.append(detail)
    return details


def _created_offer_ids(env) -> set[str]:
    ids: set[str] = set()
    for call in _tool_calls(env, 21):
        name = str(call.get("name") or "").lower().replace("-", "_")
        args = call.get("arguments") or {}
        payment = args.get("payment") or {}
        method = str(payment.get("method") or "").upper() if isinstance(payment, dict) else ""
        if (
            call.get("success") is True
            and name.endswith("create_booking")
            and args.get("hold") is False
            and args.get("offer_id") == "of_kansai_price_drop_20261008"
            and method in {"CARD", "POINTS", "TOKEN"}
        ):
            ids.add(str(args["offer_id"]))
    return ids


def s21_ticketing_call_matches_persisted_booking(env) -> bool:
    offer_ids = _created_offer_ids(env)
    if not offer_ids:
        return False
    for detail in _ticketed_details(env):
        history = " ".join(str(item.get("detail") or "") for item in detail.get("history") or [])
        if any(f"offer={offer_id}" in history for offer_id in offer_ids):
            return True
    return False


def s21_ticketed_state_is_mu737_daytime_price_drop(env) -> bool:
    for detail in _ticketed_details(env):
        segments = detail.get("segments") or []
        passengers = detail.get("passengers") or []
        paid = ((detail.get("total_paid") or {}).get("amount"))
        correct_segment = any(
            seg.get("flight_no") == "MU737"
            and str(seg.get("depart_dt") or "").startswith("2026-10-12T10:00")
            for seg in segments
        )
        if correct_segment and len(passengers) == 3 and isinstance(paid, (int, float)) and 0 < float(paid) <= 9540:
            return True
    return False


def s21_ticket_and_budget_register_are_object_specific(env) -> bool:
    bookings = _workspace_file_text(env, "booking_register.md").lower()
    budget = _workspace_file_text(env, "budget_ledger.md").lower()
    return (
        "mu737" in bookings
        and any(word in bookings for word in ("ticketed", "ticket issued"))
        and any(word in bookings for word in ("authorization", "authorized", "approved"))
        and "9540" in (bookings + budget)
        and any(word in budget for word in ("42000", "42,000"))
        and any(word in budget for word in ("remaining", "balance", "unspent"))
    )


CHECKS = [
    ("s21_ticketing_call_matches_persisted_booking", s21_ticketing_call_matches_persisted_booking, 2.0),
    ("s21_ticketed_state_is_mu737_daytime_price_drop", s21_ticketed_state_is_mu737_daytime_price_drop, 2.0),
    ("s21_ticket_and_budget_register_are_object_specific", s21_ticket_and_budget_register_are_object_specific, 1.0),
]
