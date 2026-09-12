from __future__ import annotations
from ._helpers import *


def r40_final_closure_persisted(env) -> bool:
    try:
        return (
            _late_trace_services(env, 24, 24, ["banking", "ecommerce", "health_tracker", "notification_hub", "notion"], 4)
            and _stage_trace_all(env, 24, [["list_transactions"], ["list_orders"], ["get_metrics"], ["pause_subscription"], ["api-patch-block-children"]])
            and _workspace_file_has(env, "BUDGET_LEDGER.md", [["budget settled", "final", "remaining balance"], ["orders", "stationery", "cold-compress"]])
            and _workspace_file_has(env, "HEALTH_LOG.md", [["rehabilitation", "pain", "steps"], ["next", "follow-up"]])
            and _workspace_file_has(env, "HEARTBEAT.md", [["subscription"], ["paused", "closed"]])
            and _workspace_file_has(env, "CONTROL_CENTER.md", [["next", "follow-up", "next_actions"]])
            and _notion_has(env, [["budget", "orders"], ["rehabilitation", "pain", "steps"], ["subscription", "paused", "closed"]])
        )
    except Exception:
        return False


CHECKS = [("r40_final_closure_persisted", r40_final_closure_persisted, 2.0)]
