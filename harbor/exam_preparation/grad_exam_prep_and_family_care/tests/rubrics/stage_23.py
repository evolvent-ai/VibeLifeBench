from __future__ import annotations
from ._helpers import *

def r31_health_month_export(env) -> bool:
    try:
        text = _agent_reply(env, 23) + "\n" + _trace_text(env, 23, 23) + "\n" + wfile(env, "HEALTH_LOG.md") + "\n" + _health_text(env)
        return (
            _stage_trace_all(env, 23, [["health_tracker"], ["get_metrics", "list_health_alerts"], ["notion"], ["api-patch-block-children"]])
            and any_has(text, ["rehabilitation", "health", "monthly", "export"])
            and any_has(text, ["pain", "steps", "pain_level", "steps"])
            and any_has(text, ["Dr. Wang", "doctor", "review"])
            and _notion_has(env, [["rehabilitation", "health", "monthly"], ["pain", "pain_level"], ["steps"], ["Dr. Wang", "doctor"]])
            and count_hits(_sent_or_draft_text(env) + "\n" + text, [["Dr. Wang", "doctor"], ["rehabilitation", "health", "monthly"], ["pain", "steps"]]) == 3
        )
    except Exception:
        return False

CHECKS = [
    ("r31_health_month_export", r31_health_month_export, 2.0),
]
