#!/usr/bin/env python3
"""Executable reference Oracle for the divorce asset-rebuild task."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

TASK_ID = "divorce_asset_rebuild_30d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
USER_ID = "usr_zhou_nan"
CHECKING_ACCOUNT_ID = "acct_checking_main"
PROTECTED_ACCOUNT_ID = "acct_medical_reserve"
CALENDAR_ID = "cal_finance"


def _decode_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _unwrap_mcp(result: Any) -> Any:
    """Decode all MCP SDK result shapes; an empty list is a successful read."""
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _decode_json(structured["result"])
        if structured not in (None, {}):
            return structured
        for block in blocks or []:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is not None:
                return _decode_json(text)
        return []
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _decode_json(structured["result"])
    if structured not in (None, {}):
        return structured
    content = getattr(result, "content", None)
    for block in content or []:
        if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
            raise RuntimeError("MCP content block has isError=true")
        text = getattr(block, "text", None)
        if text is not None:
            return _decode_json(text)
    if content == []:
        return []
    if isinstance(result, (dict, list)):
        return result
    return result


def _is_success(value: Any) -> bool:
    """Recognize only structurally successful mock responses."""
    if isinstance(value, list):
        return all(_is_success(item) for item in value)
    if not isinstance(value, dict):
        return value is not None
    if value.get("isError") is True or value.get("is_error") is True:
        return False
    if value.get("success") is False or value.get("ok") is False:
        return False
    if value.get("error") not in (None, False, ""):
        return False
    if str(value.get("status") or "").casefold() in {"error", "failed", "failure"}:
        return False
    code = str(value.get("code") or "").upper()
    return not code.startswith(("BAD_", "NOT_", "ERR", "FAIL", "INVALID_", "DENIED", "INTERNAL"))


class Recorder:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        from mcp import ClientSession
        from mcp.client.streamable_http import streamablehttp_client

        call_id = f"oracle-{len(self.calls) + 1:03d}"
        host = service.replace("_", "-")
        try:
            async with streamablehttp_client(f"http://{host}:8000/mcp") as streams:
                read, write = streams[0], streams[1]
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    value = _unwrap_mcp(await session.call_tool(tool, arguments))
            success = _is_success(value)
            error = None if success else str(value)
        except Exception as exc:
            value = {"error": f"{type(exc).__name__}: {exc}"}
            success = False
            error = value["error"]
        self.calls.append(
            {
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": value,
                "success": success,
                "error": error,
            }
        )
        if not success:
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}")
        return value

    def workspace_write(self, path: str, text: str) -> None:
        target = WORKSPACE / Path(path).name
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        block = text.rstrip() + "\n"
        if block.strip() not in old:
            target.write_text((old.rstrip() + "\n\n" + block).lstrip(), encoding="utf-8")
        self.calls.append(
            {
                "tool_call_id": f"oracle-{len(self.calls) + 1:03d}",
                "function_name": "workspace__append_file",
                "arguments": {"path": path, "text": text},
                "result": {"ok": True, "path": path},
                "success": True,
                "error": None,
            }
        )


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"events": [], "vars": {}}
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"unreadable Oracle state: {STATE_PATH}") from exc
    if not isinstance(value, dict):
        raise RuntimeError("Oracle state must be a JSON object")
    if not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("Oracle state must contain events and vars collections")
    return value


def _save_state(state: dict[str, Any]) -> None:
    clean = {"events": state.get("events", []), "vars": state.get("vars", {})}
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
    temporary.write_text(
        json.dumps(clean, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(STATE_PATH)


def _rows(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in keys:
            rows = value.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


async def _read_email(rec: Recorder, query: str) -> Any:
    result = await rec.call(
        "email",
        "search_emails",
        {"query": query, "folder": "INBOX", "page": 1, "page_size": 50},
    )
    rows = _rows(result, "emails", "items", "results")
    if not rows:
        raise RuntimeError(f"email evidence not found for query: {query}")
    email_id = rows[0].get("email_id") or rows[0].get("id")
    if email_id is None:
        raise RuntimeError(f"email search returned no readable id for query: {query}")
    return await rec.call("email", "read_email", {"email_id": str(email_id)})


async def _read_cards(rec: Recorder, include_unbilled: bool = False) -> None:
    await rec.call("credit_card", "list_cards", {"user_id": USER_ID})
    for card_id in ("card_cmb_family", "card_boc_parents"):
        await rec.call("credit_card", "get_card", {"card_id": card_id})
        await rec.call(
            "credit_card",
            "list_statements",
            {"card_id": card_id, "limit": 12, "page": 1},
        )
        if include_unbilled:
            await rec.call("credit_card", "list_unbilled", {"card_id": card_id})


async def _ensure_lpr_anchor(rec: Recorder) -> None:
    result = await rec.call(
        "notion",
        "API-post-database-query",
        {"database_id": "db_finance_ledger", "page_size": 100},
    )
    exact = "not a personal mortgage execution rate"
    if any(
        "public_rate_anchor" in json.dumps(row, ensure_ascii=False)
        and exact in json.dumps(row, ensure_ascii=False).casefold()
        for row in _rows(result, "results", "items")
    ):
        return
    await rec.call(
        "notion",
        "API-post-page",
        {
            "parent": {"type": "database_id", "database_id": "db_finance_ledger"},
            "properties": {
                "record_type": "public_rate_anchor",
                "date": "2026-07-20",
                "status": "verified",
                "source": "China Foreign Exchange Trade System",
                "one_year_lpr": "3.0%",
                "over_five_year_lpr": "3.5%",
                "scope": "Not a personal mortgage execution rate",
            },
        },
    )


CALENDAR_REMINDERS = (
    (
        "Daughter Medical policy renewal",
        "2026-08-16T09:00:00+08:00",
        "2026-08-16T09:30:00+08:00",
        "Divorce asset rebuilding reminder: medical policy renewal and payment-account review.",
    ),
    (
        "Critical-illness policy renewal",
        "2026-08-22T09:00:00+08:00",
        "2026-08-22T09:30:00+08:00",
        "Divorce asset rebuilding reminder: critical-illness policy premium and relationship-change status.",
    ),
    (
        "School Payment window review",
        "2026-08-17T09:00:00+08:00",
        "2026-08-17T09:30:00+08:00",
        "Divorce asset rebuilding reminder: School expenses are payable August 17-21.",
    ),
    (
        "Mortgage Debit and application review",
        "2026-08-19T09:00:00+08:00",
        "2026-08-19T09:30:00+08:00",
        "Divorce asset rebuilding reminder: Mortgage payment, Debit status and prepayment authorization check.",
    ),
    (
        "Child support monthly Review",
        "2026-08-28T09:00:00+08:00",
        "2026-08-28T09:30:00+08:00",
        "Divorce asset rebuilding reminder: Child support posting and delay-history Review.",
    ),
    (
        "Personal Pension annual Review",
        "2026-11-01T09:00:00+08:00",
        "2026-11-01T09:30:00+08:00",
        "Divorce asset rebuilding reminder: Pension liquidity and tax-policy Review.",
    ),
    (
        "30-day Summary Review",
        "2026-08-28T16:30:00+08:00",
        "2026-08-28T17:00:00+08:00",
        "Divorce asset rebuilding reminder: Thirty-day Summary closeout Review.",
    ),
)


async def _ensure_calendar(rec: Recorder) -> None:
    result = await rec.call(
        "calendar",
        "list_events",
        {
            "calendar_id": CALENDAR_ID,
            "time_min": "2026-07-30T00:00:00+08:00",
            "time_max": "2026-12-31T23:59:59+08:00",
            "max_results": 500,
            "page": 1,
        },
    )
    existing = "\n".join(
        f"{row.get('summary', '')}\n{row.get('description', '')}"
        for row in _rows(result, "items", "events", "results")
    ).casefold()
    for summary, start, end, description in CALENDAR_REMINDERS:
        if description.casefold() in existing:
            continue
        await rec.call(
            "calendar",
            "create_event",
            {
                "calendar_id": CALENDAR_ID,
                "summary": summary,
                "start": start,
                "end": end,
                "description": description,
                "location": "Personal finance calendar",
                "reminders": [{"method": "popup", "minutes_before": 1440}],
            },
        )


RESPONSES = {
    0: "Opened the 30-day asset-rebuilding record and verified the live banking, card, email and calendar services before using any amount.",
    1: "Built the asset, debt and cash-status inventory with received money, receivables, restricted reserves, emergency cash and both card statements kept separate.",
    2: "Kept the RMB 8,000 July child support as an unreceived receivable and preserved the expected date without treating it as cash.",
    3: "Verified both current card statements, unbilled charges, minimum payments, due dates and APRs without making a payment.",
    4: "Recorded the public LPR as a comparison anchor and kept it separate from the mortgage contract rate and execution terms.",
    5: "Reconciled the mortgage estimate: RMB 1,260,000 principal, 4.10% contract rate, RMB 50,000 minimum prepayment and separate joint-borrower responsibility.",
    6: "Compared a RMB 120,000 prepayment with a six-month cash buffer and clearing cards first; no mortgage prepayment was authorized or executed.",
    7: "Reviewed both policy records, premium timing, payment accounts and the still-incomplete policyholder or beneficiary change.",
    8: "Updated the RMB 7,200 and RMB 9,600 policy lanes for August 16 and 22 while leaving the relationship change unsubmitted.",
    9: "Recorded the education-fund idea as an irreversible option and confirmed the existing RMB 50,000 daughter reserve remains protected.",
    10: "Replaced the school estimate with the official RMB 18,600 August 17-21 payment window and left it unpaid.",
    11: "Completed a conservative 30-day cash-flow view that separates received cash, receivables, bills, reserves and the no-prepayment mortgage lane.",
    12: "Verified the RMB 8,000 child-support posting, changed it to received and retained the earlier delay as history.",
    13: "Executed exactly the two authorized card payments, RMB 31,800 and RMB 12,800 from acct_checking_main, with no other payment or transfer.",
    14: "Verified both payment objects and reconciled their separately applied amounts and current balances in the backend.",
    15: "Refreshed the CMB card after the RMB 486 revolving-interest adjustment and preserved the new balance as the current fact.",
    16: "Created the seven non-duplicated policy, school, mortgage, support, pension and 30-day review reminders.",
    17: "Recorded the RMB 12,000 pension deduction ceiling and 3% withdrawal tax treatment without contributing or placing an investment order.",
    18: "Recorded the August 19-21 mortgage application window and kept both prepayment and joint-liability changes unexecuted.",
    19: "Compared RMB 50,000 now, year-end reassessment and no prepayment against liquidity needs; the mortgage remains unchanged.",
    20: "Marked the daughter's medical policy renewed while the critical-illness premium and relationship change remain pending.",
    21: "Completed the 30-day backend-consistent summary of receipts, card payments, reserves, insurance, mortgage, pension and next review.",
    22: "Archived a concise closeout separating completed authorization, deferred decisions, prohibited funds and next-month checks.",
}


WORKSPACE_UPDATES: dict[int, tuple[tuple[str, str], ...]] = {
    1: (
        (
            "asset_inventory.md",
            """# Asset Inventory
Backend verification time: 2026-07-30 14:00 +08:00. Evidence objects: banking accounts, brokerage positions and credit-card statements.
- Received funds: RMB 180,000 divorce property-settlement transition payment; acct_checking_main balance RMB 228,000.
- Receivables: Child support receivable RMB 8,000; not current cash until actual posting.
- Living emergency fund: RMB 120,000, separate from future estimates.
- Daughter's education and medical reserve: RMB 50,000 in frozen acct_medical_reserve; restricted and not spendable.
- Pension and investments: acct_pension RMB 0; acct_brk_liang positions are tracked separately.
- Two card statements: card_cmb_family RMB 31,800 and card_boc_parents RMB 12,800; unbilled RMB 5,000 and RMB 1,200.""",
        ),
        (
            "debt_plan.md",
            """# Debt Plan
Two card statements are separate Backend evidence objects.
- card_cmb_family: statement RMB 31,800; Minimum payments RMB 3,180; Unbilled RMB 5,000; Due date 2026-08-12; Interest rate 18.25% APR.
- card_boc_parents: statement RMB 12,800; Minimum payments RMB 1,280; Unbilled RMB 1,200; Due date 2026-08-13; Interest rate 19.90% APR.
- Unauthorized: do not pay yet, do not prepay the Mortgage, and do not use the protected reserve.""",
        ),
        (
            "support_cashflow.md",
            """# Support Cashflow
- Child support receivable: RMB 8,000 expected but Not received; it is excluded from current cash.
- Received transition funds, Receivable support, rigid expenses and restricted reserves remain separate.
- Thirty-day cash buffer starts with verified backend balances, not estimates.""",
        ),
    ),
    2: (
        (
            "support_cashflow.md",
            """## 2026-07-31 Child Support Delay
Family Email says RMB 8,000 was Not received and has not been transferred. Preserve the Delay and expected August 5 date; Cannot count it as cash before Actual posting.""",
        ),
        (
            "asset_inventory.md",
            """## Receivable Update
Child support receivable RMB 8,000 remains Expected and Not received; do not count it as current cash.""",
        ),
    ),
    3: (
        (
            "debt_plan.md",
            """## Card Source Review
Two card statements were read with statement balances, Minimum payments, Unbilled charges, Due date and Interest rate. Minimum payment is only the delinquency floor. Payment remains Unauthorized; Do not pay yet.""",
        ),
    ),
    4: (
        (
            "source_evidence.md",
            """# Source Evidence
- Public LPR anchor: China Foreign Exchange Trade System announcement dated 2026-07-20; one-year LPR 3.0% and over-five-year LPR 3.5%.
- Scope: this is a comparison benchmark and Cannot replace a personal Mortgage contract execution rate.
- Child support basis: RMB 8,000 is recognized only upon bank posting.
- Personal pension tax policy: annual RMB 12,000 deduction limit and 3% separate withdrawal tax; actual contribution remains independent.
- Source lineage: Notion public-rate row, bank accounts, card statements and released email notices.""",
        ),
        (
            "debt_plan.md",
            """## Rate Comparison Boundary
Public LPR anchor is 3.0% / 3.5% from the China Foreign Exchange Trade System. Mortgage contract facts and Contract execution rate must come from Eastlake Bank. Scope: LPR Cannot replace the contract rate.""",
        ),
    ),
    5: (
        (
            "debt_plan.md",
            """## Mortgage Contract Facts
Eastlake Bank evidence: principal RMB 1,260,000; contract rate 4.10%; monthly payment RMB 9,860; minimum partial prepayment RMB 50,000 with 7 business days notice. Joint-borrower responsibility needs separate approval. LPR remains only a benchmark.""",
        ),
        (
            "source_evidence.md",
            """## Mortgage Source Lineage
Message mortgage-review-5520 verifies RMB 1,260,000, 4.10%, RMB 9,860, RMB 50,000 and Joint-borrower responsibility separately from LPR.""",
        ),
    ),
    6: (
        (
            "debt_plan.md",
            """## Prepayment Alternatives
Compare RMB 120,000 now with a Six-month rigid-expense buffer and clearing Credit cards first. Mortgage prepayment is Unauthorized; Do not authorize now and do not execute a transfer.""",
        ),
        (
            "support_cashflow.md",
            """## Liquidity Alternative
Retain a 6-month buffer for rigid expenses before considering RMB 120,000 prepayment. Credit cards rank ahead of an Unauthorized mortgage action.""",
        ),
    ),
    7: (
        (
            "protection_plan.md",
            """# Protection Plan
- Policy renewals: Daughter's Medical policy RMB 7,200 and personal Critical-illness policy RMB 9,600.
- Payment account must be verified from insurer evidence.
- Relationship-change status: policyholder and beneficiary changes are Unconfirmed and Incomplete until insurer confirmation.
- Daughter reserve boundary: the RMB 50,000 education and medical reserve is protected.""",
        ),
        (
            "support_cashflow.md",
            """## Insurance Expenses
Medical policy and Critical-illness policy renewals stay separate from the Unconfirmed Relationship-change status and Payment account review.""",
        ),
    ),
    8: (
        (
            "protection_plan.md",
            """## Official Policy Notice
Daughter medical premium RMB 7,200 is due August 16, 2026; critical-illness premium RMB 9,600 is due August 22, 2026. Relationship change was Not submitted; renewal and administration remain separate.""",
        ),
        (
            "support_cashflow.md",
            """## Insurance Dates
Reserve RMB 7,200 for 2026-08-16 and RMB 9,600 for 2026-08-22. Relationship change remains Not submitted and is not a completed cash event.""",
        ),
    ),
    9: (
        (
            "protection_plan.md",
            """## Irreversible Alternatives
Moving remaining transition money into an Education fund is only an option; analyze Liquidity before any action. Daughter reserve boundary: existing RMB 50,000 is Forbidden to use for Mortgage or card repayment.""",
        ),
        (
            "asset_inventory.md",
            """## Protected Reserve Check
Daughter's education and medical reserve remains RMB 50,000, frozen and Forbidden for debt repayment. The proposed Education fund is an Irreversible alternative, not an executed transfer.""",
        ),
    ),
    10: (
        (
            "support_cashflow.md",
            """## School Expenses
Official Autumn care and meals are RMB 18,600, payable 2026-08-17 through 2026-08-21. The Earlier estimate of RMB 18,500 was Different and not a school bill. Status: Unpaid; Do not pay in advance.""",
        ),
        (
            "protection_plan.md",
            """## School Payment Boundary
Official School expenses are RMB 18,600 in the August 17-21 window; they remain Unpaid and must not draw from the protected reserve.""",
        ),
    ),
    11: (
        (
            "support_cashflow.md",
            """## Thirty-Day Cash Buffer
Received: RMB 180,000 transition payment. Receivable: RMB 8,000 support. Insurance expenses: RMB 7,200 and RMB 9,600. School expenses: RMB 18,600. Mortgage: RMB 9,860 monthly. Credit-card statements: RMB 31,800 and RMB 12,800. Frozen restricted reserve: RMB 50,000. Conservative plan: maintain the Thirty-day cash buffer and Do not prepay.""",
        ),
        (
            "asset_inventory.md",
            """## Cashflow Classification
Received RMB 180,000, Receivable RMB 8,000, Living emergency fund RMB 120,000 and Frozen restricted reserve RMB 50,000 remain separate.""",
        ),
        (
            "debt_plan.md",
            """## Conservative Sequence
Reserve Insurance expenses and School expenses, clear authorized Credit cards when approved, maintain the Thirty-day cash buffer and Do not prepay the Mortgage.""",
        ),
    ),
    12: (
        (
            "support_cashflow.md",
            """## Child Support Received
Backend transaction tx_dar_support_20260810 confirms Actual posting of RMB 8,000. Status changes to Child support received. Preserve the Earlier delay and Non-receipt record as History.""",
        ),
        (
            "asset_inventory.md",
            """## Actual Receipt Update
Child support received: RMB 8,000 on 2026-08-10; acct_checking_main backend balance RMB 236,000. Preserve the earlier Delay history rather than erasing it.""",
        ),
    ),
    13: (
        (
            "execution_log.md",
            """# Execution Log
Authorization at 2026-08-10 13:00 +08:00 covered exactly card_cmb_family RMB 31,800 and card_boc_parents RMB 12,800 from acct_checking_main. Tool results and Backend objects are recorded separately. Unauthorized actions: no Mortgage prepayment, bank transfer, reserve use or investment order.""",
        ),
        (
            "debt_plan.md",
            """## Authorized Payments
Authorization covers card_cmb_family RMB 31,800 and card_boc_parents RMB 12,800 from acct_checking_main only. No overpayment and no Mortgage action.""",
        ),
    ),
    14: (
        (
            "execution_log.md",
            """## Payment Reconciliation
Tool results contain two payment Backend objects. Actual payment results: both cards posted Separately for RMB 31,800 and RMB 12,800. Reconciliation status: complete; New balances were read after execution.""",
        ),
        (
            "debt_plan.md",
            """## Actual Payment Results
Two card statements are paid through Authorized payments. card_cmb_family statement balance RMB 0 with RMB 5,000 unbilled; card_boc_parents statement balance RMB 0 with RMB 1,200 unbilled. Backend objects and New balances reconcile separately.""",
        ),
        (
            "asset_inventory.md",
            """## Card Balance Reconciliation
Actual payment results show statement balances RMB 0 and RMB 0; New balances retain unbilled RMB 5,000 and RMB 1,200 with Backend evidence.""",
        ),
    ),
    15: (
        (
            "debt_plan.md",
            """## Revolving Interest Adjustment
New fact: card_cmb_family has RMB 486 (48600 minor units) Revolving interest. Recheck Backend evidence; Previous balance does not override the new fact. Actual payment results now leave RMB 5,486 unbilled.""",
        ),
        (
            "asset_inventory.md",
            """## Interest Recheck
Backend Recheck records RMB 486 Revolving interest and New balances: card_cmb_family RMB 5,486 unbilled; card_boc_parents RMB 1,200 unbilled.""",
        ),
        (
            "execution_log.md",
            """## Post-Payment Interest
Actual payment results remain valid; a later RMB 486 Revolving interest adjustment changes the current New balances and requires Recheck against Backend objects.""",
        ),
    ),
    16: (
        (
            "calendar_plan.md",
            """# Calendar Plan
Seven confirmed non-duplicate reminders were checked or created.
- Policy dates: medical 2026-08-16 and critical-illness 2026-08-22.
- School payment window: starts 2026-08-17.
- Mortgage dates and debit review: 2026-08-19.
- Child support review: 2026-08-28.
- Pension review: 2026-11-01.
- 30-day summary review: 2026-08-28.
Duplicate check: list existing events before creation; one business reminder per lane.""",
        ),
    ),
    17: (
        (
            "source_evidence.md",
            """## Personal Pension Tax Policy
Annual pre-tax deduction limit is RMB 12,000 and withdrawal taxation is 3%. Do not automatically contribute the full amount; actual contributions, Liquidity, Policies and Credit cards must be reviewed first.""",
        ),
        (
            "protection_plan.md",
            """## Personal Pension Plan
RMB 12,000 and 3% are policy anchors, not an instruction to fund. Do not automate or automatically contribute the full amount. Liquidity, policy renewals and Credit cards come first; no contribution or investment order was made.""",
        ),
    ),
    18: (
        (
            "debt_plan.md",
            """## Mortgage Window Update
Application window is August 19 through August 21, 2026. Joint-borrower responsibility needs both parties' materials and Independent approval. Prepayment remains Unauthorized; No debit or application was executed.""",
        ),
        (
            "calendar_plan.md",
            """## Mortgage Dates Update
August 19-21 is an application window, not authorization. Calendar reminder keeps the Mortgage and No debit status visible.""",
        ),
        (
            "execution_log.md",
            """## Mortgage Non-Execution
Unauthorized: no debit, no prepayment application and no Joint-borrower responsibility change during the August 19-21 window.""",
        ),
    ),
    19: (
        (
            "debt_plan.md",
            """## Three Mortgage Choices
1. RMB 50,000 now: reduces Cash buffer and is not authorized.
2. Reassess at year-end after Premiums, School expenses and Child support stability are known.
3. Do not prepay: preserve liquidity and Joint-borrower responsibility review.
Decision: Do not prepay now; Reassess at year-end rather than acting only on rate differences.""",
        ),
        (
            "support_cashflow.md",
            """## Mortgage Decision Liquidity
Keep the Cash buffer for Premiums RMB 16,800, School expenses RMB 18,600 and support volatility. RMB 50,000 prepayment is deferred; Reassess at year-end.""",
        ),
    ),
    20: (
        (
            "protection_plan.md",
            """## Policy Confirmation
Daughter's medical policy is Renewed for RMB 7,200 from the original debit account. Critical-illness policy is Still pending for August 22. Relationship change is Still incomplete and not submitted.""",
        ),
        (
            "support_cashflow.md",
            """## Insurance Status Separation
Daughter's medical policy RMB 7,200 is Renewed. Critical-illness policy payment remains pending, and Relationship change remains incomplete.""",
        ),
        (
            "asset_inventory.md",
            """## Protection Status
Daughter's medical policy Renewed at RMB 7,200; Critical-illness policy Still pending; Relationship change Still incomplete. These are separate backend states.""",
        ),
    ),
    21: (
        (
            "final_summary.md",
            """# Final Summary
## Verified facts
Actual receipt: transition RMB 180,000 and child support RMB 8,000. Daughter reserve RMB 50,000 remains frozen. Backend verification includes banking, cards, email, calendar and Notion evidence.
## Executed actions
Actual payments: Authorized card payments of RMB 31,800 and RMB 12,800 completed; later RMB 486 interest is reflected.
## Pending items
Pending payment: critical-illness policy RMB 9,600; School RMB 18,600; normal Mortgage RMB 9,860. Relationship change remains incomplete.
## Deferred decisions
Mortgage prepayment and education-fund transfer are deferred. Personal Pension contribution remains RMB 0.
## Forbidden funds
Child reserve acct_medical_reserve RMB 50,000 cannot fund cards or Mortgage.
## Next-month review
Review date 2026-09-05: support receipt stability, premiums, School payment, Mortgage debit, card interest and liquidity.
## Evidence links
See source_evidence.md, asset_inventory.md, debt_plan.md, support_cashflow.md, protection_plan.md, calendar_plan.md and execution_log.md.""",
        ),
    ),
    22: (
        (
            "final_summary.md",
            """## Archived Closeout
- Authorized and completed: two card payments, RMB 31,800 and RMB 12,800.
- Completed verification: child support RMB 8,000, medical policy RMB 7,200 and seven calendar reminders.
- Deferred decisions: Mortgage prepayment RMB 50,000 or RMB 120,000, education-fund transfer and Pension contribution.
- Forbidden funds: daughter's RMB 50,000 reserve.
- Next-month review: 2026-09-05, starting with support, critical-policy status, School receipt, Mortgage debit and current card balances.""",
        ),
        (
            "execution_log.md",
            """## Archive Status
Authorization and Completed actions are limited to the two card payments. Deferred decisions include Mortgage prepayment and pension funding. Forbidden funds remain untouched. Next-month review is 2026-09-05.""",
        ),
        (
            "protection_plan.md",
            """## Next Materials and Handoff
Policy renewals remain separated from Relationship-change status. Irreversible alternatives remain deferred. Next materials: critical-policy receipt, relationship-change forms, School receipt and Pension liquidity review.""",
        ),
    ),
}


async def handle_record_event(
    rec: Recorder,
    state: dict[str, Any],
    spec: dict[str, Any],
    action: dict[str, Any],
) -> None:
    stage = int(spec["virtual_stage"])
    if stage == 0:
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("credit_card", "list_cards", {"user_id": USER_ID})
        await rec.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 100, "page": 1})
    elif stage == 1:
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await rec.call("banking", "get_account", {"account_id": CHECKING_ACCOUNT_ID})
        await rec.call("banking", "get_account", {"account_id": PROTECTED_ACCOUNT_ID})
        await rec.call("brokerage", "list_accounts", {"user_id": USER_ID})
        await rec.call("brokerage", "get_positions", {"account_id": "acct_brk_liang"})
        await _read_cards(rec, include_unbilled=True)
    elif stage == 2:
        await _read_email(rec, "RMB 8,000 July child-support")
    elif stage == 3:
        await _read_cards(rec, include_unbilled=True)
    elif stage == 4:
        await _ensure_lpr_anchor(rec)
    elif stage == 5:
        await _read_email(rec, "Joint mortgage prepayment estimate")
    elif stage == 7:
        await _read_email(rec, "medical policy")
        await _read_email(rec, "critical-illness policy")
    elif stage == 8:
        await _read_email(rec, "relationship-change status")
    elif stage == 9:
        await rec.call("banking", "get_account", {"account_id": PROTECTED_ACCOUNT_ID})
        await rec.call(
            "banking",
            "list_transactions",
            {"account_id": PROTECTED_ACCOUNT_ID, "since": "2026-07-30", "limit": 100, "page": 1},
        )
    elif stage == 10:
        await _read_email(rec, "Official autumn care and meal notice")
    elif stage == 11:
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await _read_cards(rec)
    elif stage == 12:
        await rec.call("banking", "get_account", {"account_id": CHECKING_ACCOUNT_ID})
        await rec.call(
            "banking",
            "list_transactions",
            {"account_id": CHECKING_ACCOUNT_ID, "since": "2026-08-10", "limit": 100, "page": 1},
        )
    elif stage == 13:
        await rec.call(
            "credit_card",
            "make_payment",
            {"card_id": "card_cmb_family", "amount_minor": 3_180_000, "source_hint": CHECKING_ACCOUNT_ID},
        )
        await rec.call(
            "credit_card",
            "make_payment",
            {"card_id": "card_boc_parents", "amount_minor": 1_280_000, "source_hint": CHECKING_ACCOUNT_ID},
        )
        await rec.call("credit_card", "get_card", {"card_id": "card_cmb_family"})
        await rec.call("credit_card", "get_card", {"card_id": "card_boc_parents"})
    elif stage == 14:
        await _read_cards(rec, include_unbilled=True)
    elif stage == 15:
        await _read_cards(rec, include_unbilled=True)
        await rec.call("credit_card", "get_statement", {"statement_id": "stm_family_20260728"})
    elif stage == 16:
        await _ensure_calendar(rec)
    elif stage == 17:
        await rec.call("banking", "get_account", {"account_id": "acct_pension"})
        await rec.call(
            "banking",
            "list_transactions",
            {"account_id": "acct_pension", "since": "2026-07-30", "limit": 100, "page": 1},
        )
        await _read_email(rec, "Personal pension account semiannual summary")
        await rec.call("brokerage", "get_positions", {"account_id": "acct_brk_liang"})
    elif stage == 18:
        await _read_email(rec, "Prepayment application window")
    elif stage == 20:
        await _read_email(rec, "Daughter medical policy renewal confirmation")
    elif stage == 21:
        await rec.call("banking", "list_accounts", {"user_id": USER_ID})
        await _read_cards(rec, include_unbilled=True)
        await rec.call("calendar", "list_events", {"calendar_id": CALENDAR_ID, "max_results": 500, "page": 1})
        await rec.call("notion", "API-post-database-query", {"database_id": "db_finance_ledger", "page_size": 100})
    elif stage == 22:
        await rec.call("banking", "get_account", {"account_id": PROTECTED_ACCOUNT_ID})
        await rec.call("credit_card", "get_card", {"card_id": "card_cmb_family"})

    for path, text in WORKSPACE_UPDATES.get(stage, ()):
        rec.workspace_write(path, text)
    state["events"].append(
        {
            "step": spec["step"],
            "source_event_id": spec["source_event_id"],
            "stage": stage,
        }
    )


ActionHandler = Callable[[Recorder, dict[str, Any], dict[str, Any], dict[str, Any]], Any]
ACTION_HANDLERS = {"record_event": handle_record_event}


def _write_trajectory(spec: dict[str, Any], response: str, rec: Recorder) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    calls = [
        {
            "tool_call_id": item["tool_call_id"],
            "function_name": item["function_name"],
            "arguments": item["arguments"],
        }
        for item in rec.calls
    ]
    results = [
        {
            "source_call_id": item["tool_call_id"],
            "content": json.dumps(item["result"], ensure_ascii=False, default=str),
            "extra": {"success": item["success"], "error": item["error"]},
        }
        for item in rec.calls
    ]
    trajectory = {
        "schema_version": "ATIF-v1.7",
        "session_id": f"oracle-{spec['step']}",
        "agent": {"name": "divorce-asset-rebuild-oracle", "version": "1.0.0"},
        "steps": [
            {"step_id": 1, "source": "user", "message": str(spec["source_event_id"])},
            {
                "step_id": 2,
                "source": "agent",
                "message": response,
                "tool_calls": calls,
                "observation": {"results": results},
                "llm_call_count": 0,
            },
        ],
        "final_metrics": {
            "tool_calls": len(calls),
            "tool_errors": sum(not item["success"] for item in rec.calls),
        },
    }
    (LOGS / "trajectory.json").write_text(
        json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (LOGS / "oracle-result.json").write_text(
        json.dumps(
            {"step": spec["step"], "response_used": response, "calls": rec.calls},
            ensure_ascii=False,
            indent=2,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )


async def execute(spec: dict[str, Any]) -> str:
    required = (
        "step",
        "virtual_stage",
        "source_event_id",
        "response",
        "response_paraphrase",
        "actions",
        "expected_env",
    )
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["actions"], list):
        raise ValueError("actions must be a list")
    state = _load_state()
    rec = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = str(action.get("kind") or "")
        handler = ACTION_HANDLERS.get(kind)
        if handler is None:
            known = sorted(ACTION_HANDLERS) or "(none - this oracle is unwired)"
            raise RuntimeError(
                f"oracle.py: no handler for action kind {kind!r} in step {spec['step']}. "
                f"Known kinds: {known}"
            )
        await handler(rec, state, spec, action)
    style = os.environ.get("ORACLE_STYLE", "canonical").strip().casefold()
    if style not in {"canonical", "paraphrase"}:
        raise ValueError(f"unsupported ORACLE_STYLE: {style!r}")
    key = "response_paraphrase" if style == "paraphrase" else "response"
    response = spec.get(key)
    if not isinstance(response, str) or not response.strip():
        raise ValueError(f"missing non-empty {key}")
    _save_state(state)
    _write_trajectory(spec, response, rec)
    return response


def _is_successful_run(value: Any) -> bool:
    return _is_success(value)


async def _main_async() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: oracle.py /solution/step_spec.json")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(await execute(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main_async()))
