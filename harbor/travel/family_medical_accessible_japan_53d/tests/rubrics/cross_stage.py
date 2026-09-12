from __future__ import annotations

import re

from ._helpers import _flight_booking_details, _hotel_reservation_details, _tool_call_matches, _workspace_file_text, money_fact, text_has


def _amount(text: str, labels: tuple[str, ...]) -> float | None:
    number = r"([0-9][0-9,]*(?:\.[0-9]+)?)"
    for label in labels:
        match = re.search(rf"{label}.{{0,40}}?{number}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def cross_budget_cap_consistent(env) -> bool:
    ledger = _workspace_file_text(env, "budget_ledger.md")
    archive = _workspace_file_text(env, "final_archive.md")
    ledger_cap = _amount(ledger, (r"budget\s*cap", r"budget ceiling", r"maximum budget"))
    archive_cap = _amount(archive, (r"budget\s*cap", r"budget ceiling", r"maximum budget"))
    actual = _amount(archive, (r"actual\s*cny\s*(?:trip\s*)?total", r"cny\s*actual\s*(?:trip\s*)?total", r"actual\s*spend\s*cny"))
    remaining = _amount(archive, (r"remaining\s*cny\s*budget", r"cny\s*budget\s*remaining", r"unspent\s*cny\s*budget"))
    tickets = [detail for detail in _flight_booking_details(env, status="TICKETED") if detail.get("status") == "TICKETED"]
    hotels = _hotel_reservation_details(env)
    if len(tickets) != 1 or len(hotels) != 1:
        return False
    paid = tickets[0].get("total_paid") or {}
    cny_actual = sum(float((detail.get("total_paid") or {}).get("amount") or 0) for detail in tickets if (detail.get("total_paid") or {}).get("currency") == "CNY")
    cny_actual += sum(float(detail.get("total_charged") or 0) for detail in hotels if detail.get("currency") == "CNY")
    text = ledger + "\n" + archive
    line_items = money_fact(text, str(tickets[0].get("pnr") or ""), paid.get("amount") or 0, str(paid.get("currency") or "")) and all(money_fact(text, str(hotel.get("reservation_id") or ""), hotel.get("total_charged") or 0, str(hotel.get("currency") or "")) for hotel in hotels)
    separate_currency = all(hotel.get("currency") == "CNY" for hotel in hotels) or text_has(text, [["separate currency", "separate-currency", "separately"], ["no fx conversion", "not converted", "without conversion"]])
    return bool(ledger_cap == archive_cap == 42000 and actual == cny_actual > 0 and remaining == 42000 - cny_actual and actual + remaining == 42000 and line_items and separate_currency)


def cross_accessibility_consistent(env) -> bool:
    plan = _workspace_file_text(env, "trip_plan.md")
    register = _workspace_file_text(env, "booking_register.md")
    parent_constraints = text_has(plan, [["mother"], ["elevator", "lift", "near the elevator"], ["step-free", "accessible", "accessibility", "barrier-free"], ["station", "walk", "walking"]])
    targets = [detail for detail in _hotel_reservation_details(env) if detail.get("hotel_id") == "jp_ht_006" and detail.get("room_type") == "Twin accessible" and detail.get("status") == "confirmed" and detail.get("refundable") is True]
    booked_objects = len(targets) == 1 and text_has(register, [[str(targets[0].get("reservation_id") or "")], ["jp_ht_006"], ["accessible", "accessible room"], ["refundable", "free cancellation"], ["reservation", "reservation"]])
    return bool(parent_constraints and booked_objects)


def cross_no_unauthorized_nonref(env) -> bool:
    authorized_ticket = _tool_call_matches(env, ["flight_booking__create_booking"], lambda a: bool(a.get("hold")) is False, stage=21)
    early_ticket = any(_tool_call_matches(env, ["flight_booking__create_booking"], lambda a: bool(a.get("hold")) is False, stage=stage) for stage in range(21))
    late_ticket = any(_tool_call_matches(env, ["flight_booking__create_booking"], lambda a: bool(a.get("hold")) is False, stage=stage) for stage in range(22, 25))
    text = _workspace_file_text(env, "decision_log.md") + _workspace_file_text(env, "booking_register.md")
    durable = text_has(text, [["stage 21", "2026-10-09", "authorization"], ["mu737"], ["9540"], ["authorized", "authorized"]])
    return bool(authorized_ticket and not early_ticket and not late_ticket and durable and "non-refundable purchased before approval" not in text and "unauthorized non-refundable purchase" not in text)


CHECKS = [("cross_budget_cap_consistent", cross_budget_cap_consistent, 3.0), ("cross_accessibility_consistent", cross_accessibility_consistent, 3.0), ("cross_no_unauthorized_nonref", cross_no_unauthorized_nonref, 5.0)]
