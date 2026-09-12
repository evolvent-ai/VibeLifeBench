"""Stage 22 checker: user asks reimbursement prep."""
from __future__ import annotations

from loguru import logger

from ._helpers import (
    _stage_tools,
    _tool_called_in_stage,
    _sent_emails,
    _email_has_approval_request,
    _email_to_zhang,
    _notion_text,
    _any,
)


def s22_sent_email(env) -> bool:
    """Stage 22 called send_email AND backend _sent_emails has at least one email to zhang_manager."""
    sent_tool = _tool_called_in_stage(env, 22, ["send_email"])
    emails = _sent_emails(env)
    to_zhang = any(_email_to_zhang(e) for e in emails)
    ok = sent_tool and to_zhang
    logger.info(f"s22_sent_email: sent_tool={sent_tool}, to_zhang={to_zhang}")
    return ok


def s22_email_has_amount(env) -> bool:
    """At least one email to zhang_manager contains >5000 amount AND approval request."""
    emails = _sent_emails(env)
    for e in emails:
        if _email_has_approval_request(e):
            logger.info("s22_email_has_amount: found approval request email to zhang_manager with >5000")
            return True
    logger.info("s22_email_has_amount: False")
    return False


def s22_notion_reimbursement(env) -> bool:
    """_notion_text contains both trip/flight/hotel info AND reimbursement/expense/approval keywords."""
    text = _notion_text(env)
    has_trip = _any(text, ["flight", "hotel", "flight", "hotel", "flight", "accommodation", "itinerary"])
    has_expense = _any(text, ["reimbursement", "expense", "approval", "breakdown", "reimbursement", "expense", "budget", "travel"])
    ok = has_trip and has_expense
    logger.info(f"s22_notion_reimbursement: trip={has_trip} expense={has_expense} -> {ok}")
    return ok


CHECKS = [
    ("s22_sent_email", s22_sent_email, 2.0),
    ("s22_email_has_amount", s22_email_has_amount, 1.75),
    ("s22_notion_reimbursement", s22_notion_reimbursement, 1.25),
]
