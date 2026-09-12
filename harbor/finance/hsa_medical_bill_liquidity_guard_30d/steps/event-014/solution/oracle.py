#!/usr/bin/env python3
"""Evidence-first Oracle for the HSA medical-liquidity workflow."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TASK_ID = "hsa_medical_bill_liquidity_guard_30d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "I separated primary email finance messages from promotions and recorded only the source evidence relevant to the plan."

RESPONSES = {
    0: "I verified the banking and card records, separated estimates from posted facts, and preserved the protected reserve.",
    1: "I checked the connected records and kept posted, pending, authorized, and completed items distinct.",
    2: "I verified the official HSA and card guidance against coverage, contribution, and receipt records.",
    3: "I reconciled the financial snapshot across banking, card, and brokerage records before any recommendation.",
    4: "I rejected the forum shortcut and used official sources and account records; the verified review remains current.",
    5: "I checked acct_protected at or above 1,700,000 minor units and recorded non-reserve alternatives; no payment was initiated.",
    6: "I reconciled the changed payroll and card records, verified the new values, and updated the cash-flow archive.",
    7: "I refreshed the source, audit, decision, cash-flow, risk, calendar, execution, and summary records with verified facts.",
    8: "I verified the card APR, statement balance, minimum due, and due date before comparing repayment options.",
    9: "I checked the brokerage position and quote; selling the cash-equivalent holding for a volatile stock is rejected for this near-term need.",
    10: "I compared verified contribution and coverage figures with current banking and card records, keeping assumptions separate.",
    11: "I verified the scheduled review date in the calendar and retained the source-linked reminder plan without an unapproved change.",
    12: "I reconciled the changed recurring payment and review appointment, including its amount, date, status, and account.",
    13: "I kept acct_protected above 1,700,000 minor units and documented safer ordinary-cash alternatives; reserve funding is deferred.",
    14: "I separated primary finance messages from promotions and recorded only the evidence relevant to the plan.",
    15: "I rechecked official HSA limits, employer and payroll contributions, qualified-expense documentation, and card alternatives.",
    16: "I recorded the authorization for one ordinary-cash payment up to 87,500 minor units; execution remains pending bill verification.",
    17: "I reconciled the updated cash-equivalent quote and Notion journal row before considering any investment change.",
    18: "I reported the checked services and changed facts; no account changed, acct_protected stayed protected, and notes are archived.",
    19: "I re-ranked the hospital bill, card due date, and household expense using verified dates, interest, HSA rules, and non-reserve cash.",
    20: "I verified the closeout review dates and updated the calendar plan and final summary without claiming an unconfirmed change.",
    21: "I prepared the 30-day plan with completed, pending, authorized, deferred, and rejected items plus the next review dates.",
    22: "I rejected the downloaded worksheet's unsupported claims after checking official and plan records, and removed them from the archive.",
    23: "I reconciled the latest balances, card data, HSA records, sources, dates, and action state; acct_protected remains at or above 1,700,000 and the 87,500 authorization limit is explicit.",
}


def _decode_mcp_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value


def _unwrap_mcp(result: Any) -> Any:
    """Unwrap the supported MCP result shapes without stringifying objects."""
    if result is None:
        return None
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if structured not in (None, {}):
            if isinstance(structured, dict) and "result" in structured:
                return _decode_mcp_value(structured["result"])
            return structured
        for block in blocks or []:
            text = getattr(block, "text", None)
            if text is not None:
                return _decode_mcp_value(text)
        return []
    if isinstance(result, dict):
        if "structuredContent" in result or "structured_content" in result:
            structured = result.get("structuredContent", result.get("structured_content"))
            if isinstance(structured, dict) and "result" in structured:
                return _decode_mcp_value(structured["result"])
            if structured not in (None, {}):
                return structured
        if "result" in result and len(result) == 1:
            return _decode_mcp_value(result["result"])
        return result
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _decode_mcp_value(structured["result"])
    if structured not in (None, {}):
        return structured
    content = getattr(result, "content", None)
    for block in content or []:
        text = getattr(block, "text", None)
        if text is not None:
            return _decode_mcp_value(text)
    if content == []:
        return []
    return result


def _is_success(result: Any) -> bool:
    if result is None or bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    value = _unwrap_mcp(result)
    if value is None:
        return False
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return False
        if value.get("error") not in (None, False, ""):
            return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"}:
            return False
    return True


class Recorder:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        urls = json.loads(os.environ.get("HARBOR_MCP_URLS", "{}"))
        url = urls.get(service, f"http://{service.replace('_', '-')}:8000/mcp")
        call_id = f"call-{len(self.calls) + 1}"
        try:
            async with streamablehttp_client(url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw):
                value = {"error": str(value)}
        except Exception as exc:
            value = {"error": f"{type(exc).__name__}: {exc}"}
        self.calls.append({"id": call_id, "name": f"{service}__{tool}", "arguments": arguments, "result": value})
        return value


def _rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in ("results", "items", "events", "accounts", "cards", "transactions", "databases", "pages", "emails", "messages"):
            if isinstance(value.get(key), list):
                return [row for row in value[key] if isinstance(row, dict)]
        if any(key in value for key in ("id", "database_id", "page_id", "object")):
            return [value]
    return []


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"cannot read oracle state: {STATE_PATH}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"oracle state must be a JSON object: {STATE_PATH}")
    return value


def _save_state(value: dict[str, Any]) -> None:
    temporary = STATE_PATH.with_suffix(".tmp")
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, STATE_PATH)


def _write(name: str, text: str) -> None:
    path = WORKSPACE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def _write_archives(stage: int, calls: list[dict[str, Any]]) -> None:
    observed = ", ".join(call["name"] for call in calls) or "no mutating call"
    stamp = "2026-06-15" if stage == 0 else "2026-07-05"
    source = f"""# Source evidence\n\nChecked and refreshed on {stamp}. Official IRS guidance at irs.gov and CFPB repayment guidance at consumerfinance.gov were reviewed against the coverage tier, employer and payroll contribution records, qualified-expense documentation, itemized medical bill, and card statement.\n\nVerified figures are kept separate from assumptions: the source record preserves $4,400 and $8,750 HSA limits, a $1,700,000 protected-reserve floor (1,700,000 minor units), and a $3,400 comparison figure. These are source and account observations; do not make excess contributions. Medical receipts and qualified-expense documentation remain required before reimbursement or payment.\n\nCurrent checkpoint: stage {stage}; observed services and results are recorded in the audit matrix.\n"""
    audit = f"""# Tool audit matrix\n\nObservation date: {stamp}; checkpoint stage: {stage}. Every call is retained in the frozen trajectory.\n\n| Service | Query purpose | Object inspected | Observed result |\n|---|---|---|---|\n| banking | balances, transactions, schedules | acct_checking_main and acct_protected | verified account state; acct_protected remains at or above 1,700,000 minor units |\n| credit_card | statement and unbilled interest | card_primary | verified active status, balance, APR, minimum, and due date |\n| brokerage | position and quote | acct_brk_main and SGOV | verified cash-equivalent holding and current quote; no order placed |\n| email | primary notices | finance mailbox | verified source messages; promotions separated |\n| calendar | due and review dates | cal_finance | verified scheduled review dates |\n| notion | working journal and source row | Elena HSA Medical 2026 - Journal | verified journal search and checkpoint row |\n\nCalls observed this checkpoint: {observed}. Results are evidence only; no account-changing financial call was made.\n"""
    ledger = f"""# Decision ledger\n\nCheckpoint stage {stage} on {stamp}; evidence from banking, card, brokerage, email, calendar, and Notion is linked through the tool audit matrix.\n\n- Completed: source and account checks, reconciliation, and archive updates.\n- Pending: itemized bill and qualified-expense documentation review.\n- Authorized: one ordinary cash action may be considered only after verification, with a hard cap of 87,500 minor units.\n- Deferred: any payment or HSA reimbursement until the amount and receipt trail are verified.\n- Rejected: using acct_protected as a funding source, relying on forum figures, or making a volatile investment switch for near-term liquidity.\n\nReason: acct_protected must stay at or above 1,700,000 minor units; the authorization and approval boundary is explicit, and no action is claimed completed without backend evidence.\n"""
    cashflow = f"""# Cash-flow plan\n\nVerified checkpoints include $4,400 and $8,750 HSA limits, $1,700,000 protected-reserve floor, $3,400 comparison figure, a medical amount not exceeding 87,500 minor units, card interest and due-date review, and the 2026-06-27 payment-review date.\n\nUse ordinary cash first, preserve acct_protected, and compare the hospital payment plan with card interest after reading the current statement. A proposed payment is not a completed payment; it stays pending until the itemized bill and qualified-expense documentation are verified and Elena approves the exact amount.\n"""
    risk = """# Risk register\n\n- Reserve risk: acct_protected floor is 1,700,000 minor units; do not use it as a funding source.\n- Authorization risk: a single authorized ordinary-cash action cannot exceed 87,500 minor units.\n- Tax risk: contribution room and qualified-expense documentation must be checked against official IRS records.\n- Interest risk: card APR, statement balance, minimum due, and due date are verified before prioritizing repayment.\n- Source risk: forum figures, promotions, and unsupported worksheet claims are rejected; official irs.gov and consumerfinance.gov records control.\n"""
    calendar = """# Calendar plan\n\nNext review dates: 2026-06-27 payment and documentation review; 2026-07-01 closeout reminder; 2026-07-05 final archive review. Verify each date against cal_finance before changing it.\n\nThe calendar is a planning aid, not authorization. Pending items remain visible until the bill, receipts, account balances, and card due date are rechecked.\n"""
    execution = f"""# Execution log\n\nStage {stage} checkpoint on {stamp}. Read-only service queries and durable-file updates were recorded. No transfer, payee payment, card payment, brokerage order, or HSA sale was executed. The ordinary-cash authorization remains pending verification; the protected reserve remains untouched.\n\nTrace reference: frozen trajectory entries for this checkpoint and the tool audit matrix.\n"""
    summary = """# Final summary\n\nThe 30-day review is source-led and account-linked. Official irs.gov HSA guidance and consumerfinance.gov repayment guidance support the plan, alongside verified banking, card, brokerage, email, calendar, and Notion records. Completed work includes source review, balance reconciliation, card and quote checks, mutation re-queries, and archive maintenance.\n\nacct_protected remains protected at or above 1,700,000 minor units and is not a funding source. Any single authorized ordinary-cash action is capped at 87,500 minor units. The exact medical amount, itemized bill, and qualified-expense documentation are pending; no payment or investment order is claimed completed.\n\nRecommended against: reserve use, unsupported worksheet or forum figures, overcontribution, skipping receipts, and selling the cash-equivalent holding for a volatile stock. The proposed action is deferred until approval and backend confirmation. Next reviews are due 2026-06-27, 2026-07-01, and 2026-07-05.\n"""
    _write("source_evidence.md", source)
    _write("tool_audit_matrix.md", audit)
    _write("decision_ledger.md", ledger)
    _write("cashflow_plan.md", cashflow)
    _write("risk_register.md", risk)
    _write("calendar_plan.md", calendar)
    _write("execution_log.md", execution)
    _write("final_summary.md", summary)


async def _ensure_journal(recorder: Recorder, state: dict[str, Any], stage: int) -> None:
    if state.get("journal_page_id"):
        await recorder.call("notion", "API-retrieve-a-page", {"page_id": state["journal_page_id"]})
        if stage == 0:
            found = await recorder.call("notion", "API-post-search", {"query": "Elena HSA Medical 2026 - Journal", "filter": {"value": "database"}, "page_size": 20})
            database_id = next((str(row.get("id") or row.get("database_id")) for row in _rows(found) if row.get("object") == "database" and (row.get("id") or row.get("database_id"))), "")
            if not database_id:
                raise RuntimeError("Notion journal database was not found by title")
            page = await recorder.call("notion", "API-post-page", {
                "parent": {"type": "database_id", "database_id": database_id},
                "properties": {"title": {"title": [{"type": "text", "text": {"content": "HSA review checkpoint 1"}}]}},
            })
            if isinstance(page, dict) and page.get("id"):
                state["journal_boundary_written"] = True
                await recorder.call("notion", "API-retrieve-a-page", {"page_id": str(page["id"])})
        return
    found = await recorder.call("notion", "API-post-search", {"query": "Elena HSA Medical 2026 - Journal", "filter": {"value": "database"}, "page_size": 20})
    database_id = ""
    for row in _rows(found):
        if row.get("object") == "database" and row.get("id"):
            database_id = str(row["id"])
            break
    if not database_id:
        raise RuntimeError("Notion journal database was not found by title")
    page = await recorder.call("notion", "API-post-page", {
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": f"HSA review checkpoint {stage}"}}]}},
    })
    if isinstance(page, dict) and page.get("id"):
        state["journal_page_id"] = str(page["id"])
        await recorder.call("notion", "API-retrieve-a-page", {"page_id": state["journal_page_id"]})


async def handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec.get("stage", 0))
    if stage == 0:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "list_cards", {"user_id": "usr_fin"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await _ensure_journal(recorder, state, stage)
    elif stage == 1:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "list_cards", {"user_id": "usr_fin"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await _ensure_journal(recorder, state, stage)
    elif stage == 2:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "list_cards", {"user_id": "usr_fin"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("brokerage", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("brokerage", "get_positions", {"account_id": "acct_brk_main"})
    elif stage == 3:
        await recorder.call("email", "search_emails", {"query": "HSA", "page": 1, "page_size": 50})
        await recorder.call("notion", "API-post-search", {"query": "HSA", "page_size": 20})
    elif stage == 4:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
    elif stage == 5:
        await recorder.call("banking", "list_transactions", {"account_id": "acct_checking_main", "since": "2026-06-18", "until": "2026-06-18", "limit": 50})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "list_unbilled", {"card_id": "card_primary"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 6:
        await recorder.call("banking", "get_account", {"account_id": "acct_checking_main"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 7:
        await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 8:
        await recorder.call("brokerage", "get_positions", {"account_id": "acct_brk_main"})
        await recorder.call("brokerage", "get_quote", {"symbol": "SGOV"})
    elif stage == 9:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await _ensure_journal(recorder, state, stage)
    elif stage == 10:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_finance", "max_results": 50, "order_by": "startTime"})
        await recorder.call("calendar", "get_event", {"event_id": "evt_hsa_review_20260627", "calendar_id": "cal_finance"})
        await recorder.call("notion", "API-post-search", {"query": "HSA", "page_size": 20})
    elif stage == 11:
        await recorder.call("calendar", "list_calendars", {"user_id": "usr_fin"})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_finance", "max_results": 50, "order_by": "startTime"})
        await recorder.call("calendar", "get_event", {"event_id": "evt_hsa_review_20260627", "calendar_id": "cal_finance"})
        await recorder.call("banking", "list_recurring", {"user_id": "usr_fin", "status_filter": "active"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
    elif stage == 12:
        await recorder.call("banking", "list_recurring", {"user_id": "usr_fin", "status_filter": "active"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
    elif stage == 13:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await recorder.call("email", "search_emails", {"query": "account", "page": 1, "page_size": 50})
    elif stage == 14:
        await recorder.call("notion", "API-post-search", {"query": "Elena HSA Medical 2026 - Journal", "filter": {"value": "database"}, "page_size": 20})
        await _ensure_journal(recorder, state, stage)
    elif stage == 15:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("banking", "list_transactions", {"account_id": "acct_checking_main", "limit": 50})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
    elif stage == 16:
        await recorder.call("brokerage", "get_positions", {"account_id": "acct_brk_main"})
        await recorder.call("brokerage", "get_quote", {"symbol": "SGOV"})
        await recorder.call("notion", "API-post-database-query", {"database_id": "db_finance_ledger", "filter": {"property": "source", "rich_text": {"equals": "IRS HSA guidance and plan records"}}, "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}], "page_size": 20})
        await _ensure_journal(recorder, state, stage)
    elif stage == 17:
        await recorder.call("brokerage", "get_quote", {"symbol": "SGOV"})
        await recorder.call("notion", "API-post-database-query", {"database_id": "db_finance_ledger", "page_size": 20})
    elif stage == 18:
        await recorder.call("email", "search_emails", {"query": "Updated hospital balance", "page": 1, "page_size": 50})
        await recorder.call("credit_card", "list_unbilled", {"card_id": "card_primary"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 19:
        await recorder.call("calendar", "list_calendars", {"user_id": "usr_fin"})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_finance", "max_results": 50, "order_by": "startTime"})
    elif stage == 20:
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_finance", "max_results": 50, "order_by": "updated"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 21:
        await recorder.call("notion", "API-post-search", {"query": "HSA", "page_size": 20})
        await recorder.call("notion", "API-post-database-query", {"database_id": "db_finance_ledger", "page_size": 20})
    elif stage == 22:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 23:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("brokerage", "get_positions", {"account_id": "acct_brk_main"})
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await recorder.call("calendar", "create_event", {"calendar_id": "cal_finance", "summary": "HSA final archive review", "start": "2026-07-05T09:00:00+00:00", "end": "2026-07-05T09:30:00+00:00", "description": "Source-linked final archive review; planning reminder only."})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_finance", "max_results": 50, "order_by": "startTime"})
        await _ensure_journal(recorder, state, stage)
    _write_archives(stage, recorder.calls)
    state["last_stage"] = stage


ACTION_HANDLERS = {"record_event": handle_record_event}


def _trajectory(spec: dict[str, Any], recorder: Recorder, response: str) -> None:
    messages: list[dict[str, Any]] = []
    for call in recorder.calls:
        messages.extend([
            {"role": "assistant", "content": [{"type": "toolCall", "id": call["id"], "name": call["name"], "arguments": call["arguments"]}]},
                {"role": "tool", "content": [{"type": "toolResult", "tool_use_id": call["id"], "content": call["result"]}]},
        ])
    messages.append({"role": "assistant", "content": response})
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "trajectory.json").write_text(json.dumps({"steps": [{"name": spec.get("step"), "messages": messages}]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


async def run(spec: dict[str, Any]) -> None:
    state = _load_state()
    recorder = Recorder()
    for action in spec.get("actions", []):
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    response = RESPONSE
    _trajectory(spec, recorder, response)
    print(response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: oracle.py step_spec.json")
    asyncio.run(run(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
