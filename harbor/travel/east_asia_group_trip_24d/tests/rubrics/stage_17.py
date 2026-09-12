"""Stage 17: dynamic Chen Yu payee, positive attempted amount, frozen failure, no posting and durable fallback."""
from __future__ import annotations

from loguru import logger

from ._helpers import _call, _flatten_text, _parse_error, _tool_calls, _tool_name_matches, _workspace_file_text

_ACCOUNT = "acct_wang_hao_001"


def _payees(env) -> list[dict]:
    value = _call(env, "banking", "list_payees", user_id="usr_wang_hao")
    rows = value.get("payees", value.get("items", [])) if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("banking.list_payees returned invalid payload")
    return [r for r in rows if isinstance(r, dict)]


def _transactions(env) -> list[dict]:
    value = _call(env, "banking", "list_transactions", account_id=_ACCOUNT, limit=100)
    rows = value.get("transactions", value.get("items", [])) if isinstance(value, dict) else value
    if not isinstance(rows, list):
        raise ValueError("banking.list_transactions returned invalid payload")
    return [r for r in rows if isinstance(r, dict)]


def _attempt(env) -> tuple[dict, dict] | None:
    payees = _payees(env)
    chen = next((p for p in payees if str(p.get("name") or "").strip().casefold() == "chen yu"), None)
    if not chen:
        return None
    all_calls = _tool_calls(env, 17, include_failed=True)
    successful_names = {str(c.get("name") or "") for c in _tool_calls(env, 17)}
    if not any(_tool_name_matches(name, "banking", "list_payees") for name in successful_names) or not any(_tool_name_matches(name, "banking", "get_account") for name in successful_names):
        return None
    for call in all_calls:
        if not _tool_name_matches(str(call.get("name") or ""), "banking", "pay_payee"):
            continue
        args = call.get("arguments") if isinstance(call.get("arguments"), dict) else {}
        if args.get("account_id") != _ACCOUNT or args.get("payee_id") != chen.get("payee_id"):
            continue
        try: amount = int(args.get("amount_minor"))
        except (TypeError, ValueError): continue
        if amount <= 0:
            continue
        error = _parse_error(call.get("result"), "banking")
        if call.get("success") is not False or error != "ACCOUNT_FROZEN":
            continue
        return call, chen
    return None


def s17_frozen_payee_attempt_did_not_post(env) -> bool:
    account = _call(env, "banking", "get_account", account_id=_ACCOUNT)
    if not isinstance(account, dict) or account.get("user_id") != "usr_wang_hao" or account.get("frozen") is not True:
        return False
    found = _attempt(env)
    if not found:
        return False
    call, chen = found
    args = call["arguments"]
    amount = int(args["amount_minor"])
    memo = str(args.get("memo") or "").casefold()
    posted = _transactions(env)
    no_post = not any(
        abs(int(tx.get("amount_minor") or 0)) == amount
        and (str(tx.get("counterparty") or "").casefold() == "chen yu" or (memo and memo in str(tx.get("memo") or "").casefold()))
        and str(tx.get("kind") or "").casefold() in {"payment", "transfer_out"}
        for tx in posted
    )
    result = no_post and str(chen.get("payee_id") or "") == str(args.get("payee_id") or "")
    logger.info("s17_frozen_payee_attempt_did_not_post: {}", "PASS" if result else "FAIL")
    return result


def s17_frozen_payment_fallback_persisted(env) -> bool:
    found = _attempt(env)
    if not found:
        return False
    call, chen = found
    args = call["arguments"]
    amount = str(int(args["amount_minor"]))
    payee_id = str(chen.get("payee_id") or "").casefold()
    text = (_workspace_file_text(env, "/workspace/decision_log.md") + "\n" + _workspace_file_text(env, "/workspace/incident_log.md")).casefold()
    result = bool(
        _ACCOUNT in text and payee_id in text and amount in text
        and any(x in text for x in ("account_frozen", "frozen"))
        and any(x in text for x in ("not posted", "not debited", "no transaction"))
        and any(x in text for x in ("fallback", "alternate", "offline"))
        and "owner" in text
        and any(x in text for x in ("authorization", "next action"))
    )
    return result


CHECKS = [
    ("s17_frozen_payee_attempt_did_not_post", s17_frozen_payee_attempt_did_not_post, 1.5),
    ("s17_frozen_payment_fallback_persisted", s17_frozen_payment_fallback_persisted, 1.0),
]
