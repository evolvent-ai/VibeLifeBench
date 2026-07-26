"""Stage 12 — 将后端生成的 canonical application ID 原位同步到唯一看板行。"""
from __future__ import annotations

from ._helpers import canonical_applications, record_text, stage_call_matches

USER_ID = "usr_gao_kai"


def s12_status_synced(env) -> bool:
    if not stage_call_matches(env, 12, "list_applications", {"user_id": USER_ID}):
        return False
    apps = canonical_applications(env)
    if len(apps) < 2:
        return False
    record = record_text(env, "job_tracker.md")
    for app in apps:
        app_id = str(app.get("application_id") or "").lower()
        job_id = str(app.get("job_id") or "").lower()
        status = str(app.get("status") or "").lower()
        updated = str(app.get("updated_at") or "").lower()
        if not app_id or record.count(app_id) != 1:
            return False
        if not all(value and value in record for value in (job_id, status, updated)):
            return False
    return True


CHECKS = [("s12_status_synced", s12_status_synced, 2.0)]
