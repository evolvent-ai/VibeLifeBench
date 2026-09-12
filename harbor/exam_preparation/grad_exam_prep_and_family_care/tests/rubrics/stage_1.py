from __future__ import annotations
from ._helpers import *

def r04_notion_init(env) -> bool:
    try:
        return (
            _stage_trace_all(env, 1, [["api-", "notion"], ["post", "patch", "database", "block", "page"]])
            and _workspace_file_has(env, "CONTROL_CENTER.md", [["Control Center", "exam progress", "mock"]])
            and _workspace_file_has(env, "HEALTH_LOG.md", [["medical", "rehabilitation", "health"]])
            and _workspace_file_has(env, "BUDGET_LEDGER.md", [["budget", "ledger", "3500"]])
            and _notion_has(env, [
                ["4 mocks", "four mocks", "full-length", "mock", "mock"],
                ["4 hours", "4 hours", "rest"],
                ["mother_li", "Ms. Li", "Dr. Wang"],
                ["3500", "800", "budget"],
            ])
        )
    except Exception:
        return False

def r05_calendar_seed(env) -> bool:
    try:
        return (
            _stage_trace_all(env, 1, [["calendar"], ["create_event", "update_event"]])
            and _stage_reply_has(env, 1, [
                ["mock", "full-length"],
                ["follow-up", "hospital"],
                ["4 hours", "rest", "split"],
            ])
            and _calendar_event_count(env, [["full-length", "mock"]]) >= 1
            and _calendar_event_count(env, [["follow-up", "Ms. Li", "knee"]]) >= 1
            and _calendar_event_count(env, [["rest", "break", "split", "4 hours"], ["study", "mock", "Math"]]) >= 1
        )
    except Exception:
        return False

def r06_subscribe_watch(env) -> bool:
    try:
        subs = _subscriptions_text(env)
        return (
            _stage_trace_all(env, 1, [["notification_hub__list_subscriptions", "list_subscriptions"]])
            and _subscription_sources_active(env, [
                ("health_tracker", "mother_health"),
                ("ecommerce", "exam_supplies"),
                ("email", "doctor_exam_notice"),
                ("notion", "study_progress"),
            ])
            and _workspace_file_has(env, "HEARTBEAT.md", [["health"], ["ecommerce", "stock", "orders"], ["email"]])
            and count_hits(subs, [["health_tracker", "mother_health"], ["ecommerce", "exam_supplies"], ["email", "doctor_exam_notice"], ["notion", "study_progress"]]) == 4
        )
    except Exception:
        return False

CHECKS = [
    ("r04_notion_init", r04_notion_init, 3.0),
    ("r05_calendar_seed", r05_calendar_seed, 3.0),
    ("r06_subscribe_watch", r06_subscribe_watch, 3.0),
]
