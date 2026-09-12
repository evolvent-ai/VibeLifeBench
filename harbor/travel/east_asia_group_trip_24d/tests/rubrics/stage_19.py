"""Stage 19: exact Shinjuku reservation, backend special-request ticket, receipt email and durable linkage."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _hotel_reservation_details,
    _successful_email_read,
    _tool_calls,
    _tool_name_matches,
    _workspace_file_text,
)


def _receipt(env) -> dict | None:
    return _successful_email_read(
        env,
        19,
        ("lf-tyo-0610-27", "2026-07-10", "power bank", "passport copy", "cannot be air-mailed"),
        from_addr="lostandfound@shinjuku-grand.example.com",
    )


def s19_gate(env) -> bool:
    calls = _tool_calls(env, 19)
    looked_up = any(_tool_name_matches(str(c.get("name") or ""), "hotel_booking", t) for c in calls for t in ("get_reservation", "list_reservations"))
    special_calls = [c for c in calls if _tool_name_matches(str(c.get("name") or ""), "hotel_booking", "submit_special_request")]
    searched = any(_tool_name_matches(str(c.get("name") or ""), "email", "search_emails") for c in calls)
    read = any(_tool_name_matches(str(c.get("name") or ""), "email", "read_email") for c in calls)
    shinjuku = [r for r in _hotel_reservation_details(env) if r.get("hotel_id") == "htl_shinjuku_grand" and str(r.get("check_in"))[:10] == "2026-06-05" and str(r.get("check_out"))[:10] == "2026-06-08"]
    linked = []
    for reservation in shinjuku:
        for req in reservation.get("special_requests") or []:
            if not isinstance(req, dict):
                continue
            text = str(req.get("text") or "").casefold()
            if "power bank" in text and "passport copy" in text:
                linked.append((reservation, req))
    exact_call = any(
        isinstance(c.get("arguments"), dict)
        and any(str(c["arguments"].get("reservation_id") or "") == str(r.get("reservation_id") or "") for r, _ in linked)
        and "power bank" in str(c["arguments"].get("text") or "").casefold()
        for c in special_calls
    )
    receipt = _receipt(env) if searched and read else None
    incident = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    links_ok = any(
        str(r.get("reservation_id") or "").casefold() in incident
        and str(req.get("ticket_id") or "").casefold() in incident
        for r, req in linked
    )
    incident_ok = links_ok and all(x in incident for x in ("lf-tyo-0610-27", "2026-07-10", "power bank", "passport copy")) and "cannot air-mail" in incident
    ok = bool(looked_up and exact_call and receipt and incident_ok)
    logger.info("s19_gate: lookup={} request={} receipt={} incident={} -> {}", looked_up, exact_call, bool(receipt), incident_ok, "PASS" if ok else "FAIL")
    return ok


CHECKS = [("s19_gate", s19_gate, 1.5)]
