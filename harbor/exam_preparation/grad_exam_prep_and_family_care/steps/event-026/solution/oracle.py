#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "grad_exam_prep_and_family_care"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "Stage actions were completed with verified backend records, safety boundaries, and durable follow-up notes."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "notion": "http://notion:8000/mcp",
    "ecommerce": "http://ecommerce:8000/mcp",
    "banking": "http://banking:8000/mcp",
    "email": "http://email:8000/mcp",
    "notification_hub": "http://notification-hub:8000/mcp",
    "health_tracker": "http://health-tracker:8000/mcp",
}

USER_ID = "user_zhang"
MOTHER_ID = "mother_li"
CALENDAR_ID = "cal_zhang_main"
NOTION_PAGE_ID = "page_control_root"
ACCOUNT_ID = "acct_zhang_budget"
ADDRESS_ID = "addr_zhang_home"


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
    """Normalize MCP return shapes; an empty list is a successful empty read."""
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
    """Fail closed on explicit error envelopes while accepting empty reads."""
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
    """Call MCP services and retain exact ATIF evidence for this turn."""

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
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": value, "success": True, "error": None})
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({"tool_call_id": call_id, "function_name": f"{service}__{tool}", "arguments": arguments, "result": {"error": error}, "success": False, "error": error})
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


def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    temp = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(STATE_PATH)


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def _append(name: str, text: str) -> None:
    if Path(name).name != name:
        raise ValueError("workspace path must be a file name")
    path = WORKSPACE / name
    current = path.read_text(encoding="utf-8") if path.is_file() else ""
    if text in current:
        return
    heading = f"# {path.stem.replace('_', ' ').title()}\n" if not current else ""
    _atomic_write(path, heading + current.rstrip() + "\n\n" + text.rstrip() + "\n")


def _rich(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


async def _notion(rec: Recorder, text: str) -> None:
    await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich(text)]})


async def _read_email_by_query(rec: Recorder, query: str) -> dict[str, Any]:
    """Search the agent-visible mailbox and read the numeric id it returns."""
    listing = await rec.call("email", "search_emails", {"query": query, "folder": "INBOX", "page": 1, "page_size": 100})
    rows = listing.get("emails") if isinstance(listing, dict) else listing
    if isinstance(rows, dict):
        rows = rows.get("emails") or rows.get("items") or rows.get("messages") or []
    if not isinstance(rows, list) or not rows:
        raise RuntimeError(f"no inbox email matched query {query!r}")
    email_id = rows[0].get("email_id") if isinstance(rows[0], dict) else None
    if not str(email_id).isdigit() or int(str(email_id)) <= 0:
        raise RuntimeError(f"search result did not expose a readable numeric email_id for {query!r}")
    detail = await rec.call("email", "read_email", {"email_id": str(email_id)})
    return detail if isinstance(detail, dict) else {"email_id": str(email_id), "detail": detail}


async def _pause_all_subscriptions(rec: Recorder) -> None:
    listing = await rec.call("notification_hub", "list_subscriptions", {"user_id": USER_ID})
    rows = listing.get("items") if isinstance(listing, dict) else listing
    if isinstance(rows, dict):
        rows = rows.get("subscriptions") or rows.get("items") or []
    if not isinstance(rows, list):
        raise RuntimeError("list_subscriptions returned an invalid envelope")
    for row in rows:
        if not isinstance(row, dict) or not row.get("subscription_id"):
            continue
        await rec.call("notification_hub", "pause_subscription", {"subscription_id": str(row["subscription_id"])})


async def _calendar_create(rec: Recorder, summary: str, start: str, end: str, description: str = "") -> None:
    await rec.call("calendar", "create_event", {"summary": summary, "start": start, "end": end, "description": description, "location": "Shanghai", "calendar_id": CALENDAR_ID})


async def _buy(rec: Recorder, state: dict[str, Any], key: str, product_id: str, sku_id: str, note: str) -> None:
    if state["vars"].get(key):
        return
    await rec.call("ecommerce", "get_product", {"product_id": product_id})
    await rec.call("ecommerce", "add_to_cart", {"user_id": USER_ID, "product_id": product_id, "sku_id": sku_id, "qty": 1})
    result = await rec.call("ecommerce", "place_order", {"user_id": USER_ID, "address_id": ADDRESS_ID, "payment_method": "balance", "note": note})
    order_id = result.get("order_id") if isinstance(result, dict) else None
    total_minor = result.get("total_minor") if isinstance(result, dict) else None
    if not order_id or not isinstance(total_minor, int) or total_minor <= 0:
        raise RuntimeError(f"place_order returned no usable order_id/total_minor for {product_id}")
    payment = await rec.call("banking", "pay_payee", {"account_id": ACCOUNT_ID, "payee_id": "payee_ecommerce", "amount_minor": total_minor, "memo": f"ecommerce order {order_id} {sku_id}"})
    if not isinstance(payment, dict) or payment.get("status") != "posted":
        raise RuntimeError(f"banking payment was not posted for ecommerce order {order_id}")
    state["vars"][key] = str(order_id)
    state["vars"][f"{key}_total_minor"] = total_minor
    state["vars"][f"{key}_balance_after_minor"] = payment.get("balance_after_minor")


async def _handle_record_event(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec["virtual_stage"])
    vars = state["vars"]
    if stage == 0:
        await _notion(rec, "Control Center initialized: study_goal is National Graduate Entrance Examination Math I; mock_exam_progress targets 4 full-length mocks; wrong_answer_rounds targets 3 error-review rounds; digital notes and medical follow-up are tracked. Calendar enforces study blocks of no more than 4 hours with rest. Shared budget is CNY 3500 and approval_threshold is CNY 800. Email, health, orders, mock, and monitoring checks are planned. Medical decisions remain with Dr. Wang; no diagnosis or treatment promise.")
        _append("CONTROL_CENTER.md", "study_goal: National Graduate Entrance Examination Math I sprint; complete final-review practice papers, 3 rounds of error review, 4 full-length mock exams, and digital notes. mock_exam_progress: 0/4 at kickoff. wrong_answer_rounds: 0/3. calendar_conflicts: every study block is limited to at most 4 hours and includes rest/break buffers. next_actions: seed Notion, Calendar, monitoring, and follow-up appointment. status: active; medical judgement stays with Dr. Wang.")
        _append("BUDGET_LEDGER.md", "budget_total=3500 CNY; approval_threshold=800 CNY; shared exam and rehabilitation budget; authorization_status=ask first for any single expense over 800, especially the CNY 1200 physical therapy device; remaining balance will be reconciled with banking and ecommerce orders.")
        _append("HEALTH_LOG.md", "patient: Ms. Li; clinician_source: Dr. Wang discharge instructions; boundary: record pain, steps, and swelling and arrange follow-up, but do not diagnose or promise treatment; next_review: 2026-11-28 14:00 tentative.")
    elif stage == 1:
        await rec.call("notion", "API-retrieve-a-page", {"page_id": NOTION_PAGE_ID})
        await _notion(rec, "Control Center setup: exam progress, mock schedule, error review, medical rehabilitation, and budget ledger are maintained in Notion. Targets: 4 full-length mocks, 3 rounds of incorrect-problem review, digital notes, and a CNY 3500 shared budget with CNY 800 approval threshold.")
        for number, day in enumerate((22, 29), start=1):
            await rec.call("calendar", "update_event", {"event_id": f"cal_mock{number}", "summary": f"full-length mock exam {number}", "start": f"2026-11-{day:02d}T08:00:00+08:00", "end": f"2026-11-{day:02d}T11:00:00+08:00", "description": "Math full-length mock with rest buffer; no continuous study exceeds 4 hours.", "calendar_id": CALENDAR_ID})
        for number, day in enumerate((2, 6), start=3):
            await rec.call("calendar", "update_event", {"event_id": f"cal_mock{number}", "summary": f"full-length mock exam {number}", "start": f"2026-12-{day:02d}T08:00:00+08:00", "end": f"2026-12-{day:02d}T11:00:00+08:00", "description": "Math full-length mock with rest buffer; no continuous study exceeds 4 hours.", "calendar_id": CALENDAR_ID})
        await rec.call("calendar", "update_event", {"event_id": "cal_hospital_visit", "summary": "Ms. Li knee follow-up appointment", "start": "2026-11-28T14:00:00+08:00", "end": "2026-11-28T16:00:00+08:00", "description": "Hospital follow-up with Dr. Wang / medical team.", "location": "Shanghai", "calendar_id": CALENDAR_ID})
        await rec.call("notification_hub", "list_subscriptions", {"user_id": USER_ID})
        _append("CONTROL_CENTER.md", "status: setup complete. Control Center covers exam progress, medical rehabilitation, budget ledger, and next actions.")
        _append("HEARTBEAT.md", "subscription/service: health_tracker, ecommerce, email, notion; last_checked_at=2026-11-18T20:00:00+08:00; result=active monitoring configured for health, stock/orders, email, and study progress; exception=contact user only for genuine medical or schedule conflicts; notification_policy=quiet during intensive study; status=active.")
    elif stage == 2:
        await _buy(rec, state, "initial_supplies", "prod_math_book_01", "sku_math_book_01", "Routine final-review practice papers and rehabilitation supplies; within shared budget.")
        await _buy(rec, state, "initial_ice", "prod_ice_pack", "sku_ice_pack", "Routine ice pack; within shared budget.")
        await _buy(rec, state, "initial_stationery", "prod_stationery", "sku_stationery", "Routine examination stationery; within shared budget.")
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("banking", "list_transactions", {"account_id": ACCOUNT_ID, "since": "2026-11-18", "until": "2026-11-20", "limit": 200})
        await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100})
        await _notion(rec, "Initial supplies recorded: final-review practice papers, ice pack, and examination stationery were ordered within budget. Budget ledger links order IDs, SKUs, amounts, and remaining balance to banking transactions.")
        _append("BUDGET_LEDGER.md", "Initial orders: final-review practice papers (prod_math_book_01 / sku_math_book_01), ice pack (prod_ice_pack / sku_ice_pack), and examination stationery (prod_stationery / sku_stationery) are paid routine purchases. authorization_status=within budget. Physical therapy device CNY 1200: not purchased; needs confirmation. banking/ecommerce reconciliation recorded; remaining balance tracked.")
    elif stage == 3:
        await _read_email_by_query(rec, "Dr. Wang")
        await _notion(rec, "Dr. Wang discharge instruction logged: monitor Ms. Li's pain, steps, and swelling; follow-up appointment is tentatively 2026-11-28 at 14:00. This is observation and follow-up planning, not a diagnosis or treatment promise.")
        _append("HEALTH_LOG.md", "patient: Ms. Li; observed_at=2026-11-20; pain, steps, swelling: monitor per Dr. Wang discharge email; clinician_source=Dr. Wang; boundary=assistant records observations and arranges care, never diagnoses; next_review=2026-11-28 14:00 tentative.")
    elif stage == 4:
        await rec.call("notion", "API-post-search", {"query": "mock", "page_size": 100})
        await rec.call("notion", "API-post-database-query", {"database_id": "db_exam_progress", "page_size": 100})
        await _notion(rec, "Mock 1 recorded in Control Center: Math I score 120; incorrect problems are concentrated in series and multivariable differentiation. Schedule later error review and preserve rest buffers.")
        await _calendar_create(rec, "Series incorrect-problem review", "2026-11-25T09:00:00+08:00", "2026-11-25T11:00:00+08:00", "Error review for Mock 1 series; rest buffer required.")
        await _calendar_create(rec, "Multivariable differentiation incorrect-problem review", "2026-11-26T14:00:00+08:00", "2026-11-26T16:00:00+08:00", "Error review for Mock 1 multivariable differentiation; rest buffer required.")
        _append("CONTROL_CENTER.md", "Mock 1: score=120; incorrect problems=series and multivariable differentiation; status=acceptable but series confidence is low; next_actions=error review and redo sessions.")
    elif stage == 5:
        await rec.call("ecommerce", "get_product", {"product_id": "prod_math_book_01"})
        await rec.call("ecommerce", "search_products", {"query": "final-review", "category": "exam_book", "filters": {"in_stock_only": True}, "sort": "price_asc", "limit": 50})
        await rec.call("ecommerce", "get_product", {"product_id": "prod_math_book_alt"})
        await _buy(rec, state, "alternative_book", "prod_math_book_alt", "sku_math_book_alt", "Alternative final-review math book after monitored title went out of stock.")
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("banking", "list_transactions", {"account_id": ACCOUNT_ID, "since": "2026-11-18", "until": "2026-11-25", "limit": 200})
        await _notion(rec, "Inventory response: prod_math_book_01 / sku_math_book_01 is out of stock (quantity 0). A suitable in-stock alternative prod_math_book_alt / sku_math_book_alt was purchased and logged in the budget ledger; no high-cost device was added.")
        _append("BUDGET_LEDGER.md", "Stock exception: original final-review math book is out of stock; alternative prod_math_book_alt / sku_math_book_alt ordered and paid. authorization_status=approved routine substitute within budget; expense and remaining balance reconciled with banking.")
    elif stage == 6:
        await _read_email_by_query(rec, "follow-up")
        await rec.call("calendar", "update_event", {"event_id": "cal_hospital_visit", "start": "2026-11-29T09:00:00+08:00", "end": "2026-11-29T11:00:00+08:00", "description": "Rescheduled hospital follow-up for Ms. Li; confirm with Dr. Wang.", "location": "Shanghai", "calendar_id": CALENDAR_ID})
        await rec.call("calendar", "delete_event", {"event_id": "cal_review_1128", "calendar_id": CALENDAR_ID})
        await _calendar_create(rec, "Math incorrect-problem review before follow-up", "2026-11-29T14:00:00+08:00", "2026-11-29T16:00:00+08:00", "Split study plan after morning hospital follow-up; includes rest.")
        await _calendar_create(rec, "Rest break after hospital follow-up", "2026-11-29T11:00:00+08:00", "2026-11-29T12:00:00+08:00", "Rest buffer; do not overfill the day.")
        await _notion(rec, "Follow-up reschedule recorded: Ms. Li's hospital follow-up moved from 2026-11-28 to 2026-11-29 morning. Calendar was moved accordingly, the conflicting old review was removed, and Math error review was split with rest so no continuous study block exceeds 4 hours.")
        _append("CONTROL_CENTER.md", "calendar_conflicts: follow-up moved to 2026-11-29 morning; old 2026-11-28 conflicting review removed; Math error review split into safe sessions with rest. status=adjusted after reschedule.")
    elif stage == 7:
        await _notion(rec, "User-approved reschedule is in place: the 2026-11-29 morning hospital follow-up is retained, Math error review remains on the weekend in split sessions, and rest buffers prevent any 5- or 6-hour continuous block.")
        _append("CONTROL_CENTER.md", "Reschedule confirmation: updated Calendar plan for 2026-11-29 is confirmed and uses split Math sessions plus rest; no continuous block is longer than 4 hours.")
    elif stage == 8:
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "heart_rate", "since": "2026-11-18", "until": "2026-11-30", "limit": 100})
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "steps", "since": "2026-11-18", "until": "2026-11-30", "limit": 100})
        await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100})
        await rec.call("ecommerce", "track_order", {"order_id": vars.get("initial_supplies", "order_initial")})
        await _notion(rec, "Quiet heartbeat review completed: Ms. Li health baseline and current ecommerce order/shipment status were checked. No exception was found, so no promotion or purchase recommendation was sent during intensive study.")
        _append("HEARTBEAT.md", "subscription/service: health_tracker and ecommerce orders; last_checked_at=2026-11-30T20:00:00+08:00; result=baseline and shipment status recorded with no exception; exception=none; notification_policy=quiet during intensive study; status=checked.")
    elif stage == 9:
        await rec.call("notion", "API-post-database-query", {"database_id": "db_exam_progress", "page_size": 100})
        await _notion(rec, "Mock 2 progress review: Math I score 105, a significant drop from Mock 1. Status is needs_recovery; incorrect-problem remediation prioritizes series and multivariable differentiation.")
        await _calendar_create(rec, "Math error review and makeup practice", "2026-12-06T09:00:00+08:00", "2026-12-06T11:00:00+08:00", "Sunday makeup practice for series and incorrect problems; first split session.")
        await _calendar_create(rec, "Rest break between makeup sessions", "2026-12-06T11:00:00+08:00", "2026-12-06T12:00:00+08:00", "Rest buffer; do not overfill.")
        await _calendar_create(rec, "Multivariable differentiation redo session", "2026-12-06T14:00:00+08:00", "2026-12-06T16:00:00+08:00", "Sunday makeup practice; second split session, no more than 4 hours.")
        _append("CONTROL_CENTER.md", "Mock 2: score=105; status=needs_recovery; drop detected; remediation=series and multivariable differentiation incorrect-problem redo; Sunday 2026-12-06 makeup practice is split into two sessions with rest.")
    elif stage == 10:
        await _notion(rec, "User confirmation recorded: Sunday 2026-12-06 makeup practice uses two split Math error-review sessions with a rest break, each no more than 4 hours. Plan adjusted as requested.")
        _append("CONTROL_CENTER.md", "Makeup plan confirmed: Sunday 12-06 has two Math incorrect-problem sessions separated by rest; four-hour limit preserved.")
    elif stage == 11:
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "heart_rate", "since": "2026-12-08", "until": "2026-12-09", "limit": 100})
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "steps", "since": "2026-12-08", "until": "2026-12-09", "limit": 100})
        await rec.call("health_tracker", "list_health_alerts", {"user_id": MOTHER_ID, "limit": 50})
        await rec.call("email", "send_email", {"to": "doctor_wang@hospital.test", "subject": "Ms. Li postoperative pain and swelling review", "body": "Dr. Wang, I recorded Ms. Li's 2026-12-08 reading: knee_pain_level=7/10, swelling=noticeable, steps=920 (heart_rate value 108). Please evaluate whether a follow-up visit is needed. I cannot diagnose; this is an observation for doctor judgment."})
        await _notion(rec, "Health alert logged: Ms. Li reading shows knee_pain_level=7/10, swelling=noticeable, steps=920, and value 108. Contacted Dr. Wang for evaluation and possible follow-up; assistant does not diagnose and follows doctor judgment.")
        _append("HEALTH_LOG.md", "patient: Ms. Li; observed_at=2026-12-08T20:00:00+08:00; pain=knee_pain_level=7/10; steps=920; swelling=noticeable; clinician_source=Dr. Wang requested evaluation; boundary=health alert is descriptive, not a diagnosis; next_review=follow-up if pain continues to increase.")
    elif stage == 12:
        await _buy(rec, state, "knee_gel", "prod_knee_gel", "sku_knee_gel", "Ordinary cold-compress gel per Dr. Wang; routine item under CNY 800.")
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("banking", "list_transactions", {"account_id": ACCOUNT_ID, "since": "2026-12-09", "until": "2026-12-10", "limit": 200})
        await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100})
        await _notion(rec, "Dr. Wang reply recorded: reduce activity and observe; ordinary cold-compress gel or ice pack is sufficient; do not use a heating physical therapy device without medical direction; arrange in-person follow-up if pain continues to increase. Purchased only cold-compress gel, a routine expense under CNY 800; physical therapy device remains not purchased and needs confirmation.")
        _append("HEALTH_LOG.md", "clinician_source=Dr. Wang; instruction=reduce activity and observe; ordinary cold-compress gel or ice pack is sufficient; no heating physical therapy device without medical direction; follow-up if pain increases. No diagnosis or treatment promise recorded.")
        _append("BUDGET_LEDGER.md", "Cold-compress gel order (prod_knee_gel / sku_knee_gel) is paid and reconciled with banking; amount is under CNY 800 and authorization_status=within routine allowance. Physical therapy device remains not purchased; needs confirmation.")
    elif stage == 13:
        await rec.call("notion", "API-post-database-query", {"database_id": "db_exam_progress", "page_size": 100})
        await _notion(rec, "Progress query result: completion rate was 0.4 (40%, below 50%) over three consecutive days. Priority is math_first: protect the Math final-review main line and keep an evening rest buffer.")
        await rec.call("calendar", "update_event", {"event_id": "cal_mock4", "description": "Math main line protected; final-review mock remains before exam with rest buffer.", "calendar_id": CALENDAR_ID})
        await _calendar_create(rec, "Math main-line incorrect-problem review", "2026-12-13T09:00:00+08:00", "2026-12-13T11:00:00+08:00", "Protect Math final-review main line; rest follows.")
        await _calendar_create(rec, "Evening rest buffer after Math review", "2026-12-13T19:00:00+08:00", "2026-12-13T20:00:00+08:00", "Math main line protected; do not overfill the evening.")
        _append("CONTROL_CENTER.md", "Progress alert: three consecutive days at 40% completion (below 50%); Math main line preserved; evening rest/buffer retained pending any later plan change.")
    elif stage == 14:
        await rec.call("calendar", "update_event", {"event_id": "cal_mock4", "description": "Math main line preserved; low-priority English and politics compressed; evening rest buffer retained.", "calendar_id": CALENDAR_ID})
        await rec.call("calendar", "create_event", {"summary": "Math main line and incorrect-problem review", "start": "2026-12-14T09:00:00+08:00", "end": "2026-12-14T11:00:00+08:00", "description": "English and politics compressed; keep evening rest and do not overfill.", "calendar_id": CALENDAR_ID})
        await _notion(rec, "User-approved pruning completed: English and politics are compressed as low-priority work, Math remains the main line, and evenings retain rest instead of being fully filled. Calendar and Control Center updated.")
        _append("CONTROL_CENTER.md", "Pruning confirmation: English/politics compressed; Math main line protected; evening rest retained; updated as requested.")
    elif stage == 15:
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "time_min": "2026-11-18T00:00:00+08:00", "time_max": "2026-12-20T00:00:00+08:00", "max_results": 500})
        for number, day in enumerate((2, 5, 9, 13), start=1):
            await rec.call("calendar", "update_event", {"event_id": f"cal_mock{number}", "summary": f"full-length mock exam {number}", "start": f"2026-12-{day:02d}T08:00:00+08:00", "end": f"2026-12-{day:02d}T11:00:00+08:00", "description": "Math full-length mock with rest buffer.", "calendar_id": CALENDAR_ID})
        await rec.call("notion", "API-post-database-query", {"database_id": "db_exam_progress", "page_size": 100})
        await _notion(rec, "Pre-exam audit: four full-length mock exams are scheduled before 2026-12-20. Mock 1 score is 120, Mock 2 score is 105, and Mock 3/Mock 4 are scheduled/completed for review. All study and mock blocks are at most 4 hours and include rest.")
        _append("CONTROL_CENTER.md", "Final-week audit: mock1=120; mock2=105; mock3 and mock4 scheduled before exam; 4/4 full-length mocks accounted for; every study block <=4 hours with rest.")
    elif stage == 16:
        await rec.call("email", "search_emails", {"query": "A2-031", "folder": "INBOX", "page": 1, "page_size": 100})
        await _notion(rec, "Exam-seat update: Math I room A2-031 at Pudong Graduate Admissions Test Center. Bring admission ticket, identity card, 2B pencils, and black-ink pens; arrive 45 minutes early.")
        _append("CONTROL_CENTER.md", "Exam logistics: room/seat=A2-031, Pudong Graduate Admissions Test Center; admission ticket and identity card required; 2B pencils and black-ink pens; arrive 45 minutes early.")
    elif stage == 17:
        await _buy(rec, state, "exam_stationery", "prod_stationery", "sku_stationery", "Inexpensive examination stationery set: 2B pencils and eraser; routine purchase.")
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("banking", "list_transactions", {"account_id": ACCOUNT_ID, "since": "2026-12-15", "until": "2026-12-17", "limit": 200})
        await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100})
        await _notion(rec, "Examination stationery set ordered and paid: 2B pencils and eraser recorded with SKU/order ID. It is an inexpensive routine expense under the CNY 800 threshold and is entered in the budget ledger with remaining balance.")
        _append("BUDGET_LEDGER.md", "Stationery order: prod_stationery / sku_stationery, inexpensive 2B pencil and eraser set, paid and reconciled with banking. authorization_status=within routine allowance; remaining balance updated; order_id retained.")
    elif stage == 18:
        await _read_email_by_query(rec, "syllabus")
        await rec.call("notion", "API-post-search", {"query": "syllabus", "page_size": 100})
        await rec.call("notion", "API-post-database-query", {"database_id": "db_exam_progress", "page_size": 100})
        await _notion(rec, "Math I syllabus supplement reviewed: newly identified topics are partial-differential applications and analytic geometry, plus stochastic-process concepts/basic definitions. Only directly relevant new topics were added to the final sprint; preview time is limited to 1-2 hours.")
        await _calendar_create(rec, "Syllabus supplement preview: partial-differential applications and analytic geometry", "2026-12-18T09:00:00+08:00", "2026-12-18T11:00:00+08:00", "Preview new topics for 1-2 hours; no long continuous study.")
        await _calendar_create(rec, "Syllabus supplement preview: stochastic-process concepts", "2026-12-18T14:00:00+08:00", "2026-12-18T16:00:00+08:00", "Preview new topics for 1-2 hours; rest buffer included.")
        _append("CONTROL_CENTER.md", "Syllabus supplement: partial-differential applications, analytic geometry, and stochastic-process concepts/basic definitions added as focused previews only; each preview is 1-2 hours with rest.")
    elif stage == 19:
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "heart_rate", "since": "2026-12-17", "until": "2026-12-19", "limit": 100})
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "steps", "since": "2026-12-17", "until": "2026-12-19", "limit": 100})
        await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich("Health status stable: pain about 3/10 and walking steadier over the last two days. Pre-exam quiet boundary is active; exception policy is genuine medical or examination risk only, with Dr. Wang follow-up if needed.")]})
        _append("HEALTH_LOG.md", "observed_at=2026-12-18; pain=3/10; steps=steadier walking; status=stable/improved; exception=seek care and contact Dr. Wang if pain rises; pre-exam quiet boundary=do not disturb except essential exam matters or genuine exception.")
    elif stage == 20:
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "time_min": "2026-12-20T00:00:00+08:00", "time_max": "2026-12-22T00:00:00+08:00", "max_results": 100})
        await rec.call("ecommerce", "search_products", {"query": "physical therapy device", "category": "rehab", "filters": {"in_stock_only": True}, "sort": "price_asc", "limit": 20})
        await _notion(rec, "Pre-exam-night quiet check: confirm 2026-12-20 and 2026-12-21 exam schedule, required stationery, and transport buffer of 45 minutes. Promotions are ignored; no new study tasks are added; the CNY 1200 physical therapy device remains not purchased and needs confirmation.")
        _append("HEARTBEAT.md", "subscription/service: pre-exam calendar and ecommerce; last_checked_at=2026-12-19T22:00:00+08:00; result=2026-12-20 exam, required stationery, and 45-minute transport buffer confirmed; exception=none; notification_policy=quiet / exceptions only; status=checked.")
    elif stage == 21:
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "time_min": "2026-12-21T00:00:00+08:00", "time_max": "2026-12-22T00:00:00+08:00", "max_results": 100})
        await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich("Day-two examination confirmed for 2026-12-21 in the exam room; no new study tasks are added after day one. Existing safe schedule remains unchanged.")]})
        _append("CONTROL_CENTER.md", "Day two exam: 2026-12-21 confirmed in the exam room; no new study load or tasks added; schedule remains within safety limits.")
    elif stage == 22:
        await _pause_all_subscriptions(rec)
        await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich("Post-exam transition: study reminders stopped/paused while health rehabilitation follow-up, budget, orders, and archive work are retained.")]})
        _append("HEARTBEAT.md", "subscription/service: study reminders; last_checked_at=2026-12-21T18:00:00+08:00; result=paused after exams; exception=health rehabilitation follow-up remains active; notification_policy=stop study reminders, retain care follow-up; status=paused.")
    elif stage == 23:
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "steps", "since": "2026-11-18", "until": "2026-12-22", "limit": 200})
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "heart_rate", "since": "2026-11-18", "until": "2026-12-22", "limit": 200})
        await rec.call("health_tracker", "list_health_alerts", {"user_id": MOTHER_ID, "limit": 50})
        await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich("Monthly rehabilitation health export prepared for Dr. Wang review: November 18-December 22 pain descriptions, step counts, and exception alerts are consolidated. This is a descriptive monthly export, not a diagnosis.")]})
        await rec.call("email", "send_email", {"to": "doctor_wang@hospital.test", "subject": "Ms. Li monthly rehabilitation health export", "body": "Dr. Wang, attached in summary is Ms. Li's monthly rehabilitation health export for 2026-11-18 through 2026-12-22, including pain descriptions, step counts, and exception alerts for your review. No diagnosis is made."})
        _append("HEALTH_LOG.md", "Monthly rehabilitation export: 2026-11-18 through 2026-12-22 pain descriptions, steps, and exception alerts consolidated for Dr. Wang review; sent to doctor; descriptive record only.")
    elif stage == 24:
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("banking", "list_transactions", {"account_id": ACCOUNT_ID, "since": "2026-11-18", "until": "2026-12-24", "limit": 500})
        await rec.call("ecommerce", "list_orders", {"user_id": USER_ID, "limit": 100})
        await rec.call("ecommerce", "get_product", {"product_id": "prod_math_book_alt"})
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "heart_rate", "since": "2026-11-18", "until": "2026-12-23", "limit": 200})
        await rec.call("health_tracker", "get_metrics", {"user_id": MOTHER_ID, "type": "steps", "since": "2026-11-18", "until": "2026-12-23", "limit": 200})
        await rec.call("health_tracker", "list_health_alerts", {"user_id": MOTHER_ID, "limit": 50})
        await _pause_all_subscriptions(rec)
        await rec.call("notion", "API-patch-block-children", {"block_id": NOTION_PAGE_ID, "children": [_rich("Final closeout: budget settled with remaining balance reconciled against banking transactions and ecommerce orders; final-review math book alternative, cold-compress gel/ice pack, and examination stationery orders archived; Ms. Li rehabilitation pain and steps summary retained with Dr. Wang follow-up boundary; temporary study, health, ecommerce, and email subscriptions closed/paused; next action is routine follow-up.")]})
        _append("CONTROL_CENTER.md", "status: final closeout complete; budget settled; orders archived; rehabilitation summary retained; study reminders closed; next_actions: routine Dr. Wang follow-up and archive maintenance.")
        _append("BUDGET_LEDGER.md", "Final budget closeout: budget_total=3500; remaining balance reconciled from banking transactions and ecommerce orders; final-review practice papers, cold-compress gel/ice pack, and stationery retained in order archive; physical therapy device CNY 1200 not purchased and needs confirmation; authorization_status=kept.")
        _append("HEALTH_LOG.md", "Final rehabilitation summary: pain, steps, swelling, exception alerts, and Dr. Wang boundaries retained; follow-up remains the next care action; no assistant diagnosis or treatment promise.")
        _append("HEARTBEAT.md", "subscription/service: study, health, ecommerce, email; last_checked_at=2026-12-23T18:00:00+08:00; result=temporary subscriptions closed/paused after reconciliation; exception=retain rehabilitation follow-up; notification_policy=archive and routine follow-up only; status=closed.")
    else:
        raise ValueError(f"unsupported virtual stage: {stage}")
    state["events"] = [row for row in state["events"] if row.get("source_event_id") != spec["source_event_id"]]
    state["events"].append({"source_event_id": spec["source_event_id"], "virtual_stage": stage})


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
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


def _write_trajectory(spec: dict[str, Any], rec: Recorder, response: str) -> None:
    trajectory = {"schema_version": "ATIF-v1.7", "session_id": f"oracle-{spec['step']}", "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"}, "steps": [{"step_id": 1, "source": "user", "message": str(spec["source_event_id"])}, {"step_id": 2, "source": "agent", "message": response, "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in rec.calls], "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in rec.calls]}, "llm_call_count": 0}], "final_metrics": {"tool_calls": len(rec.calls), "tool_errors": sum(not row["success"] for row in rec.calls)}}
    LOGS.mkdir(parents=True, exist_ok=True)
    temp = LOGS / ".trajectory.json.tmp"
    temp.write_text(json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(LOGS / "trajectory.json")


async def _run(spec: dict[str, Any]) -> str:
    _validate_spec(spec)
    state = _load_state()
    rec = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"no handler for action kind {kind!r}; known kinds: {known}")
        await ACTION_HANDLERS[kind](rec, state, spec, action)
    _save_state(state)
    response = str(spec["response"])
    _write_trajectory(spec, rec, response)
    (WORKSPACE / "oracle_response.txt").write_text(response + "\n", encoding="utf-8")
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
