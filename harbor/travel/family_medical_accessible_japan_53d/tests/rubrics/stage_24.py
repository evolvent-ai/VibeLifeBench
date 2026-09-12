from __future__ import annotations

import re

from ._helpers import _flight_booking_details, _hotel_reservation_details, _workspace_file_exists, _workspace_file_text, money_fact, text_has


def _amount(text: str, labels: tuple[str, ...]) -> float | None:
    number = r"([0-9][0-9,]*(?:\.[0-9]+)?)"
    for label in labels:
        match = re.search(rf"{label}.{{0,40}}?{number}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
        match = re.search(rf"{number}.{{0,24}}?{label}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def s24_final_archive_created(env):
    return _workspace_file_exists(env, "final_archive.md")


def s24_actual_budget_and_receipts(env):
    text = _workspace_file_text(env, "final_archive.md")
    cap = _amount(text, (r"budget\s*cap", r"cap", r"budget ceiling", r"maximum budget"))
    actual = _amount(text, (r"actual\s*cny\s*(?:trip\s*)?total", r"cny\s*actual\s*(?:trip\s*)?total", r"actual\s*spend\s*cny"))
    remaining = _amount(text, (r"remaining\s*cny\s*budget", r"cny\s*budget\s*remaining", r"unspent\s*cny\s*budget"))
    flights = [detail for detail in _flight_booking_details(env, status="TICKETED") if detail.get("status") == "TICKETED"]
    hotels = _hotel_reservation_details(env)
    if len(flights) != 1 or len(hotels) != 1:
        return False
    paid = flights[0].get("total_paid") or {}
    cny_actual = float(paid.get("amount") or 0) if paid.get("currency") == "CNY" else 0.0
    cny_actual += sum(float(hotel.get("total_charged") or 0) for hotel in hotels if hotel.get("currency") == "CNY")
    line_items = money_fact(text, str(flights[0].get("pnr") or ""), paid.get("amount") or 0, str(paid.get("currency") or "")) and all(money_fact(text, str(hotel.get("reservation_id") or ""), hotel.get("total_charged") or 0, str(hotel.get("currency") or "")) for hotel in hotels)
    separate_currency = all(hotel.get("currency") == "CNY" for hotel in hotels) or text_has(text, [["separate currency", "separate-currency", "separately"], ["no fx conversion", "not converted", "without conversion"]])
    receipt_index = any(x in text for x in ("receipt index", "receipt list", "indexed receipts", "receipt inventory", "evidence index"))
    receipt_types = text_has(text, [["flight", "airfare", "mu737"], ["hotel", "lodging", "accommodation"], ["insurance", "travel insurance"]])
    return bool(cap == 42000 and actual == cny_actual > 0 and remaining == cap - actual and actual + remaining == cap and line_items and separate_currency and receipt_index and receipt_types)


def s24_status_and_reimbursement_closeout(env):
    text = _workspace_file_text(env, "final_archive.md")
    return text_has(text, [["confirmed", "confirmation"], ["refunded", "refund"], ["cancellation deadline", "cancellation cutoff", "cancel-by deadline"], ["pending", "handoff"], ["reimbursement", "fee"], ["owner", "responsible"], ["next action", "action"]])


CHECKS = [("s24_final_archive_created", s24_final_archive_created, 0.5), ("s24_actual_budget_and_receipts", s24_actual_budget_and_receipts, 1.0), ("s24_status_and_reimbursement_closeout", s24_status_and_reimbursement_closeout, 1.0)]
