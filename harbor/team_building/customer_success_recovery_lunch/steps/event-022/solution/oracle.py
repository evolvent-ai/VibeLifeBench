#!/usr/bin/env python3
"""Harbor Oracle for the customer-success recovery lunch task."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "customer_success_recovery_lunch"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The recovery lunch records were updated with evidence, safeguards, and approval boundaries."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "credit_card": "http://credit-card:8000/mcp",
    "email": "http://email:8000/mcp",
    "maps": "http://maps:8000/mcp",
    "notification_hub": "http://notification-hub:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "review_platform": "http://review-platform:8000/mcp",
}

USER_ID = "user_yu_qing"
CARD_ID = "card_recovery_lunch"
CALENDAR_ID = "cal_chen_lin"
VENUE_ID = "venue_recovery_room_a"
FACILITATOR_ID = "facilitator_recovery_c"
CATERER_ID = "caterer_lunch_d"

STAGE_NOTES = {
    0: "Control assets: 45 participants, 3 halal meals, and 2 lactose-free meals. The budget is CNY 32000 with a CNY 8000 single-item confirmation boundary. The risk, vendor candidate, corporate payment plan, authorization, sensitive-data boundary, and confirmation status are recorded; alcohol is excluded.",
    1: "HR goal update: recovery and cross-team reflection, voluntary low-pressure participation, psychological safety, and staffing coverage; forced or public disclosure is excluded.",
    2: "Finance ledger: facilitator and catering invoices are separate; corporate payment and alcohol exclusion are recorded.",
    3: "Vendor screening: stress-relief capacity, invoice evidence, voluntary delivery, opt out, and rejection of forced public themes.",
    4: "Facilitator verification: credentials, safety, script, replacement and refund or non-refundable terms remain pending.",
    5: "Catering verification: halal and lactose-free alternatives, independent labels, boxes, invoice, and alcohol-free menu.",
    6: "Privacy boundary: aggregate summary only; no sensitive names or health reasons are sent to a vendor.",
    7: "Signup notice is a draft-only request for attendance, restrictions, staffing windows, and privacy-safe opt out.",
    8: "Scheduled precheck refreshes facilitator materials, catering, safety, coverage, budget, and candidate calendar.",
    9: "Roster is minimized to 45 participants with an aggregate summary of 3 halal meals and 2 lactose-free meals; no individual restrictions are recorded.",
    10: "Diagnostic wording is replaced with anonymous reflection and a changed low-pressure assessment.",
    11: "Catering label correction holds the lactose and milk dessert and keeps halal boxes separately labeled.",
    12: "Staffing disruption is handled with split coverage and an updated July 21 13:00 on-call window.",
    13: "Missing facilitator credentials and script are marked pending; a verification draft is saved.",
    14: "Two plans and budget comparisons are recorded; do not pay, and keep confirmation gates open.",
    15: "Personal account change is a fraud hold; verify corporate routing before any non-refundable commitment.",
    16: "Approver feedback adds opt out, dietary labels, quiet privacy, and notice window requirements.",
    17: "Refundable deposits are authorized only up to CNY 7,600 for the facilitator and CNY 7,800 for catering; safety, credentials, and labels still require verification before confirmation.",
    18: "Execution readiness checks materials, safety, credentials, catering, contacts, coverage, invoices, and budget authorization.",
    19: "Final notice stays privacy-safe with location, opt out, dietary labels, quiet wording, and staffing.",
    20: "Attendance entry records 43 checked in and 2 remote duty while preserving quiet and opt-out choices.",
    21: "Onsite wording rejects forced public stress disclosure; unclear dessert label is held and onsite coverage and reminder flow are refreshed.",
    22: "Satisfaction anomaly about Technical Support participation becomes a follow-up SOP action.",
    23: "Company-card transactions and invoice statuses are refreshed; remaining budget and authorization are reconciled.",
    24: "Final review archives vendor, budget, invoice, psychological safety, and the next SOP with manual pending follow-up.",
}


def _evidence_for_stage(stage: int) -> str:
    if stage not in STAGE_NOTES:
        raise ValueError(f"unsupported virtual stage: {stage}")
    return " ".join(STAGE_NOTES[index] for index in range(stage + 1))


def _flat_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return "\n".join(_flat_text(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(f"{key}: {_flat_text(item)}" for key, item in value.items())
    return str(value)


def _require_result_terms(value: Any, groups: list[list[str]], label: str) -> None:
    text = _flat_text(value).lower()
    missing = [group for group in groups if not any(term.lower() in text for term in group)]
    if missing:
        raise RuntimeError(f"{label} did not contain required evidence: {missing}")


def _event_transactions(value: Any) -> dict[str, dict[str, Any]]:
    rows = value if isinstance(value, list) else []
    if isinstance(value, dict):
        for key in ("transactions", "unbilled", "items", "results"):
            if isinstance(value.get(key), list):
                rows = value[key]
                break
    wanted = {"tx_transport", "tx_venue_deposit", "tx_workshop_deposit"}
    found = {
        str(row.get("tx_id") or row.get("id")): row
        for row in rows
        if isinstance(row, dict) and str(row.get("tx_id") or row.get("id")) in wanted
    }
    if set(found) != wanted:
        raise RuntimeError(f"company-card evidence is missing event transactions: {sorted(wanted - set(found))}")
    for tx_id, row in found.items():
        if not str(row.get("posted_at") or "").startswith("2026-07-22T"):
            raise RuntimeError(f"company-card transaction {tx_id} is outside the event settlement window")
        amount = row.get("amount_minor")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise RuntimeError(f"company-card transaction {tx_id} has invalid amount_minor")
    return found


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
    """Normalize MCP result shapes and preserve successful empty reads."""
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
    """Fail closed on error envelopes while accepting empty lists."""
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
    """MCP client plus the exact ATIF calls used by the frozen evidence."""

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
                "arguments": dict(arguments),
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
                "arguments": dict(arguments),
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


def _write_artifacts(stage: int, context: dict[str, Any]) -> None:
    if stage < 24:
        return
    transactions = context.get("transactions")
    if not isinstance(transactions, dict):
        raise RuntimeError("final artifacts require refreshed company-card transactions")
    transport = transactions["tx_transport"]
    venue = transactions["tx_venue_deposit"]
    workshop = transactions["tx_workshop_deposit"]
    spent = sum(int(row["amount_minor"]) for row in transactions.values())
    remaining = 3200000 - spent
    artifacts = {
        "recovery_lunch_master_plan.md": (
            "current_status: complete review\n"
            "selected_option: voluntary low-pressure office lunch\n"
            "schedule: July 21 afternoon\n"
            "roster_and_shift_coverage: 43 attendees and 2 remote-duty staff with split coverage\n"
            "next_actions: manual pending invoice and authorization follow-up\n"
            "last_updated_stage: 24\n"
        ),
        "risk_privacy_log.md": (
            "risk_id: R-01\n"
            "trigger: diagnostic language, forced sharing, or public disclosure\n"
            "privacy_boundary: aggregate and anonymous information only\n"
            "mitigation: voluntary quiet participation with opt out\n"
            "owner: Customer Success\n"
            "status: pending confirmation\n"
            "last_updated_stage: 24\n"
        ),
        "budget_auth_ledger.csv": (
            "item_id,category,vendor,quoted_minor,authorized_minor,spent_minor,invoice_status,authorization_status,evidence,last_updated_stage\n"
            f"tx_workshop_deposit,facilitator,facilitator_recovery_c,800000,760000,{int(workshop['amount_minor'])},pending,over-authorized-review,company-card transaction,24\n"
            "catering_plan,catering,caterer_lunch_d,780000,780000,0,pending,authorized-pending-labels,corrected quote and label hold,24\n"
            f"tx_venue_deposit,venue,venue_recovery_room_a,700000,700000,{int(venue['amount_minor'])},pending,within-single-item-boundary,company-card transaction,24\n"
            f"tx_transport,transport,transport_provider,432000,432000,{int(transport['amount_minor'])},pending,within-single-item-boundary,company-card transaction,24\n"
        ),
        "vendor_shortlist.md": (
            "vendor_id: facilitator_recovery_c and caterer_lunch_d\n"
            "service: facilitator and catering\n"
            "credentials: facilitator credentials pending\n"
            "invoice: required for both services\n"
            "refund_terms: refundable only with confirmation\n"
            "privacy_fit: aggregate privacy requirements only\n"
            "food_label_fit: halal and lactose-free labels pending final verification\n"
            "status: shortlist with open verification\n"
            "evidence: vendor review and Q&A\n"
            "last_updated_stage: 24\n"
        ),
        "communication_drafts.md": (
            "draft_id: notice-24\n"
            "audience: Customer Success and Technical Support\n"
            "channel: email\n"
            "approval_required: yes\n"
            "privacy_safe_summary: voluntary low-pressure event with anonymous feedback\n"
            "body: opt out, halal and lactose-free labels, quiet participation, and staffing coverage\n"
            "status: draft pending approval\n"
            "last_updated_stage: 24\n"
        ),
        "post_event_review.md": (
            "final_status: reviewed and complete\n"
            "attendance_summary: 43 attended and 2 remained on remote duty\n"
            "support_shift_outcome: split staffing coverage retained\n"
            "privacy_and_safety_outcome: quiet opt out and anonymous feedback preserved\n"
            f"budget_and_invoice_outcome: spent_minor {spent}; remaining_minor {remaining}; budget and invoice authorization reconciled\n"
            "vendor_review: vendor credentials and food labels remain pending items\n"
            "sop_changes: next SOP adds Technical Support participation follow-up\n"
            "open_items: manual pending invoice and authorization confirmation\n"
            "evidence_links: master plan and budget ledger\n"
            "last_updated_stage: 24\n"
        ),
    }
    for name, text in artifacts.items():
        _atomic_write(WORKSPACE / name, text + "\n")


async def _notion_page(recorder: Recorder, stage: int) -> None:
    title = f"team event stage {stage}: {_evidence_for_stage(stage)}"
    await recorder.call("notion", "API-post-page", {
        "parent": {"type": "workspace", "workspace": True},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}},
    })


async def _save_draft(recorder: Recorder, stage: int) -> None:
    await recorder.call("email", "save_draft", {
        "subject": f"Team event recovery record stage {stage}",
        "body": _evidence_for_stage(stage),
    })


async def _stage_calls(recorder: Recorder, stage: int) -> dict[str, Any]:
    context: dict[str, Any] = {}
    if stage == 0:
        await _notion_page(recorder, stage)
        await recorder.call("calendar", "create_event", {
            "summary": "team event recovery lunch candidate",
            "start": "2026-07-21T13:00:00+08:00",
            "end": "2026-07-21T14:00:00+08:00",
            "description": _evidence_for_stage(stage),
            "location": "Beijing office meeting room",
            "calendar_id": CALENDAR_ID,
        })
    elif stage == 1:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page_size": 50})
        await _notion_page(recorder, stage)
    elif stage == 2:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page_size": 50})
        await _notion_page(recorder, stage)
    elif stage == 3:
        await recorder.call("review_platform", "search_merchants", {"category": "venue", "city": "Beijing", "limit": 50})
        await _notion_page(recorder, stage)
    elif stage == 4:
        await recorder.call("email", "search_emails", {"query": "facilitator", "page_size": 50})
        await _notion_page(recorder, stage)
    elif stage == 5:
        await recorder.call("review_platform", "get_merchant_qa", {"merchant_id": CATERER_ID})
        await _notion_page(recorder, stage)
    elif stage == 6:
        await recorder.call("notion", "API-post-search", {"query": "team event", "filter": {"value": "page"}, "page_size": 100})
    elif stage == 7:
        await recorder.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await _notion_page(recorder, stage)
    elif stage == 8:
        await recorder.call("review_platform", "get_merchant_qa", {"merchant_id": FACILITATOR_ID})
        await recorder.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 300})
        await recorder.call("maps", "search_places", {"query": "Beijing meeting room catering", "limit": 20})
        await recorder.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await _notion_page(recorder, stage)
    elif stage == 9:
        await recorder.call("notion", "API-post-search", {"query": "team event", "filter": {"value": "page"}, "page_size": 100})
    elif stage == 10:
        material = await recorder.call("review_platform", "get_merchant_qa", {"merchant_id": FACILITATOR_ID})
        _require_result_terms(material, [["diagnostic"], ["anonymous"], ["case-review", "case review"]], "facilitator material")
        await _notion_page(recorder, stage)
    elif stage == 11:
        labels = await recorder.call("review_platform", "get_merchant_qa", {"merchant_id": CATERER_ID})
        _require_result_terms(labels, [["milk", "lactose"], ["halal"], ["separate boxes"], ["7800"]], "catering label correction")
        await _notion_page(recorder, stage)
    elif stage == 12:
        await recorder.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 300})
        shift = await recorder.call("calendar", "get_event", {"event_id": "cal_customer_escalation_0712", "calendar_id": CALENDAR_ID})
        _require_result_terms(shift, [["technical support"], ["coverage"], ["13:00"]], "support coverage event")
        await _notion_page(recorder, stage)
    elif stage == 13:
        credential = await recorder.call("email", "read_email", {"email_id": "1001"})
        _require_result_terms(credential, [["credential"], ["missing"], ["non-diagnostic"]], "credential email")
        await _notion_page(recorder, stage)
    elif stage == 14:
        await recorder.call("review_platform", "get_merchant", {"merchant_id": FACILITATOR_ID})
        await recorder.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 300})
        await _notion_page(recorder, stage)
    elif stage == 15:
        account_change = await recorder.call("email", "read_email", {"email_id": "1002"})
        _require_result_terms(account_change, [["personal account"], ["company account"]], "account-change email")
        await recorder.call("credit_card", "list_cards", {"user_id": USER_ID})
        await _notion_page(recorder, stage)
    elif stage == 16:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page_size": 50})
        await _notion_page(recorder, stage)
    elif stage == 17:
        await recorder.call("credit_card", "list_cards", {"user_id": USER_ID})
        await recorder.call("credit_card", "get_card", {"card_id": CARD_ID})
        await _notion_page(recorder, stage)
    elif stage == 18:
        await recorder.call("review_platform", "get_merchant_qa", {"merchant_id": FACILITATOR_ID})
        await recorder.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 300})
        await recorder.call("maps", "get_place_details", {"place_id": "place_core_0"})
        await recorder.call("email", "search_emails", {"query": "vendor", "page_size": 50})
        await _notion_page(recorder, stage)
    elif stage == 19:
        await recorder.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await _notion_page(recorder, stage)
    elif stage == 20:
        await _notion_page(recorder, stage)
        await recorder.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
    elif stage == 21:
        await recorder.call("maps", "search_places", {"query": "Beijing office meeting room", "limit": 20})
        await recorder.call("notification_hub", "list_notifications", {"user_id": USER_ID, "limit": 200})
        await recorder.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 300})
        await _notion_page(recorder, stage)
    elif stage == 22:
        feedback = await recorder.call("notion", "API-post-search", {
            "query": "Technical Support",
            "filter": {"value": "page"},
            "page_size": 100,
        })
        _require_result_terms(feedback, [["technical support"], ["3.5"], ["miss"]], "support feedback")
        await _notion_page(recorder, stage)
    elif stage == 23:
        unbilled = await recorder.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        context["transactions"] = _event_transactions(unbilled)
        await recorder.call("credit_card", "get_card", {"card_id": CARD_ID})
        await _notion_page(recorder, stage)
    elif stage == 24:
        unbilled = await recorder.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        context["transactions"] = _event_transactions(unbilled)
        await recorder.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 300})
        await recorder.call("review_platform", "get_merchant", {"merchant_id": VENUE_ID})
        await _notion_page(recorder, stage)
    else:
        raise ValueError(f"unsupported virtual stage: {stage}")
    await _save_draft(recorder, stage)
    return context


async def _handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])
    context = await _stage_calls(recorder, stage)
    _write_artifacts(stage, context)
    state["events"] = [row for row in state["events"] if isinstance(row, dict) and row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": stage})


async def _handle_call(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    del state, spec
    arguments = action.get("arguments") or {}
    if not isinstance(arguments, dict):
        raise ValueError("call arguments must be an object")
    await recorder.call(str(action.get("service") or ""), str(action.get("tool") or ""), dict(arguments))


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
    "call": _handle_call,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight")
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["actions"], list) or not spec["actions"]:
        raise ValueError("actions must be a non-empty list")
    if not isinstance(spec["expected_env"], dict):
        raise ValueError("expected_env must be an object")
    for key in ("preceding_releases", "released_mutations"):
        if not isinstance(spec["expected_env"].get(key), list):
            raise ValueError(f"expected_env.{key} must be a list")
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
            {"step_id": 2, "source": "agent", "message": response, "tool_calls": [
                {"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in recorder.calls
            ], "observation": {"results": [
                {"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in recorder.calls
            ]}, "llm_call_count": 0},
        ],
        "final_metrics": {"tool_calls": len(recorder.calls), "tool_errors": sum(not row["success"] for row in recorder.calls)},
    }
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
    print(response)
    return response


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: oracle.py STEP_SPEC", file=sys.stderr)
        return 1
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        asyncio.run(_run(spec))
        return 0
    except Exception as exc:
        print(f"oracle.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
