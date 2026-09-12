"""Stage 10: defense notice and follow-up."""
from __future__ import annotations
from ._helpers import _food_journal_text, _notifications

def s10_detects_defense(env) -> bool:
    notifications = _notifications(env)
    if notifications is None: return False
    notice = any(str(item.get("notification_id") or "") == "ntf_food_s10_defense" or ("defense" in str(item.get("title") or "") and any(key in str(item.get("body") or "") for key in ("knowingly buying counterfeit goods", "labeling defect", "refund plus threefold compensation"))) for item in notifications)
    journal = _food_journal_text(env)
    return journal is not None and notice and any(k in journal for k in ("defense", "cross-examination")) and any(k in journal for k in ("cross-examination", "check item by item", "rebuttal", "strengthen evidence")) and sum(k in journal for k in ("refund plus threefold compensation", "knowingly buying counterfeit goods", "labeling defect")) >= 2
CHECKS = [("s10_defense_notice_and_followup", s10_detects_defense, 0.75)]

