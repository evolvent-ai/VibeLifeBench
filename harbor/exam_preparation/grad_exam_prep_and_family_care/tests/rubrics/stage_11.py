from __future__ import annotations
from ._helpers import *

def r20_health_pull(env) -> bool:
    try:
        text = _agent_reply(env, 11) + "\n" + _trace_text(env, 11, 11) + "\n" + _health_text(env)
        return (
            _stage_trace_all(env, 11, [["health_tracker"], ["get_metrics", "list_health_alerts"]])
            and any_has(text, ["pain_level=7", "7/10", "108", "above_typical_range"])
            and any_has(text, ["pain", "swelling", "knee"])
            and _workspace_file_has(env, "HEALTH_LOG.md", [["pain_level=7", "7/10", "pain"], ["108", "steps"], ["Dr. Wang", "doctor", "follow-up visit"]])
            and _notion_has(env, [["pain_level=7", "7/10", "pain"], ["108", "steps"], ["contactDr. Wang", "Dr. Wang", "doctorevaluate"]])
        )
    except Exception:
        return False

def r21_email_doctor_pain(env) -> bool:
    try:
        text = _agent_reply(env, 11) + "\n" + _trace_text(env, 11, 11) + "\n" + _sent_or_draft_text(env) + "\n" + wfile(env, "HEALTH_LOG.md")
        return (
            _stage_trace_all(env, 11, [["email", "mail"], ["send_email", "reply_email", "save_draft"]])
            and any_has(text, ["Dr. Wang", "doctor_wang@hospital.test", "doctor"])
            and any_has(text, ["pain_level=7", "7/10", "pain", "swelling"])
            and any_has(text, ["cannot diagnose", "doctor judgment", "follow-up visit", "please evaluate", "consult"])
            and count_hits(_sent_or_draft_text(env), [["Dr. Wang", "doctor_wang@hospital.test", "doctor"], ["pain", "swelling"], ["7/10", "pain_level=7", "108"]]) == 3
        )
    except Exception:
        return False

CHECKS = [
    ("r20_health_pull", r20_health_pull, 4.0),
    ("r21_email_doctor_pain", r21_email_doctor_pain, 5.0),
]
