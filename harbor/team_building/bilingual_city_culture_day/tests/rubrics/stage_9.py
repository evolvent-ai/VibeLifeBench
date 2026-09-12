from __future__ import annotations
from ._helpers import *


def s9_shortlist_draft(env) -> bool:
    return (
        used_tool(env, 9, "email", "save_draft")
        and draft_matches(env, "primary and backup plans", "gu.ning", ["primary plan", "backup", "risk", "pending confirmation", "do not pay"], stage=9)
        and workspace_has(env, "CITY_CULTURE_PLAN.json", ["primary plan", "backup", "pending confirmation"], 3, stage=9)
        and workspace_has(env, "AUTH_LOG.json", ["do not pay", "do not sign", "do not send final"], 2, stage=9)
    )


CHECKS = [("s9_shortlist_draft", s9_shortlist_draft, 1.5)]
