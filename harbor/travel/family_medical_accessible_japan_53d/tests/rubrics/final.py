"""Final task-level checks: backend truth, durable reconciliation, and retrospective."""
from __future__ import annotations

import re

from ._helpers import (
    WORKSPACE_FILES,
    _call_json,
    _flight_booking_details,
    _hotel_reservation_details,
    _workspace_file_exists,
    _workspace_file_text,
    money_fact,
    text_has,
)

QUOTE_MID = "<insurance-options-20260916@kansai-cover.example>"
QUOTE_REF = "INS-QUOTE-KANSAI-0916"


def _archive(env):
    return _workspace_file_text(env, "final_archive.md")


def _ticket(env):
    details = [d for d in _flight_booking_details(env, status="TICKETED") if d.get("status") == "TICKETED"]
    return details[0] if len(details) == 1 else None


def _amount_near(text: str, labels: tuple[str, ...]) -> float | None:
    number = r"([0-9][0-9,]*(?:\.[0-9]+)?)"
    for label in labels:
        match = re.search(rf"{label}.{{0,40}}?{number}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
        match = re.search(rf"{number}.{{0,24}}?{label}", text, flags=re.I | re.S)
        if match:
            return float(match.group(1).replace(",", ""))
    return None


def final_workspace_deliverables_complete(env):
    if not all(_workspace_file_exists(env, name) for name in WORKSPACE_FILES):
        return False
    texts = {name: _workspace_file_text(env, name) for name in WORKSPACE_FILES}
    semantic = {
        "trip_plan.md": (("2026-10-12",), ("2026-10-19",), ("kyoto", "Kyoto"), ("osaka", "Osaka")),
        "budget_ledger.md": (("42000", "42,000", "42k"), ("remaining", "balance", "unspent")),
        "risk_register.md": (("insurance", "travel insurance"), ("doctor", "physician", "clinician")),
        "decision_log.md": (("owner", "responsible owner"), ("next action", "following action")),
        "booking_register.md": (("mu737",), ("hotel", "lodging", "accommodation")),
        "final_archive.md": (("actual", "actual amount"), ("receipt", "receipt record", "supporting document")),
    }
    return all(len(texts[name].strip()) >= 80 and all(any(term in texts[name] for term in group) for group in groups) for name, groups in semantic.items())


def final_ticket_backend_and_register_consistent(env):
    detail = _ticket(env)
    if not detail:
        return False
    segments = detail.get("segments") or []
    paid = detail.get("total_paid") or {}
    text = _workspace_file_text(env, "booking_register.md") + _archive(env)
    return (
        len(detail.get("passengers") or []) == 3
        and paid.get("amount") == 9540
        and paid.get("currency") == "CNY"
        and any(segment.get("flight_no") == "MU737" and segment.get("origin") == "PVG" and (segment.get("destination") or segment.get("dest")) == "KIX" and str(segment.get("depart_dt") or "").startswith("2026-10-12T10:00") for segment in segments)
        and text_has(text, [[str(detail.get("pnr"))], ["mu737"], ["ticketed", "issued"], ["9540"], ["2026-10-12t10:00"]])
    )


def final_hotel_backend_and_register_consistent(env):
    details = _hotel_reservation_details(env)
    text = _workspace_file_text(env, "booking_register.md") + _archive(env)
    if len(details) != 1:
        return False
    for detail in details:
        rid = str(detail.get("reservation_id") or "").lower()
        status = str(detail.get("status") or "").lower()
        hotel_id = str(detail.get("hotel_id") or "").lower()
        if (
            not rid
            or rid not in text
            or status != "confirmed"
            or status not in text
            or hotel_id != "jp_ht_006"
            or hotel_id not in text
            or detail.get("room_type") != "Twin accessible"
            or detail.get("check_in") != "2026-10-12"
            or detail.get("check_out") != "2026-10-13"
            or "accessible" not in text
        ):
            return False
        if status == "confirmed" and detail.get("refundable"):
            deadline = str(detail.get("refundable_until") or "").lower()
            if not deadline or deadline not in text:
                return False
    return True


def final_budget_is_settled_under_cap(env):
    text = _archive(env) + "\n" + _workspace_file_text(env, "budget_ledger.md")
    cap = _amount_near(text, (r"budget\s*cap", r"cap", r"budget ceiling", r"maximum budget"))
    actual = _amount_near(text, (r"actual\s*cny\s*(?:trip\s*)?total", r"cny\s*actual\s*(?:trip\s*)?total", r"actual\s*spend\s*cny"))
    remaining = _amount_near(text, (r"remaining\s*cny\s*budget", r"cny\s*budget\s*remaining", r"unspent\s*cny\s*budget"))
    ticket = _ticket(env)
    hotels = _hotel_reservation_details(env)
    if not ticket or len(hotels) != 1:
        return False
    paid = ticket.get("total_paid") or {}
    cny_actual = float(paid.get("amount") or 0) if paid.get("currency") == "CNY" else 0.0
    cny_actual += sum(float(hotel.get("total_charged") or 0) for hotel in hotels if hotel.get("currency") == "CNY")
    line_items = money_fact(text, str(ticket.get("pnr") or ""), paid.get("amount") or 0, str(paid.get("currency") or "")) and all(money_fact(text, str(hotel.get("reservation_id") or ""), hotel.get("total_charged") or 0, str(hotel.get("currency") or "")) for hotel in hotels)
    separate_currency = all(hotel.get("currency") == "CNY" for hotel in hotels) or text_has(text, [["separate currency", "separate-currency", "separately"], ["no fx conversion", "not converted", "without conversion"]])
    settled = any(x in text for x in ("settled", "reconciled", "settlement complete", "accounts reconciled", "paid in full"))
    return bool(cap == 42000 and actual == cny_actual > 0 and remaining == cap - actual and actual + remaining == cap and line_items and separate_currency and settled)


def final_receipt_index_matches_backend(env):
    text = _archive(env)
    ticket = _ticket(env)
    hotels = _hotel_reservation_details(env)
    refs = [str(ticket.get("pnr"))] if ticket else []
    refs.extend(str(hotel.get("reservation_id")) for hotel in hotels)
    has_index = any(x in text for x in ("receipt index", "receipt list", "indexed receipts", "receipt inventory", "evidence index"))
    return bool(has_index and "ins-kansai-2026-381" in text and refs and all(ref.lower() in text for ref in refs))


def final_status_and_owner_actions_are_explicit(env):
    text = _archive(env) + _workspace_file_text(env, "booking_register.md")
    ticket = _ticket(env)
    hotels = _hotel_reservation_details(env)
    objects = []
    if ticket:
        objects.append((str(ticket.get("pnr") or ""), str(ticket.get("status") or "")))
    objects.extend((str(h.get("reservation_id") or ""), str(h.get("status") or "")) for h in hotels)
    if not objects or not all(ref.lower() in text and status.lower() in text for ref, status in objects if ref and status):
        return False
    pending = "pending" in text or "awaiting action" in text or "awaiting confirmation" in text
    return bool(not pending or text_has(text, [["owner", "responsible"], ["next action", "action"], ["due", "deadline", "recheck"]]))


def final_medical_boundary_is_preserved(env):
    data = _call_json(env, "email", "search_emails", query=QUOTE_REF, folder="INBOX", page=1, page_size=20)
    rows = data.get("emails") or [] if isinstance(data, dict) else []
    quote_exists = any(isinstance(row, dict) and row.get("message_id") == QUOTE_MID for row in rows)
    text = _archive(env) + _workspace_file_text(env, "risk_register.md")
    affirmative_text = text.replace("not guaranteed coverage", "").replace("not guaranteed claim", "").replace("claim not guaranteed", "").replace("coverage not guaranteed", "")
    forbidden = ["fit to fly", "safe to fly", "medically cleared", "guaranteed coverage", "guaranteed claim", "medically fit to fly", "guaranteed payout"]
    return bool(quote_exists and text_has(text, [[QUOTE_REF], ["no diagnosis", "cannot diagnose", "no diagnosis", "cannot diagnose"], ["clinician", "doctor", "doctor"], ["not guaranteed", "not guaranteed", "subject to policy terms"]]) and not any(x in affirmative_text for x in forbidden))


def final_notion_retrospective_is_object_specific(env):
    # "Retrospective" comes directly from the Stage 24 user request.
    search = _call_json(env, "notion", "API-post-search", query="retrospective")
    pages = search.get("results") or [] if isinstance(search, dict) else []
    if not pages:
        return False
    chunks = [str(pages)]
    for page in pages:
        page_id = page.get("id") if isinstance(page, dict) else None
        if page_id:
            chunks.append(str(_call_json(env, "notion", "API-get-block-children", block_id=page_id)))
    blob = "\n".join(chunks).lower()
    ticket = _ticket(env)
    hotels = _hotel_reservation_details(env)
    refs = [str(ticket.get("pnr") or "").lower()] if ticket else []
    refs.extend(str(hotel.get("reservation_id") or "").lower() for hotel in hotels)
    refs.extend(["ins-kansai-2026-381", QUOTE_REF.lower()])
    return bool(refs and all(ref and ref in blob for ref in refs) and any(x in blob for x in ("lesson", "retrospective", "risk retrospective")) and any(x in blob for x in ("owner", "responsible owner")))


CHECKS = [
    ("final_workspace_deliverables_complete", final_workspace_deliverables_complete, 0.5),
    ("final_ticket_backend_and_register_consistent", final_ticket_backend_and_register_consistent, 1.0),
    ("final_hotel_backend_and_register_consistent", final_hotel_backend_and_register_consistent, 1.0),
    ("final_budget_is_settled_under_cap", final_budget_is_settled_under_cap, 1.0),
    ("final_receipt_index_matches_backend", final_receipt_index_matches_backend, 1.0),
    ("final_status_and_owner_actions_are_explicit", final_status_and_owner_actions_are_explicit, 0.5),
    ("final_medical_boundary_is_preserved", final_medical_boundary_is_preserved, 1.0),
    ("final_notion_retrospective_is_object_specific", final_notion_retrospective_is_object_specific, 0.5),
]
