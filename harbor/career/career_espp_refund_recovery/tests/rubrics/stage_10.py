"""Stage 10 — in the correct HR original thread generate a unique unsent calculation draft."""
from __future__ import annotations

from ._helpers import norm_num, sent_emails, stage_call_matches, text_has, unique_message

HR = "hr.luqian@ximingsemi.com"
REVISE_MESSAGE_ID = "<20260624-revise@ximingsemi.com>"
HISTORY_MESSAGE_ID = "<20240418-espp-plan@ximingsemi.com>"
_BAD_BASE = ("redemption spread basis is income", "redemption spread calculated from tenure", "redemption spread calculated from tenure")


def s10_demand_letter_drafted(env) -> bool:
    if not stage_call_matches(env, 10, "read_email", {"email_id": "103"}):
        return False
    draft = unique_message(
        env,
        folder="drafts",
        recipient=HR,
        in_reply_to=REVISE_MESSAGE_ID,
        required_groups=[
            [HISTORY_MESSAGE_ID], ["vested"], ["base date"], ["quoted market value", "market"],
            ["value"], ["proposal"], ["shortfall"],
            ["art_cc_509"], ["art_cc_496"], ["art_cc_497"], ["art_cc_151"],
            ["amount", "make"], ["retain", "claiming"],
        ],
    )
    if not draft or str(draft.get("date") or "") < "2026-06-24T09:55:00Z":
        return False
    body = str(draft.get("body_text") or draft.get("body") or "").lower()
    corpus = norm_num(body)
    if not all(value in corpus for value in ("4955", "60.00", "297300", "200300", "97000")):
        return False
    if any(term in body for term in _BAD_BASE):
        return False
    for msg in sent_emails(env):
        if str(msg.get("in_reply_to") or "") == REVISE_MESSAGE_ID:
            return False
    # Preserve the source requirement's full meaning: payroll is supporting
    # evidence only and must not be treated as the redemption-spread basis.
    return text_has(body, [[
        "payroll statements are income support only and are not the redemption spread basis",
        "payroll account statements are income and cash-flow support only, not the redemption spread basis",
        "income and cash-flow support only, not the redemption spread basis",
    ]])


CHECKS = [("s10_demand_letter_drafted", s10_demand_letter_drafted, 3.0)]
