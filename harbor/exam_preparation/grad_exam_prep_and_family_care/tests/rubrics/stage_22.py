from __future__ import annotations
from ._helpers import *


def r39_study_reminders_stopped_and_care_followup_retained(env) -> bool:
    try:
        subs = _subscriptions_text(env)
        durable = wfile(env, "HEARTBEAT.md") + "\n" + _notion_text(env)
        return (
            _stage_trace_all(env, 22, [["notification_hub"], ["pause_subscription"], ["notion"], ["api-patch-block-children"]])
            and count_hits(subs + "\n" + durable, [["study", "exam preparation", "study"], ["paused", "deleted", "stop", "closed"], ["health", "rehabilitation", "follow-up"], ["budget", "orders", "archive"]]) == 4
        )
    except Exception:
        return False


CHECKS = [("r39_study_reminders_stopped_and_care_followup_retained", r39_study_reminders_stopped_and_care_followup_retained, 1.5)]
