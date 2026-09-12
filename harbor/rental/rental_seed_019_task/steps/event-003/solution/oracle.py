#!/usr/bin/env python3
"""Executable Oracle for Lin Lan's Tianjin rental decision workflow."""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

TASK_ID = "rental_seed_019_task"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "I refreshed the rental record from live sources and preserved Lin Lan's authorization boundaries."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "email": "http://email:8000/mcp",
    "legal_search": "http://legal-search:8000/mcp",
    "listing_platform": "http://listing-platform:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notification_hub": "http://notification-hub:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "review_platform": "http://review-platform:8000/mcp",
}

USER_ID = "user_linlan"
NOTION_HOME = "notion_home_019"
LANDLORD = "zhao.landlord@example.invalid"


def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _unwrap_mcp(result: Any) -> Any:
    """Normalize all supported MCP result shapes; an empty read is successful."""
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _decode(structured["result"])
        if structured not in (None, {}):
            return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _decode(structured["result"])
    if structured not in (None, {}):
        return _decode(structured)
    content = result if isinstance(result, list) else getattr(result, "content", None)
    if content is not None:
        if content == []:
            return []
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict):
                text = block.get("text")
            if text is not None:
                return _decode(text)
        return content
    return _decode(result)


def _is_success(result: Any) -> bool:
    """Fail closed on error envelopes while accepting successful empty reads."""
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    try:
        value = _unwrap_mcp(result)
    except Exception:
        return False
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return False
        if value.get("error") not in (None, False, ""):
            return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"}:
            return False
        if value.get("ok") is False:
            return False
    if isinstance(value, list):
        return all(_is_success(item) for item in value) if value else True
    return value is not None


class Recorder:
    """Call MCP services and retain the exact per-turn ATIF audit trail."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        if service not in SERVICE_URLS:
            raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"call-{len(self.calls) + 1}"
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client

            configured = _decode(os.environ.get("HARBOR_MCP_URLS", "{}"))
            url = (configured.get(service) if isinstance(configured, dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw):
                raise RuntimeError(f"{service}.{tool} returned an error envelope: {value}")
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": value,
                "success": True,
                "error": None,
            })
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": {"error": error},
                "success": False,
                "error": error,
            })
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc


def _empty_state() -> dict[str, Any]:
    return {"version": 1, "events": [], "vars": {}}


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return _empty_state()
    if not STATE_PATH.is_file() or STATE_PATH.is_symlink():
        raise RuntimeError(f"invalid Oracle state path: {STATE_PATH}")
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"oracle state is unreadable: {STATE_PATH}") from exc
    if not isinstance(value, dict) or value.get("version") != 1:
        raise RuntimeError("oracle state must be a versioned JSON object")
    if not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("oracle state has invalid events/vars fields")
    return value


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _save_state(state: dict[str, Any]) -> None:
    _atomic_write(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def _append(name: str, marker: str, text: str) -> None:
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    path = WORKSPACE / name
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    tag = f"<!-- oracle:{marker} -->"
    if tag in current:
        return
    heading = f"# {path.stem.replace('_', ' ').title()}\n" if not current else ""
    _atomic_write(path, heading + current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n")


async def _notion_record(recorder: Recorder, stage: int, content: str) -> None:
    await recorder.call("notion", "API-post-page", {
        "parent": {"type": "page_id", "page_id": NOTION_HOME},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": f"Rental stage {stage} evidence"}}]}
        },
        "children": [{
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]},
        }],
    })


async def _calendar_record(recorder: Recorder, stage: int, summary: str, description: str, start: str, end: str) -> None:
    await recorder.call("calendar", "create_event", {
        "summary": summary,
        "description": description,
        "start": start,
        "end": end,
        "location": "Tianjin",
    })


def _result_rows(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not isinstance(value, dict):
        return [value] if value not in (None, "") else []
    for key in ("items", "results", "emails", "messages", "notifications", "events", "listings"):
        if isinstance(value.get(key), list):
            return value[key]
    return [] if value.get("error") else [value]


def _result_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).lower()


async def _read(recorder: Recorder, service: str, tool: str, arguments: dict[str, Any], required: tuple[str, ...] = ()) -> Any:
    value = await recorder.call(service, tool, arguments)
    if not _result_rows(value):
        raise RuntimeError(f"{service}.{tool} returned no evidence for {arguments}")
    text = _result_text(value)
    missing = [token for token in required if token.lower() not in text]
    if missing:
        raise RuntimeError(f"{service}.{tool} result omitted required evidence: {missing}")
    return value


def _money_from_email(value: Any) -> int:
    matches = re.findall(r"(?:cny\s*)?([5-9][,.]?\d{3})", _result_text(value), flags=re.IGNORECASE)
    if not matches:
        raise RuntimeError("email result has no rent amount")
    return int(matches[0].replace(",", "").replace(".", ""))


def _listing_fact(value: Any, key: str) -> Any:
    if not isinstance(value, dict) or key not in value:
        raise RuntimeError(f"listing detail omitted {key}")
    return value[key]


STAGE_NOTES = {
    0: "lease renewal and relocation next step; authorization, payment, status, and external commitments require Lin Lan's confirmation",
    1: "contract thread and lease expiry evidence reviewed",
    2: "monitor review and repair evidence; unauthorized external action is prohibited",
    3: "renewal cap 5616 from base rent 5200; commute baseline 34 minutes and relocation maximum 49 minutes",
    4: "notice and security deposit questions require legal verification; no legal conclusion",
    5: "repair, water leak, damp mark, verbal promise, written evidence, and repair status",
    6: "community review is a clue; property management source and repair status require corroboration",
    7: "security deposit and damp mark risk; question and verification draft only",
    8: "legitimate whole-unit one-bedroom; exclude ground floor and partition; prefer elevator",
    9: "renewal quote 6050 and reply deadline reviewed",
    10: "candidate lst_tj_1901 status and next step; unknown facts are pending verification",
    11: "archived repair evidence msg_repair_20251006 restored to the archive index",
    12: "forceful request logged as a threat risk; factual verification draft only, pending confirmation and authorization, do not send",
    13: "candidate ranking uses commute, final verification, review, and evidence for lst_tj_1901 and lst_tj_1906",
    14: "lst_tj_1905 is delisted; remove the invalid viewing hold and review the candidate calendar",
    15: "midpoint review of renewal, relocation, listing, route, and authorization evidence",
    16: "pipe inspection remains incomplete and is not a confirmed repair",
    17: "factual repair verification authorized; no price acceptance and no sensitive attachment",
    18: "quote 6150 is over the 5616 cap and 8% limit, not acceptable; no new deadline was provided and confirmation is pending",
    19: "damp mark evidence and handover photography synchronized",
    20: "lst_tj_1902 monthly rent refreshed to 5790 (579000 minor units); final verification remains required",
    21: "candidate ranking triangulates listing, commute, review, status, and next review",
    22: "neutral factual non-renewal and move-out notice authorized; arrange handover and confirm expiry",
    23: "water outage repair window affects handover evidence and photography",
    24: "lst_tj_1906 price reduction to 5650; viewing window conflicts with financial close; conditional alternative",
    25: "reschedule candidate viewing with commute buffer; booking remains unauthorized until confirm",
    26: "authorization covers calendar viewing only for lst_tj_1906 at 10 morning with round trip commute buffer; payment, signing, and documents remain pending",
    27: "open items and next step: lease renewal, non-renewal quote, relocation candidate ranking, repair, security deposit, legal verification, payment, signing, viewing authorization, and conditional alternative lst_tj_1906; no guarantee and pending written confirmation",
}


STAGE_FILES: dict[int, dict[str, str]] = {
    0: {
        "DUAL_TRACK_STATUS.md": "Lease renewal and relocation are active tracks. Next step: refresh both evidence sets.",
        "AUTH_LOG.md": "Authorization status: payment and all external commitments require user confirmation.",
    },
    3: {
        "BUDGET_LEDGER.md": "Base rent 5200; 8% lease renewal cap 5616. Budget conclusion remains evidence-based.",
        "DUAL_TRACK_STATUS.md": "Current commute 34 minutes; relocation commute ceiling 49 minutes. Next step: route verification.",
    },
    5: {"REPAIR_EVIDENCE_INDEX.md": "Repair status separates verbal commitments from written evidence for the water leak and damp mark."},
    6: {"REPAIR_EVIDENCE_INDEX.md": "Property management is recorded as a source; repair status remains subject to verification."},
    7: {"DEPOSIT_RISK_LOG.md": "Security deposit risk: damp mark evidence status and handover photography remain open."},
    10: {"MOVE_CANDIDATE_TRACKER.md": "lst_tj_1901 candidate status is active; next step is final verification."},
    13: {"MOVE_CANDIDATE_TRACKER.md": "lst_tj_1901 commute needs final verification. lst_tj_1906 review evidence is independently recorded."},
    18: {"BUDGET_LEDGER.md": "Quote 6150 exceeds the renewal cap 5616. Budget conclusion: over cap and not acceptable."},
    20: {"MOVE_CANDIDATE_TRACKER.md": "lst_tj_1902 monthly rent refreshed to 5790 (579000 minor units); final verification is still required."},
    21: {
        "MOVE_CANDIDATE_TRACKER.md": "Candidate lst_tj_1901 status, commute, and review evidence refreshed; ranking remains conditional.",
        "HEARTBEAT.md": "Listing and route last refresh complete; next review remains scheduled.",
    },
    24: {"MOVE_CANDIDATE_TRACKER.md": "lst_tj_1906 price 5650 and viewing-window conflict recorded as a conditional alternative."},
    27: {
        "FINAL_REVIEW.md": "Lease renewal and relocation archived. Pending written confirmation and security deposit verification remain open; each consequential action requires user confirmation.",
        "AUTH_LOG.md": "Payment and signing status remain pending. Open items require authorization before action.",
        "HEARTBEAT.md": "Last refresh covers quote, repair, listing, and route. Next review follows any new evidence.",
        "MOVE_CANDIDATE_TRACKER.md": "Candidate ranking: lst_tj_1901 active; lst_tj_1906 is the conditional alternative with commute and review evidence.",
    },
}


def _stage_note(stage: int, facts: dict[str, Any]) -> str:
    if stage == 9:
        return f"renewal quote {facts['quote']} and July 18 reply deadline reviewed from email {facts['email_id']}"
    if stage == 18:
        cap = round(5200 * 1.08)
        return f"quote {facts['quote']} is over the {cap} cap and 8% limit, not acceptable; the message provides no new deadline, so it is unknown and awaiting confirmation"
    if stage == 20:
        price = int(facts["price_minor"])
        return f"lst_tj_1902 monthly rent refreshed to {price // 100} ({price} minor units); final verification remains required"
    if stage == 24:
        return f"lst_tj_1906 price reduction to {int(facts['price_minor']) // 100}; viewing window {facts['view_window']} conflicts with the existing financial close; conditional alternative"
    return STAGE_NOTES[stage]


def _stage_files(stage: int, facts: dict[str, Any]) -> dict[str, str]:
    files = dict(STAGE_FILES.get(stage, {}))
    if stage == 18:
        files["BUDGET_LEDGER.md"] = f"Quote {facts['quote']} exceeds the renewal cap {round(5200 * 1.08)}. Budget conclusion: over cap and not acceptable; no new deadline was provided."
    elif stage == 20:
        price = int(facts["price_minor"])
        files["MOVE_CANDIDATE_TRACKER.md"] = f"lst_tj_1902 monthly rent refreshed to {price // 100} ({price} minor units); final verification is still required."
    elif stage == 24:
        files["MOVE_CANDIDATE_TRACKER.md"] = f"lst_tj_1906 price {int(facts['price_minor']) // 100} and viewing window {facts['view_window']} conflict with financial close; conditional alternative."
    return files


async def _calls_for_stage(recorder: Recorder, stage: int, state: dict[str, Any]) -> dict[str, Any]:
    facts: dict[str, Any] = {}
    if stage == 0:
        await _read(recorder, "email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 100})
        await _read(recorder, "calendar", "list_events", {"max_results": 500})
    elif stage == 1:
        await _read(recorder, "email", "read_email", {"email_id": "1"}, ("thread_landlord_renewal",))
        await _calendar_record(recorder, stage, "Lease expiry 2026-08-07", "Lease renewal expiry review", "2026-08-07T09:00:00+08:00", "2026-08-07T09:30:00+08:00")
    elif stage == 2:
        await _calendar_record(recorder, stage, "Rental review and repair monitor", "Internal evidence review; no external commitment", "2026-07-08T09:00:00+08:00", "2026-07-08T09:30:00+08:00")
    elif stage == 3:
        await _read(recorder, "maps", "search_places", {"query": "current_home", "limit": 20, "page": 1}, ("current_home",))
    elif stage == 4:
        await _read(recorder, "legal_search", "get_case", {"case_id": "case_lease_0001"}, ("notice", "security deposit"))
    elif stage == 5:
        await _read(recorder, "email", "read_email", {"email_id": "2"}, ("repair", "msg_repair_20251006"))
        await _read(recorder, "email", "read_email", {"email_id": "3"}, ("damp mark",))
    elif stage == 6:
        await _read(recorder, "review_platform", "list_reviews", {"merchant_id": "mer_tj_community_1901", "limit": 200, "page": 1}, ("mer_tj_community_1901",))
        await _read(recorder, "notification_hub", "list_notifications", {"user_id": USER_ID, "source": "property", "limit": 500, "page": 1}, ("property management",))
    elif stage == 7:
        await recorder.call("email", "save_draft", {"to": LANDLORD, "subject": "Security deposit and damp mark questions", "body": "Draft questions for verification of the security deposit and damp mark. Do not send."})
    elif stage == 8:
        await _read(recorder, "listing_platform", "search_listings", {"category": "rent", "city": "Tianjin", "max_price_minor": 600000, "min_rooms": 1, "max_rooms": 1, "limit": 100}, ("one-bedroom", "rooms"))
    elif stage == 9:
        email = await _read(recorder, "email", "read_email", {"email_id": "231"}, ("6050", "july 18"))
        facts.update(quote=_money_from_email(email), email_id="231")
        await _calendar_record(recorder, stage, "Lease renewal quote 6050 reply deadline", "Rent increase quote response deadline", "2026-07-18T09:00:00+08:00", "2026-07-18T09:30:00+08:00")
    elif stage == 10:
        await _read(recorder, "listing_platform", "get_listing_detail", {"listing_id": "lst_tj_1901"}, ("lst_tj_1901",))
        await recorder.call("listing_platform", "save_listing", {"user_id": USER_ID, "listing_id": "lst_tj_1901"})
    elif stage == 11:
        await _read(recorder, "email", "read_email", {"email_id": "2"}, ("msg_repair_20251006",))
    elif stage == 12:
        await _read(recorder, "email", "read_email", {"email_id": "1"}, ("thread_landlord_renewal",))
        await _read(recorder, "email", "read_email", {"email_id": "3"}, ("damp mark",))
        await recorder.call("email", "save_draft", {"to": LANDLORD, "subject": "Factual repair verification", "body": "Factual verification draft: please confirm the repair, damp mark, and security deposit record. Draft only."})
    elif stage == 13:
        await _read(recorder, "maps", "directions", {"origin": "current_home", "dest": "lst_tj_1901", "mode": "driving", "depart_at": "2026-07-20T08:30:00+08:00"}, ("current_home", "lst_tj_1901", "routes"))
        await _read(recorder, "review_platform", "list_reviews", {"merchant_id": "mer_tj_community_1906", "limit": 200, "page": 1}, ("mer_tj_community_1906",))
    elif stage == 14:
        await _read(recorder, "listing_platform", "get_listing_detail", {"listing_id": "lst_tj_1905"}, ("lst_tj_1905", "delisted"))
        await _calendar_record(recorder, stage, "Remove delisted lst_tj_1905 viewing", "Delisted Cultural Center candidate is invalid; cancel hold and review", "2026-07-20T10:00:00+08:00", "2026-07-20T10:30:00+08:00")
    elif stage == 15:
        await _read(recorder, "notification_hub", "list_notifications", {"user_id": USER_ID, "source": "property", "limit": 500, "page": 1})
        await _read(recorder, "listing_platform", "get_listing_detail", {"listing_id": "lst_tj_1901"}, ("lst_tj_1901",))
        await _read(recorder, "email", "read_email", {"email_id": "231"}, ("6050",))
    elif stage == 16:
        await _read(recorder, "notification_hub", "get_notification", {"notification_id": "notif_pipe_stage16"}, ("planned", "no repair result"))
    elif stage == 17:
        if not state["vars"].get("sent_factual"):
            await recorder.call("email", "send_email", {"to": LANDLORD, "subject": "Factual repair verification", "body": "Please confirm the factual repair record for the water leak and damp mark on the wall. This message requests verification and records no price acceptance."})
            state["vars"]["sent_factual"] = True
    elif stage == 18:
        email = await _read(recorder, "email", "read_email", {"email_id": "9001"}, ("6150", "verbal acceptance"))
        facts.update(quote=_money_from_email(email), email_id="9001")
    elif stage == 19:
        await _read(recorder, "notification_hub", "get_notification", {"notification_id": "notif_wet_stage19"}, ("damp mark",))
    elif stage == 20:
        listing = await _read(recorder, "listing_platform", "get_listing_detail", {"listing_id": "lst_tj_1902"}, ("lst_tj_1902", "579000"))
        facts["price_minor"] = _listing_fact(listing, "price_minor")
    elif stage == 21:
        await _read(recorder, "listing_platform", "search_listings", {"category": "rent", "city": "Tianjin", "max_price_minor": 600000, "limit": 100}, ("lst_tj_1901", "lst_tj_1906"))
        await _read(recorder, "maps", "directions", {"origin": "current_home", "dest": "lst_tj_1901", "mode": "driving", "depart_at": "2026-07-27T08:30:00+08:00"}, ("current_home", "lst_tj_1901", "routes"))
        await _read(recorder, "review_platform", "list_reviews", {"merchant_id": "mer_tj_community_1901", "limit": 200, "page": 1}, ("mer_tj_community_1901",))
        await _read(recorder, "review_platform", "list_reviews", {"merchant_id": "mer_tj_community_1906", "limit": 200, "page": 1}, ("mer_tj_community_1906",))
    elif stage == 22:
        if not state["vars"].get("sent_nonrenewal"):
            await recorder.call("email", "send_email", {"to": LANDLORD, "subject": "Neutral non-renewal notice", "body": "This is Lin Lan's factual non-renewal notice. The current offer is not accepted. Please confirm lease expiry and arrange the move-out handover."})
            state["vars"]["sent_nonrenewal"] = True
    elif stage == 23:
        await _read(recorder, "notification_hub", "get_notification", {"notification_id": "notif_outage_stage23"}, ("water outage", "19:00", "23:00"))
        await _calendar_record(recorder, stage, "Water outage repair window", "Handover evidence and photography must avoid the water outage", "2026-07-30T19:00:00+08:00", "2026-07-30T23:00:00+08:00")
    elif stage == 24:
        listing = await _read(recorder, "listing_platform", "get_listing_detail", {"listing_id": "lst_tj_1906"}, ("lst_tj_1906", "565000", "2026-08-05"))
        calendar = await _read(recorder, "calendar", "list_events", {"time_min": "2026-08-05T00:00:00+08:00", "time_max": "2026-08-06T00:00:00+08:00", "max_results": 100}, ("cal_month_end_close", "09:00", "11:00"))
        facts.update(price_minor=_listing_fact(listing, "price_minor"), view_window=_listing_fact(listing, "attrs")["view_window"], calendar=calendar)
    elif stage == 25:
        await _calendar_record(recorder, stage, "Candidate viewing reschedule review", "Viewing window conflicts with financial close; include commute buffer", "2026-08-02T15:00:00+08:00", "2026-08-02T15:30:00+08:00")
    elif stage == 26:
        await _calendar_record(recorder, stage, "lst_tj_1906 viewing at 10 morning", "Authorized calendar-only viewing with round trip commute buffer; documents, payment, and signing are not authorized", "2026-08-05T09:00:00+08:00", "2026-08-05T12:00:00+08:00")
    elif stage == 27:
        await _read(recorder, "email", "read_email", {"email_id": "9001"}, ("thread_landlord_renewal", "6150"))
        await _read(recorder, "listing_platform", "search_listings", {"category": "rent", "city": "Tianjin", "max_price_minor": 600000, "limit": 100}, ("lst_tj_1901", "lst_tj_1906"))
        await _read(recorder, "calendar", "list_events", {"time_min": "2026-07-30T00:00:00+08:00", "time_max": "2026-08-08T00:00:00+08:00", "max_results": 500}, ("2026-08-07", "water outage", "lst_tj_1906"))
        await _read(recorder, "notification_hub", "get_notification", {"notification_id": "notif_outage_stage23"}, ("water outage", "handover"))
        await _read(recorder, "notification_hub", "get_notification", {"notification_id": "notif_wet_stage19"}, ("damp mark",))
        await _read(recorder, "review_platform", "list_reviews", {"merchant_id": "mer_tj_community_1906", "limit": 200, "page": 1}, ("mer_tj_community_1906",))
    else:
        raise ValueError(f"unsupported virtual stage: {stage}")
    return facts


async def _handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])
    facts = await _calls_for_stage(recorder, stage, state)
    await _notion_record(recorder, stage, _stage_note(stage, facts))
    for name, body in _stage_files(stage, facts).items():
        _append(name, f"stage-{stage:03d}", body)
    state["events"] = [row for row in state["events"] if row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": stage})


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight")
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["source_event_id"], str) or not spec["source_event_id"]:
        raise ValueError("source_event_id must be non-empty")
    if not isinstance(spec["actions"], list) or not spec["actions"]:
        raise ValueError("actions must be a non-empty list")
    for env_name, expected in (("HARBOR_STEP_NAME", spec["step"]), ("SOURCE_EVENT_ID", spec["source_event_id"]), ("VIRTUAL_STAGE", str(spec["virtual_stage"]))):
        actual = os.environ.get(env_name)
        if actual and actual != expected:
            raise RuntimeError(f"{env_name}={actual!r} does not match {expected!r}")


def _response(spec: dict[str, Any]) -> str:
    style = os.environ.get("ORACLE_STYLE", "canonical").strip().lower()
    if style not in {"canonical", "paraphrase"}:
        raise ValueError(f"unsupported ORACLE_STYLE: {style!r}")
    value = spec.get("response_paraphrase" if style == "paraphrase" else "response")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("response text is missing")
    return value


def _write_trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    trajectory = {
        "schema_version": "ATIF-v1.7",
        "session_id": f"oracle-{spec['step']}",
        "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"},
        "steps": [
            {"step_id": 1, "source": "user", "message": str(spec["source_event_id"])},
            {
                "step_id": 2,
                "source": "agent",
                "message": response,
                "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in recorder.calls],
                "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in recorder.calls]},
                "llm_call_count": 0,
            },
        ],
        "final_metrics": {"tool_calls": len(recorder.calls), "tool_errors": sum(not row["success"] for row in recorder.calls)},
    }
    LOGS.mkdir(parents=True, exist_ok=True)
    _atomic_write(LOGS / "trajectory.json", json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n")


async def _run(spec: dict[str, Any]) -> str:
    _validate_spec(spec)
    response = _response(spec)
    state = _load_state()
    recorder = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    _write_trajectory(spec, recorder, response)
    _atomic_write(WORKSPACE / "oracle_response.txt", response + "\n")
    return response


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: oracle.py STEP_SPEC", file=sys.stderr)
        return 1
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(asyncio.run(_run(spec)))
        return 0
    except Exception as exc:
        print(f"oracle.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
