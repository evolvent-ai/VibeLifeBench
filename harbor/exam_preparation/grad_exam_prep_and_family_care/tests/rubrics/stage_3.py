from __future__ import annotations
from ._helpers import *

def r09_medical_instruction_log(env) -> bool:
    try:
        return (
            _stage_trace_all(env, 3, [["email", "mail"], ["read_email", "search_emails", "get_emails"]])
            and _workspace_file_has(env, "HEALTH_LOG.md", [
                ["Dr. Wang", "doctor"],
                ["pain", "steps", "swelling"],
                ["follow-up", "11-28", "11 month28"],
            ])
            and _notion_has(env, [["Dr. Wang", "doctor"], ["pain", "steps", "swelling"], ["11-28", "11 month28"]])
            and _stage_reply_has(env, 3, [["pain", "steps", "swelling"], ["follow-up"]])
        )
    except Exception:
        return False

CHECKS = [
    ("r09_medical_instruction_log", r09_medical_instruction_log, 3.0),
]
