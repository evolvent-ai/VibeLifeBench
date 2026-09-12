#!/usr/bin/env python3
"""Harbor Oracle for the disability-leave income-gap bridge."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "disability_leave_income_gap_guard_30d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The disability-leave bridge step was reviewed with live evidence and recorded in the durable plan."

SERVICE_URLS = {
    "banking": "http://banking:8000/mcp",
    "brokerage": "http://brokerage:8000/mcp",
    "calendar": "http://calendar:8000/mcp",
    "credit_card": "http://credit-card:8000/mcp",
    "email": "http://email:8000/mcp",
    "notion": "http://notion:8000/mcp",
}

FIRST_REQUIRED_STAGE = {
    "account_snapshot.md": 1,
    "cash_bridge.md": 1,
    "reserve_guard.md": 1,
    "benefit_timeline.md": 2,
    "leave_evidence.md": 3,
    "calendar_plan.md": 12,
    "execution_log.md": 13,
    "final_summary.md": 20,
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
    """Normalize MCP result shapes; an empty list is a successful empty read."""
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
        if str(value.get("status") or "").lower() in {"error", "failed", "failure", "rejected", "declined"}:
            return False
        if value.get("ok") is False:
            return False
    if isinstance(value, list):
        return all(_is_success(item) for item in value) if value else True
    return value is not None


class Recorder:
    """Call MCP services and retain the exact ATIF audit trail."""

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


def _rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [dict(row) for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in ("items", "results", "emails", "events", "accounts", "cards"):
            candidate = value.get(key)
            if isinstance(candidate, list):
                return [dict(row) for row in candidate if isinstance(row, dict)]
    return []


def _doc_text(state: dict[str, Any], stage: int) -> dict[str, str]:
    """Render only facts available at this virtual stage."""
    if stage < 0 or stage > 23:
        raise ValueError(f"unsupported document stage: {stage}")

    payment_id = str(state.get("vars", {}).get("payment_id") or "")
    checking_minor = 2_898_000 if stage >= 15 else 2_772_000 if stage >= 9 else 2_626_000
    statement_minor = 309_169 if stage >= 21 else 306_569 if stage >= 13 else 354_569
    unbilled_minor = 139_800 if stage >= 17 else 147_000
    available_minor = (
        1_051_031 if stage >= 21 else 1_053_631 if stage >= 17 else 1_046_431 if stage >= 13 else 998_431
    )

    docs: dict[str, str] = {}
    if stage >= FIRST_REQUIRED_STAGE["account_snapshot.md"]:
        account = [f"""# Account Snapshot
## Cash accounts
- Available cash: everyday checking `acct_checking_main`, current backend balance ${checking_minor / 100:,.2f} ({checking_minor:,} minor units); operating buffer remains separate.
- Protected account: Medical Reserve Bucket `acct_protected`, $13,250.00 (1,325,000 minor units), held above the minimum.
## Card position
- `card_primary` card statement balance is ${statement_minor / 100:,.2f} ({statement_minor:,} minor), unbilled balance is ${unbilled_minor / 100:,.2f} ({unbilled_minor:,} minor), and available credit is ${available_minor / 100:,.2f} ({available_minor:,} minor).
- Minimum payment due is $88.64 (8,864 minor); due date is 2026-08-21.
## Backend checked at
- Live banking and credit-card evidence objects were refreshed for the current review stage.
## Evidence objects
- Account ids: `acct_checking_main`, `acct_protected`; card id: `card_primary`."""]
        if stage >= 6:
            account.append("The minimum due and interest-reducing options are separate; no payment was authorized or scheduled at this stage.")
        if stage >= 9:
            account.append("The $1,460.00 (146,000 minor) payroll adjustment is posted in checking and included in available cash.")
        if stage >= 13:
            account.append(f"The authorized $480.00 payment is linked to backend payment identifier `{payment_id}`.")
        if stage >= 14:
            account.append("The payment result, posted status, new card balance, and reconciliation status were verified from backend objects.")
        if stage >= 17:
            account.append("The $72.00 (7,200 minor) pharmacy refund is reflected in the remaining card exposure.")
        if stage >= 21:
            account.append("The $26.00 (2,600 minor) periodic interest line is reflected in the current card position.")
        docs["account_snapshot.md"] = "\n".join(account)

        cash = [f"""# Cash Bridge
## Available cash
- Checking balance is ${checking_minor / 100:,.2f} ({checking_minor:,} minor); the Medical Reserve Bucket is protected and excluded from bridge cash.
## Operating buffer
- Bill timing and the operating buffer remain separate from protected funds."""]
        if stage >= 4:
            cash.append("## Pending income\n- Claim 8472 has a conditional $840.00 weekly estimate and earliest possible 2026-08-12 payment date; it is not available cash.")
        if stage >= 5:
            cash.append("## Reserve boundary\n- Prohibited uses include the Medical Reserve; safer alternatives use checking, bill timing, and the operating buffer.")
        if stage >= 6:
            cash.append("## Card due\n- The $88.64 minimum payment, statement balance, interest exposure, and 2026-08-21 due date are separate; payment remains not authorized and must not be scheduled.")
        if stage >= 7:
            cash.append("## Claim delay\n- A documentation delay keeps claim 8472 pending income unavailable; the next step is follow-up on the missing clinic note.")
        if stage >= 8:
            cash.append("## Deferred options\n- Brokerage sales are deferred, checking is preferred, and protected funds remain prohibited.")
        if stage >= 9:
            cash.append("## Payroll adjustment\n- The backend-posted $1,460.00 (146,000 minor) payroll adjustment is included in the checking balance and thirty-day outlook.")
        if stage >= 10:
            cash.append("## Two-week reforecast\n- The next two weeks and fourteen-day view include posted payroll, the pending claim, and the card due date.")
        if stage >= 11:
            cash.append("## Scheduled outflows\n- The clinic invoice is pending for $286.00 (28,600 minor) on 2026-08-18.")
        if stage >= 13:
            cash.append(f"## Authorized amounts\n- Exactly one $480.00 (48,000 minor) payment from `acct_checking_main` to `card_primary` was authorized; backend object `{payment_id}` was returned.")
        if stage >= 15:
            cash.append("## Posted benefit\n- The actual posted net benefit is $1,260.00 (126,000 minor); the earlier $840.00 amount remains an estimate.")
        if stage >= 17:
            cash.append("## Card refund\n- A $72.00 (7,200 minor) pharmacy refund reduced card exposure.")
        if stage >= 19:
            cash.append("## Claim review\n- The next review is 2026-08-25; no second payment is approved and pending income remains unavailable.")
        if stage >= 21:
            cash.append("## Interest\n- A $26.00 (2,600 minor) periodic interest charge is recorded; there is no new payment authorization.")
        docs["cash_bridge.md"] = "\n".join(cash)

        reserve = ["""# Reserve Guard
## Protected account
- Medical Reserve Bucket is `acct_protected`; protected funds are $13,250.00 (1,325,000 minor).
## Minimum balance
- Required minimum balance is $13,250.00.
## Latest verification
- Banking evidence confirms the protected account is at the floor with no debit."""]
        if stage >= 5:
            reserve.append("## Prohibited uses\n- Do not use the protected account for rent, card payments, or the income-gap bridge.\n## Safer alternatives\n- Prefer everyday checking, the operating buffer, and bill timing.")
        if stage >= 8:
            reserve.append("Brokerage remains deferred rather than substituting for protected funds.")
        if stage >= 11:
            reserve.append("The $286.00 clinic invoice is a scheduled checking outflow, not a reserve debit.")
        if stage >= 13:
            reserve.append("The authorized $480.00 card payment uses `acct_checking_main`; `acct_protected` remains untouched.")
        if stage >= 18:
            reserve.append("A possible leave extension is a pending risk; it is not approved, and clinician follow-up is the next step.")
        docs["reserve_guard.md"] = "\n".join(reserve)

    if stage >= FIRST_REQUIRED_STAGE["benefit_timeline.md"]:
        benefit = ["""# Benefit Timeline
## Leave dates
- Approved leave is 2026-08-03 through 2026-08-28.
## Waiting period
- The first five workdays are unpaid before the separate payroll handoff.
## Claim documents
- The Northstar leave approval is recorded."""]
        if stage >= 4:
            benefit.append("## Benefit estimates\n- Claim 8472 has a conditional gross weekly estimate of $840.00 (84,000 minor) and an earliest possible first payment date of 2026-08-12; approval is pending.")
        if stage >= 7:
            benefit.append("## Documentation delay\n- A missing clinic note makes the earlier estimate unreliable; pending income is not available cash and follow-up is the next step.")
        if stage >= 15:
            benefit.append("## Posted benefits\n- The actual net deposit is $1,260.00 (126,000 minor), distinct from the earlier gross estimate. Tax-treatment status remains unresolved.")
        if stage >= 16:
            benefit.append("## Pending determinations\n- Posted net benefits and benefit estimates remain separate in the thirty-day outlook.")
        if stage >= 18:
            benefit.append("A leave extension is only a risk and possibility, not approved; clinician review is the next step.")
        if stage >= 19:
            benefit.append("The next claim review is 2026-08-25. No second payment or leave extension is approved; pending income remains unavailable.")
        docs["benefit_timeline.md"] = "\n".join(benefit)

    if stage >= FIRST_REQUIRED_STAGE["leave_evidence.md"]:
        leave = ["""# Leave Evidence
## Source review
- Official IRS source review covers Publication 525 disability payments and Publication 15-A sick-pay guidance; CFPB card-minimum guidance is retained as general source evidence.
## Claim documents
- Northstar leave approval covers 2026-08-03 through 2026-08-28.
## Tax-treatment status
- Tax treatment is unresolved and conditional on plan funding and payer details; no personalized tax conclusion is asserted.
## Source lineage
- Source records are `us_irs_pub525_2025_disability`, `us_irs_pub15a_2026_sick_pay`, and `us_cfpb_credit_minimum`."""]
        if stage >= 4:
            leave.append("Harbor Benefits claim 8472 was received with medical certification still pending.")
        if stage >= 7:
            leave.append("Claim 8472 has a documented clinic-note delay.")
        if stage >= 15:
            leave.append("The posted $1,260.00 net deposit does not resolve the payer-dependent tax treatment.")
        if stage >= 19:
            leave.append("The claim schedule now records the 2026-08-25 review and no approved extension.")
        docs["leave_evidence.md"] = "\n".join(leave)

    if stage >= FIRST_REQUIRED_STAGE["calendar_plan.md"]:
        calendar = ["""# Calendar Plan
## Claim follow-up
- A claim follow-up reminder is present; its date remains subject to the administrator's next review notice.
## Payment dates
- Card payment review and due date: 2026-08-21.
## Medical dates
- Clinic invoice review: 2026-08-18.
## Cash reviews
- The next cash review is 2026-08-14.
## Duplicate check
- One reminder exists for each claim, card, clinic, and cash-review group; no duplicate business reminders were created."""]
        if stage >= 19:
            calendar.append("The claim follow-up/review is now dated 2026-08-25, with no second payment approved.")
        docs["calendar_plan.md"] = "\n".join(calendar)

    if stage >= FIRST_REQUIRED_STAGE["execution_log.md"]:
        execution = [f"""# Execution Log
## Authorization received
- Priya Singh authorized one $480.00 payment from `acct_checking_main` to `card_primary` on 2026-08-11.
## Tool result
- Credit-card `make_payment` returned a successful result retained in the trace.
## Backend object
- Payment identifier: `{payment_id}`; the backend object is linked to the archived result.
## Amount and source
- Amount is $480.00 (48,000 minor); source is `acct_checking_main`, target is `card_primary`."""]
        if stage >= 14:
            execution.append("## Reconciliation status\n- Posted status, payment result, new card balance, and new outstanding amount were verified from a follow-up backend read.")
        if stage >= 17:
            execution.append("The $72.00 (7,200 minor) pharmacy refund was backend verified separately from the payment.")
        if stage >= 21:
            execution.append("The $26.00 (2,600 minor) periodic interest was reconciled; no new authorization was given.")
        docs["execution_log.md"] = "\n".join(execution)

    if stage >= FIRST_REQUIRED_STAGE["final_summary.md"]:
        final = [f"""# Final Summary
## Verified facts
- Leave is approved for 2026-08-03 through 2026-08-28 with five unpaid workdays; actual deposits are the $1,460.00 payroll adjustment and $1,260.00 net benefit.
- Current checking is $28,980.00; the $72.00 pharmacy refund is reflected in card exposure; protected funds are $13,250.00.
## Executed actions
- The actual payment was one authorized $480.00 (48,000 minor) transfer from `acct_checking_main` to `card_primary`, linked to payment identifier `{payment_id}`.
## Pending items
- Clinic invoice $286.00 (28,600 minor) due 2026-08-18 and claim determination remain pending; no second payment is available.
## Deferred choices
- Tax treatment remains unresolved; brokerage sales and reserve use were deferred.
## Protected funds
- Medical Reserve Bucket stayed at or above $13,250.00 (1,325,000 minor) with no unauthorized debit.
## Next dated actions
- Review clinic payment on 2026-08-18, card due date on 2026-08-21, and claim follow-up on 2026-08-25.
## Evidence links
- Banking, credit-card, email, calendar, Notion source, and brokerage reads are linked to backend objects in the trace."""]
        if stage >= 21:
            final.append("A $26.00 (2,600 minor) periodic interest charge is included in the verified final card position of $3,091.69 (309,169 minor), with $1,398.00 (139,800 minor) unbilled and $10,510.31 (1,051,031 minor) available credit.")
        docs["final_summary.md"] = "\n".join(final)

    return docs


def _write_docs(state: dict[str, Any], stage: int) -> None:
    for name, text in _doc_text(state, stage).items():
        _atomic_write(WORKSPACE / name, text.rstrip() + "\n")


async def _ensure_calendar(recorder: Recorder) -> None:
    existing = await recorder.call("calendar", "list_events", {
        "time_min": "2026-08-17T00:00:00-07:00",
        "time_max": "2026-08-26T23:59:59-07:00",
        "calendar_id": "cal_finance",
        "max_results": 100,
    })
    blob = json.dumps(_rows(existing), ensure_ascii=False).casefold()
    reminders = [
        ("Claim follow-up review", "2026-08-25T09:00:00-07:00", "2026-08-25T09:30:00-07:00", "Claim 8472 follow-up and pending determination review."),
        ("Card payment due date", "2026-08-21T09:00:00-07:00", "2026-08-21T09:30:00-07:00", "Review card payment due date and minimum due."),
        ("Medical clinic invoice", "2026-08-18T09:00:00-07:00", "2026-08-18T09:30:00-07:00", "Review pending clinic invoice and scheduled outflows."),
        ("Cash bridge review", "2026-08-24T09:00:00-07:00", "2026-08-24T09:30:00-07:00", "Review available cash, pending income, and protected funds."),
    ]
    for summary, start, end, description in reminders:
        terms = [summary.split()[0].casefold()]
        if "claim" in summary.casefold():
            terms.append("follow-up")
        elif "card" in summary.casefold():
            terms.append("due")
        elif "medical" in summary.casefold():
            terms.append("clinic")
        else:
            terms.append("cash")
        if all(term in blob for term in terms):
            continue
        await recorder.call("calendar", "create_event", {
            "summary": summary,
            "start": start,
            "end": end,
            "description": description,
            "calendar_id": "cal_finance",
            "reminders": [{"method": "popup", "minutes_before": 30}],
        })


async def _handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or action.get("event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])
    # Every stage collects the newest backend evidence required by its rubric.
    if stage == 0:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("credit_card", "list_cards", {"user_id": "usr_fin"})
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 100})
        await recorder.call("calendar", "list_events", {"time_min": "2026-07-29T00:00:00-07:00", "time_max": "2026-07-30T23:59:59-07:00", "calendar_id": "cal_finance", "max_results": 100})
    elif stage == 1:
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("banking", "get_account", {"account_id": "acct_checking_main"})
        await recorder.call("credit_card", "list_cards", {"user_id": "usr_fin"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
    elif stage in (2, 4, 7, 18, 19):
        query = {2: "leave approval", 4: "claim 8472", 7: "claim delay", 18: "extension", 19: "claim schedule"}[stage]
        result = await recorder.call("email", "search_emails", {"query": query, "folder": "INBOX", "page": 1, "page_size": 100})
        for row in _rows(result)[:2]:
            email_id = row.get("email_id") or row.get("id")
            if email_id:
                await recorder.call("email", "read_email", {"email_id": str(email_id)})
        if stage == 19:
            await recorder.call("calendar", "list_events", {"time_min": "2026-08-24T00:00:00-07:00", "time_max": "2026-08-26T23:59:59-07:00", "calendar_id": "cal_finance", "max_results": 100})
    elif stage == 3:
        await recorder.call("notion", "API-post-search", {"query": "IRS", "filter": {"value": "page"}, "page_size": 100})
    elif stage == 5:
        await recorder.call("banking", "get_account", {"account_id": "acct_protected"})
        await recorder.call("banking", "list_accounts", {"user_id": "usr_fin"})
    elif stage == 6:
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
        await recorder.call("credit_card", "get_statement", {"statement_id": "stmt_y_2025_12"})
        await recorder.call("credit_card", "list_unbilled", {"card_id": "card_primary"})
    elif stage == 8:
        await recorder.call("brokerage", "list_accounts", {"user_id": "usr_fin"})
        await recorder.call("brokerage", "get_portfolio", {"account_id": "acct_brk_main"})
        await recorder.call("brokerage", "get_positions", {"account_id": "acct_brk_main"})
    elif stage in (9, 10, 15, 16, 20, 22, 23):
        await recorder.call("banking", "get_account", {"account_id": "acct_checking_main"})
        await recorder.call("banking", "list_transactions", {"account_id": "acct_checking_main", "since": "2026-07-30", "limit": 500})
        if stage in (10, 20, 22, 23):
            await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
            await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
        if stage in (22,):
            await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 100})
            await recorder.call("calendar", "list_events", {"time_min": "2026-07-30T00:00:00-07:00", "time_max": "2026-08-29T23:59:59-07:00", "calendar_id": "cal_finance", "max_results": 100})
    elif stage == 11:
        await recorder.call("banking", "list_pending_payments", {"user_id": "usr_fin", "account_id": "acct_checking_main", "status_filter": "pending", "limit": 100})
        await recorder.call("banking", "get_account", {"account_id": "acct_checking_main"})
    elif stage == 12:
        await _ensure_calendar(recorder)
    elif stage == 13:
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        if not state.get("vars", {}).get("payment_id"):
            payment = await recorder.call("credit_card", "make_payment", {"card_id": "card_primary", "amount_minor": 48000, "source_hint": "acct_checking_main"})
            if not isinstance(payment, dict) or not payment.get("payment_id"):
                raise RuntimeError("authorized payment returned no payment identifier")
            state["vars"]["payment_id"] = str(payment["payment_id"])
    elif stage == 14:
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
    elif stage == 17:
        await recorder.call("credit_card", "list_unbilled", {"card_id": "card_primary"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
    elif stage == 21:
        await recorder.call("credit_card", "get_statement", {"statement_id": "stmt_y_2025_12"})
        await recorder.call("credit_card", "get_card", {"card_id": "card_primary"})
        await recorder.call("credit_card", "list_statements", {"card_id": "card_primary", "limit": 12})
    else:
        raise ValueError(f"unsupported stage: {stage}")
    _write_docs(state, stage)
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
    if not isinstance(spec["expected_env"], dict):
        raise ValueError("expected_env must be an object")
    for key in ("preceding_releases", "released_mutations"):
        if not isinstance(spec["expected_env"].get(key), list):
            raise ValueError(f"expected_env.{key} must be a list")
    for env_name, expected in (("HARBOR_STEP_NAME", spec["step"]), ("HARBOR_EVENT_ID", spec["source_event_id"]), ("SOURCE_EVENT_ID", spec["source_event_id"]), ("HARBOR_VIRTUAL_STAGE", str(spec["virtual_stage"])), ("VIRTUAL_STAGE", str(spec["virtual_stage"]))):
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
            {"step_id": 2, "source": "agent", "message": response,
             "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in recorder.calls],
             "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in recorder.calls]},
             "llm_call_count": 0},
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
        kind = str(action.get("kind") or "")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    _save_state(state)
    _write_trajectory(spec, recorder, response)
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
