from __future__ import annotations
from ._helpers import *


def r34_quiet_health_and_order_heartbeat(env) -> bool:
    try:
        return (
            _stage_trace_all(env, 8, [["health_tracker"], ["get_metrics"], ["ecommerce"], ["list_orders", "track_order"]])
            and _workspace_file_has(env, "HEARTBEAT.md", [["HEARTBEAT", "heartbeat", "review"], ["health", "pain", "steps"], ["orders", "shipment", "stock"]])
            and not _stage_reply_has(env, 8, [["promotion", "recommend purchase", "add to cart"]])
        )
    except Exception:
        return False


CHECKS = [("r34_quiet_health_and_order_heartbeat", r34_quiet_health_and_order_heartbeat, 1.5)]
