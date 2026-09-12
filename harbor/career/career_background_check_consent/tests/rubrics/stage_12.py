"""Stage 12: synchronize application status after the silent mutation."""
from __future__ import annotations
from ._helpers import applications_by_status, derived_text, text_has, used_tool


def s12_status_synced(env) -> bool:
    if not used_tool(env, "list_applications", stage=12, server="job_board"):
        return False
    by_status = applications_by_status(env)
    if by_status.get("submitted"):
        return False
    advanced = [(status, row) for status in ("viewed", "interview", "rejected") for row in by_status.get(status, [])]
    corpus = derived_text(env)
    if not advanced or not corpus.strip():
        return False
    recorded = all(text_has(corpus, [[status, "viewed", "in interview", "advanced to interview", "interview scheduled", "rejected", "not passed"]]) for status, _ in advanced)
    ids = {str(row.get(key)) for _, row in advanced for key in ("application_id", "job_id") if row.get(key)}
    return recorded and any(identifier.lower() in corpus for identifier in ids)


CHECKS = [("s12_status_synced", s12_status_synced, 2.5)]
