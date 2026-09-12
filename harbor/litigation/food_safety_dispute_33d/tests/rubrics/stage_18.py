"""Stage 18: seller appeal and respondent preparation."""
from __future__ import annotations
from ._helpers import _food_journal_text, _notifications

def s18_identifies_appellee(env) -> bool:
    notices = _notifications(env)
    journal = _food_journal_text(env)
    return notices is not None and journal is not None and any(str(item.get("notification_id") or "") == "ntf_food_s18_appeal" or "appeal" in str(item.get("title") or "").lower() for item in notices) and "respondent" in journal and any(k in journal for k in ("second instance", "seller appeal", "opposing appeal")) and any(k in journal for k in ("defense", "respond to the case", "evidence index", "second-instance preparation"))
CHECKS = [("s18_appeal_notice_and_persisted_response", s18_identifies_appellee, 0.75)]

