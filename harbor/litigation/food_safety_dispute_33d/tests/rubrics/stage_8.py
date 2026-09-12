"""Stage 8: case acceptance notice."""
from __future__ import annotations
from ._helpers import _notifications, _notion_page_text, _stage_corpus

def s8_responds_acceptance(env) -> bool:
    text = _stage_corpus(env, 8)
    return any(k in text for k in ("accepted", "case filing", "case number", "Civil First Instance")) and sum(k in text for k in ("evidence submission", "testing", "trial hearing", "defense", "preparation opinion", "follow-up plan")) >= 2

def s8_detects_acceptance_notice(env) -> bool:
    notifs = _notifications(env)
    if notifs is None: return False
    notice = any(
        isinstance(item, dict)
        and str(item.get("notification_id") or "") == "ntf_food_s8_case_accepted"
        for item in notifs
    )
    # The acceptance conclusion is read from the durable journal record.  This
    # keeps paraphrased replies from changing the result while retaining the
    # backend notification identity as the factual anchor.
    record = (_notion_page_text(env, "acceptance") or "").lower()
    return notice and any(
        phrase in record
        for phrase in ("accepted", "case filing", "case number", "civil first instance", "acceptance notice")
    )
CHECKS = [("s8_detects_acceptance_notice", s8_detects_acceptance_notice, 0.5)]
