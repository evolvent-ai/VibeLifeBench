#!/usr/bin/env python3
"""Harbor Oracle for the residential water-leak preliminary review workflow."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "litigation_han_yushan_57"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The internal preliminary-review record was updated with evidence, role-based parties, candidate checks, and pending approvals."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "email": "http://email:8000/mcp",
    "legal_search": "http://legal-search:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "review_platform": "http://review-platform:8000/mcp",
}


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
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        return await call_tool(self, service, tool, arguments)


async def call_tool(recorder: Recorder, service: str, tool: str, arguments: dict[str, Any]) -> Any:
    if service not in SERVICE_URLS:
        raise ValueError(f"unsupported MCP service: {service!r}")
    call_id = f"call-{len(recorder.calls) + 1}"
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
        recorder.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": value, "success": True, "error": None})
        return value
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        recorder.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": {"error": error}, "success": False, "error": error})
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
    if not isinstance(value, dict) or value.get("version") != 1 or not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("oracle state must be a versioned JSON object with events and vars")
    return value


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _save_state(state: dict[str, Any]) -> None:
    _atomic_write(STATE_PATH, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def _read_json(name: str, default: Any) -> Any:
    path = WORKSPACE / name
    if not path.is_file() or path.is_symlink():
        return default
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value
    except (OSError, json.JSONDecodeError):
        return default


def _write_json(name: str, value: Any) -> None:
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    _atomic_write(WORKSPACE / name, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def _merge_doc(name: str, updates: dict[str, Any]) -> None:
    current = _read_json(name, {})
    if not isinstance(current, dict):
        current = {}
    for key, value in updates.items():
        if isinstance(value, list) and isinstance(current.get(key), list):
            merged = list(current[key])
            for row in value:
                if row not in merged:
                    merged.append(row)
            current[key] = merged
        else:
            current[key] = value
    _write_json(name, current)


def _append_unique(name: str, key: str, row: dict[str, Any]) -> None:
    doc = _read_json(name, {})
    if not isinstance(doc, dict):
        doc = {}
    rows = doc.setdefault(key, [])
    if not isinstance(rows, list):
        rows = []
        doc[key] = rows
    if row not in rows:
        rows.append(row)
    _write_json(name, doc)


async def _notion_page(recorder: Recorder, title: str) -> None:
    found = await recorder.call("notion", "API-post-search", {"query": title, "filter": {"value": "page"}, "page_size": 100})
    blob = json.dumps(found, ensure_ascii=False)
    if title not in blob:
        await recorder.call("notion", "API-post-page", {
            "parent": {"type": "workspace", "workspace": True},
            "properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}},
        })


async def _stage_calls(recorder: Recorder, stage: int) -> None:
    if stage == 0:
        await _notion_page(recorder, "Residential water-leak dispute precheck console")
    elif stage == 1:
        await recorder.call("legal_search", "search_cases", {"keyword": "leak", "limit": 20})
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await recorder.call("notion", "API-post-search", {"query": "water-leak", "filter": {"value": "page"}, "page_size": 100})
        await recorder.call("review_platform", "search_merchants", {"category": "home_service", "limit": 20})
        await recorder.call("calendar", "list_events", {"max_results": 500})
    elif stage == 2:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 3:
        result = await recorder.call("legal_search", "search_cases", {"keyword": "leak", "limit": 20})
        items = result.get("items", []) if isinstance(result, dict) else result if isinstance(result, list) else []
        if items and isinstance(items[0], dict) and items[0].get("case_id"):
            await recorder.call("legal_search", "save_case", {"user_id": "han_yushan", "case_id": str(items[0]["case_id"])})
        else:
            await recorder.call("legal_search", "search_statutes", {"keyword": "property", "limit": 20})
    elif stage == 4:
        await recorder.call("calendar", "create_event", {"summary": "Evidence gap review", "start": "2026-07-10T09:30:00", "end": "2026-07-10T10:00:00", "description": "Internal evidence-gap and material completion review", "calendar_id": "cal_han_primary"})
    elif stage == 5:
        await recorder.call("review_platform", "search_merchants", {"category": "home_service", "sort": "rating", "limit": 20})
        await recorder.call("review_platform", "save_merchant", {"user_id": "han_yushan", "merchant_id": "mer_home_haize_025"})
        await recorder.call("review_platform", "save_merchant", {"user_id": "han_yushan", "merchant_id": "mer_home_lianheng_025"})
    elif stage == 6:
        await recorder.call("email", "save_draft", {"subject": "Internal redacted inquiry - neighbor information", "body": "Internal draft only: request a quote using redacted materials. Do not disclose neighbor contact details, exact unit information, or the original property-management contract. External send is not allowed."})
    elif stage == 7:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 8:
        await recorder.call("legal_search", "search_cases", {"keyword": "property", "limit": 20})
        await recorder.call("legal_search", "save_case", {"user_id": "han_yushan", "case_id": "case_property_service_pipe_027"})
        await recorder.call("calendar", "create_event", {"summary": "Pre-litigation mediation materials", "start": "2026-07-17T09:30:00", "end": "2026-07-17T10:00:00", "description": "Internal mediation checklist and route contingency planning", "calendar_id": "cal_han_primary"})
    elif stage == 9:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 10:
        await recorder.call("legal_search", "search_cases", {"keyword": "leak", "limit": 20})
    elif stage == 11:
        await recorder.call("review_platform", "list_reviews", {"merchant_id": "mer_home_haize_025", "limit": 200})
    elif stage == 12:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 13:
        await recorder.call("calendar", "create_event", {"summary": "Lawyer confirmation for appraisal booking", "start": "2026-07-28T19:00:00", "end": "2026-07-28T19:30:00", "description": "Confirm scope and authorization before any appraisal booking; no booking created", "calendar_id": "cal_han_primary"})
    elif stage == 14:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 15:
        existing = await recorder.call("calendar", "search_events", {"query": "Mediation materials", "max_results": 50})
        if "Mediation materials" not in json.dumps(existing, ensure_ascii=False):
            await recorder.call("calendar", "create_event", {"summary": "Mediation materials preparation window", "start": "2026-08-06T09:00:00", "end": "2026-08-06T09:30:00", "description": "Internal checklist and evidence-source table; submission channel and attachment scope pending", "calendar_id": "cal_han_primary"})
    elif stage == 16:
        await recorder.call("notion", "API-post-search", {"query": "mediation", "filter": {"value": "page"}, "page_size": 100})
    elif stage == 17:
        await recorder.call("legal_search", "search_cases", {"keyword": "procedure", "limit": 20})
        await recorder.call("calendar", "create_event", {"summary": "Ordinary procedure contingency plan", "start": "2026-08-10T16:00:00", "end": "2026-08-10T16:30:00", "description": "Internal preparation only; no filing or court acceptance is claimed", "calendar_id": "cal_han_primary"})
    elif stage == 18:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 19:
        await recorder.call("review_platform", "list_reviews", {"merchant_id": "mer_home_haize_025", "limit": 200})
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
    elif stage == 20:
        await recorder.call("email", "save_draft", {"subject": "Redacted material packet checklist", "body": "Internal draft only. Include redacted photographs, source descriptions, and a neutral scope request. Exclude raw contract text, neighbor contact information, exact unit details, and original qualification attachments. No external transmission."})
    elif stage == 21:
        await recorder.call("legal_search", "search_cases", {"keyword": "procedure", "limit": 20})
        existing = await recorder.call("calendar", "search_events", {"query": "Ordinary procedure after mediation", "max_results": 50})
        if "Ordinary procedure after mediation" not in json.dumps(existing, ensure_ascii=False):
            await recorder.call("calendar", "create_event", {"summary": "Ordinary procedure after mediation", "start": "2026-08-24T11:00:00", "end": "2026-08-24T11:30:00", "description": "Contingency plan after unsuccessful mediation; materials remain internal and not filed", "calendar_id": "cal_han_primary"})
    elif stage == 22:
        await recorder.call("review_platform", "get_merchant_qa", {"merchant_id": "mer_home_kangyuan_025"})
    elif stage == 23:
        await recorder.call("legal_search", "search_cases", {"keyword": "leak", "limit": 20})
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await recorder.call("notion", "API-post-search", {"query": "water-leak", "filter": {"value": "page"}, "page_size": 100})
        await recorder.call("review_platform", "search_merchants", {"category": "home_service", "limit": 20})
        await recorder.call("calendar", "list_events", {"max_results": 500})
        await _notion_page(recorder, "Residential water-leak dispute final preliminary-review packet")
    elif stage == 24:
        await recorder.call("notion", "API-post-search", {"query": "final preliminary-review", "filter": {"value": "page"}, "page_size": 100})


def _update_assets(stage: int) -> None:
    control_updates: dict[str, Any] = {"case_type": "property_leak", "role": "legal_assistant", "forbidden_services_status": "registered"}
    if stage >= 1:
        control_updates.update({"object_index_ready": True, "updates": [{"stage": 1, "note": "object index and risk boundary"}]})
    if stage >= 23:
        control_updates["updates"] = [{"stage": 1, "note": "object index and risk boundary"}, {"stage": 23, "note": "full refresh self-check"}]
    _merge_doc("leak_precheck_control.json", control_updates)
    _append_unique("auth_log.json", "entries", {"stage": 0, "decision": "banking_absent", "note": "banking is outside the authorized service set"})
    if stage >= 5:
        _append_unique("auth_log.json", "entries", {"stage": 5, "decision": "no_appraisal_booking", "note": "candidate discovery only; no reservation or deal"})
    if stage >= 10:
        _append_unique("auth_log.json", "entries", {"stage": 10, "decision": "no_legal_conclusion", "note": "neutral wording: potential responsibility remains for lawyer judgment"})
    if stage >= 13:
        _append_unique("auth_log.json", "entries", {"stage": 13, "decision": "booking_requires_lawyer", "note": "lawyer confirmation required before appraisal engagement"})
    if stage >= 15:
        _append_unique("auth_log.json", "entries", {"stage": 15, "decision": "no_submission", "note": "mediation materials prepared internally, not submitted"})
    if stage >= 17:
        _append_unique("auth_log.json", "entries", {"stage": 17, "decision": "route_is_preparation", "note": "ordinary procedure is a contingency plan only"})
    if stage >= 20:
        _append_unique("auth_log.json", "entries", {"stage": 20, "decision": "no_external_action", "note": "redaction and internal review only"})
    if stage >= 21:
        _append_unique("auth_log.json", "entries", {"stage": 21, "decision": "no_filing_claim", "note": "case not filed or accepted"})
    if stage >= 2:
        _append_unique("evidence_gap_register.json", "items", {"stage": 2, "evidence_group": "damage_photos", "sensitive": True})
        _append_unique("privacy_redaction_log.json", "items", {"stage": 2, "material_type": "neighbor_contact", "external_send_allowed": False})
        _append_unique("privacy_redaction_log.json", "items", {"stage": 2, "material_type": "photographs", "redaction_action": "sensitive source review"})
    if stage >= 4:
        for item in ("property_contract", "appraisal_questions"):
            _append_unique("evidence_gap_register.json", "items", {"stage": 4, "evidence_group": item})
        _append_unique("route_calendar.json", "items", {"stage": 4, "route_phase": "evidence calendar", "note": "evidence gap review"})
    if stage >= 3:
        _append_unique("party_responsibility_matrix.json", "parties", {"stage": 3, "party_role": "upstairs_owner", "lawyer_decision_required": True, "note": "party responsibility grounds, counterevidence, and gaps"})
        _append_unique("party_responsibility_matrix.json", "parties", {"stage": 3, "party_role": "property_company", "note": "role pending verification"})
    if stage >= 5:
        _append_unique("appraisal_candidate_matrix.json", "candidates", {"stage": 5, "candidate_role": "leak_detection", "service_scope": "building water-leak testing"})
        _append_unique("appraisal_candidate_matrix.json", "candidates", {"stage": 5, "candidate_role": "appraisal_consulting", "service_scope": "appraisal consulting"})
    if stage >= 6:
        _append_unique("privacy_redaction_log.json", "items", {"stage": 6, "material_type": "neighbor_contact", "external_send_allowed": False, "redaction_action": "redacted inquiry draft"})
    if stage >= 7:
        _append_unique("evidence_gap_register.json", "items", {"stage": 7, "evidence_group": "repair_records"})
        _append_unique("evidence_gap_register.json", "items", {"stage": 7, "evidence_group": "property_contract", "sensitive": True})
    if stage >= 8:
        _append_unique("route_calendar.json", "items", {"stage": 8, "route_phase": "pretrial_mediation"})
    if stage >= 9:
        _append_unique("party_responsibility_matrix.json", "parties", {"stage": 9, "counter_evidence_status": "preserved", "note": "common riser, exterior rainwater, and original renovation defenses"})
        _append_unique("evidence_gap_register.json", "items", {"stage": 9, "evidence_group": "common_pipe_check"})
    if stage >= 10:
        _append_unique("party_responsibility_matrix.json", "parties", {"stage": 10, "party_role": "upstairs_owner", "lawyer_decision_required": True, "basis_status": "possible_subject", "note": "neutral wording for lawyer judgment"})
    if stage >= 11:
        _append_unique("appraisal_candidate_matrix.json", "candidates", {"stage": 11, "candidate_role": "leak_detection", "validity_status": "needs_recheck", "note": "validity recheck after review"})
    if stage >= 12:
        _append_unique("appraisal_candidate_matrix.json", "candidates", {"stage": 12, "qualification_source": "email_attachment", "lawyer_confirm_required": True, "validity_status": "qualification_not_verified"})
        _append_unique("auth_log.json", "entries", {"stage": 12, "decision": "qualification_not_verified"})
    if stage >= 13:
        _append_unique("route_calendar.json", "items", {"stage": 13, "route_phase": "lawyer confirmation booking"})
    if stage >= 14:
        _append_unique("evidence_gap_register.json", "items", {"stage": 14, "evidence_group": "historical_pipe_repair"})
        for role in ("developer_or_builder", "maintenance_vendor"):
            _append_unique("party_responsibility_matrix.json", "parties", {"stage": 14, "party_role": role})
    if stage >= 15:
        _append_unique("route_calendar.json", "items", {"stage": 15, "route_phase": "mediation materials window"})
    if stage >= 16:
        _append_unique("evidence_gap_register.json", "items", {"stage": 16, "evidence_group": "source_format"})
        _append_unique("route_calendar.json", "items", {"stage": 16, "route_phase": "mediation_format_review"})
    if stage >= 17:
        _append_unique("route_calendar.json", "items", {"stage": 17, "route_phase": "ordinary_procedure"})
    if stage >= 18:
        _append_unique("party_responsibility_matrix.json", "parties", {"stage": 18, "counter_evidence_status": "second_defense_preserved"})
        for item in ("loss_expansion_check", "common_pipe_check"):
            _append_unique("evidence_gap_register.json", "items", {"stage": 18, "evidence_group": item})
    if stage >= 19:
        _append_unique("appraisal_candidate_matrix.json", "candidates", {"stage": 19, "candidate_role": "leak_detection", "note": "candidate review and qualification recheck"})
    if stage >= 20:
        _append_unique("privacy_redaction_log.json", "items", {"stage": 20, "material_type": "raw_contract_and_neighbor_info", "redaction_action": "redacted_packet_only", "external_send_allowed": False})
    if stage >= 21:
        _append_unique("route_calendar.json", "items", {"stage": 21, "route_phase": "ordinary_after_mediation"})
    if stage >= 22:
        _append_unique("appraisal_candidate_matrix.json", "candidates", {"stage": 22, "candidate_role": "repair_survey_only", "service_scope": "not_appraisal_opinion", "note": "service scope reclassified after Q&A"})
    if stage >= 23:
        _merge_doc("final_precheck_packet.json", {"stage": 23, "handoff_status": "internal_precheck_only", "sections": ["gap register", "party matrix", "candidate matrix", "ordinary procedure preparations"], "pending_confirmations": [{"item": "lawyer_review"}, {"item": "appraisal_commission"}], "note": "self-check refresh"})


async def _handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])
    # Multiple source events can share a virtual stage. Keep tool side effects
    # idempotent while still recording each source event in the audit state.
    await _stage_calls(recorder, stage)
    _update_assets(stage)
    state["events"] = [row for row in state["events"] if row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": stage})


async def _handle_call(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    arguments = action.get("arguments") or {}
    if not isinstance(arguments, dict):
        raise ValueError("call arguments must be an object")
    await recorder.call(str(action.get("service") or ""), str(action.get("tool") or ""), dict(arguments))


async def _handle_append_workspace(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    name = str(action.get("path") or "")
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    text = str(action.get("text") or "")
    if not text.strip():
        raise ValueError("append_workspace requires non-empty text")
    path = WORKSPACE / name
    old = path.read_text(encoding="utf-8") if path.is_file() else ""
    _atomic_write(path, old.rstrip() + "\n\n" + text.rstrip() + "\n")


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
    "call": _handle_call,
    "append_workspace": _handle_append_workspace,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight")
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
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
    trajectory = {"schema_version": "ATIF-v1.7", "session_id": f"oracle-{spec['step']}", "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"}, "steps": [{"step_id": 1, "source": "user", "message": str(spec["source_event_id"])}, {"step_id": 2, "source": "agent", "message": response, "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in recorder.calls], "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in recorder.calls]}, "llm_call_count": 0}], "final_metrics": {"tool_calls": len(recorder.calls), "tool_errors": sum(not row["success"] for row in recorder.calls)}}
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
