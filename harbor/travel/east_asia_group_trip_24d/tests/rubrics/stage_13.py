"""Stage 13: replacement lodging must restore four-person capacity and persist the exact cost delta."""
from __future__ import annotations

from loguru import logger

from ._helpers import _hotel_reservation_details, _tool_calls, _tool_name_matches, _workspace_file_text


def _tokyo_state(env) -> tuple[list[dict], list[dict]]:
    rows = _hotel_reservation_details(env)
    active = [r for r in rows if str(r.get("status") or "").casefold() in {"confirmed", "modified"} and str(r.get("check_in"))[:10] == "2026-06-05" and str(r.get("check_out"))[:10] == "2026-06-08"]
    affected = [r for r in rows if r.get("hotel_id") == "htl_shinjuku_grand" and r.get("room_type") == "Superior Twin" and str(r.get("status") or "").casefold() == "walked"]
    return active, affected


def s13_gate(env) -> bool:
    active, affected = _tokyo_state(env)
    replacements = [r for r in active if r.get("hotel_id") != "htl_shinjuku_grand"]
    created = any(_tool_name_matches(str(c.get("name") or ""), "hotel_booking", "create_reservation") for c in _tool_calls(env, 13))
    capacity_ok = len(active) >= 2 and bool(replacements)  # two 2-person rooms cover the four travelers
    budget = _workspace_file_text(env, "/workspace/budget.md").casefold()
    incident = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    exact = affected + replacements
    references_ok = all(str(r.get("reservation_id") or "").casefold() in incident + "\n" + budget for r in exact)
    amounts_ok = all(str(r.get("total_charged") or "") in budget and str(r.get("currency") or "").casefold() in budget for r in replacements)
    budget_ok = "actual" in budget and "delta" in budget
    result = bool(created and affected and capacity_ok and references_ok and amounts_ok and budget_ok)
    logger.info("s13_gate: create={} affected={} capacity={} refs={} amounts={} budget={} -> {}", created, bool(affected), capacity_ok, references_ok, amounts_ok, budget_ok, "PASS" if result else "FAIL")
    return result


def s13b_gate(env) -> bool:
    active, affected = _tokyo_state(env)
    budget = _workspace_file_text(env, "/workspace/budget.md").casefold()
    incident = _workspace_file_text(env, "/workspace/incident_log.md").casefold()
    replacement_ids = [str(r.get("reservation_id") or "").casefold() for r in active if r.get("hotel_id") != "htl_shinjuku_grand"]
    return bool(
        affected and replacement_ids
        and all(rid in incident + "\n" + budget for rid in replacement_ids)
        and "actual" in budget
        and any(x in incident for x in ("walked", "oversell"))
        and "owner" in incident
    )


CHECKS = [("s13_gate", s13_gate, 2), ("s13b_gate", s13b_gate, 1.5)]
