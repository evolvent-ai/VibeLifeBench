"""Stage 5: bind the insurance quote to inbox evidence and exact budget state."""
from __future__ import annotations

from loguru import logger

from .shared._helpers import _call, _tool_call_matches, workspace_file_content


def s5_budget_running_total(env) -> bool:
    searched = _tool_call_matches(
        env,
        "email",
        "search_emails",
        lambda a: "ti-q-20260602" in str(a.get("query") or "").casefold(),
        stage=5,
    )
    email_result = _call(
        env,
        "email",
        "search_emails",
        query="TI-Q-20260602",
        folder="INBOX",
        page=1,
        page_size=20,
    )
    rows = email_result.get("emails", email_result.get("messages", [])) if isinstance(email_result, dict) else email_result
    if not isinstance(rows, list):
        return False
    summary = next(
        (
            row for row in rows
            if isinstance(row, dict) and "ti-q-20260602" in str(row).casefold()
        ),
        None,
    )
    if not summary or not summary.get("email_id"):
        return False
    email_id = str(summary["email_id"])
    read = _tool_call_matches(
        env,
        "email",
        "read_email",
        lambda a: str(a.get("email_id") or "") == email_id,
        stage=5,
    )
    amount_searches = [
        _call(env, "email", "search_emails", query=query, folder="INBOX", page=1, page_size=20)
        for query in ("1,860", "2,180", "4,040")
    ]
    backend_amounts = all("ti-q-20260602" in str(result).casefold() for result in amount_searches)
    expense = workspace_file_content(env, "/workspace/expense_summary.md").casefold().replace(",", "")
    inbox_ok = read and backend_amounts
    object_bound = all(x in expense for x in ("ti-q-20260602", "1860", "2180", "4040", "cny"))
    expiry = any(x in expense for x in ("2026-06-05t09:55", "72h", "72 h", "72hours"))
    status = any(x in expense for x in ("quote", "pending", "confirm", "payment"))
    running = any(x in expense for x in ("running", "running total", "total"))
    result = bool(searched and inbox_ok and object_bound and expiry and status and running)
    logger.info("s5_budget_running_total: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s5_budget_running_total", s5_budget_running_total, 2.5)]
