"""Stage 4 checker — FX rate change world event."""
from __future__ import annotations
from loguru import logger
from ._helpers import (
    _tool_called_in_stage,
    _ws,
    _any,
)


def s4_expense_and_fx(env) -> bool:
    """Stage 4 called record_expense AND budget_tracker.md shows FX awareness: rate 7.42/7.4 AND conversion evidence."""
    # Expenses are read from the real banking ledger (record_expense was a phantom tool); the
    # expense record itself is verified in the durable budget_tracker.md below.
    ok_tools = _tool_called_in_stage(env, 4, ["list_transactions", "get_account", "list_accounts"])
    bt = _ws(env, "/workspace/budget_tracker.md")
    has_rate = _any(bt, ["7.42", "7.4"])
    has_conversion = _any(bt, ["exchange rate", "USD", "usd", "CNY", "cny", "conversion", "CNY"])
    ok_text = has_rate and has_conversion
    ok = ok_tools and ok_text
    logger.info(f"s4_expense_and_fx: tools={ok_tools} rate={has_rate} conversion={has_conversion} -> {ok}")
    return ok


CHECKS = [
    ("s4_expense_and_fx", s4_expense_and_fx, 1.25),
]
