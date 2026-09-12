"""Stage 19 — use real Offer application ID continue maintaining two tracks."""
from __future__ import annotations

from ._helpers import record_text, text_has, unique_application_for_job


def s19_maintains_state(env) -> bool:
    app = unique_application_for_job(env, "job_gk_0001", {"offer"})
    if not app:
        return False
    app_id = str(app.get("application_id") or "").lower()
    record = record_text(env, "decision_log.md")
    return text_has(record, [
        ["equity trackstatus"], ["tx_gk_severance"], ["shortfall 97000"],
        ["re-employment trackstatus"], [app_id], ["offer"],
        ["unresolved"], ["owner"], ["follow-up"],
    ]) and record.count("owner") >= 2 and record.count("next review point") >= 2


CHECKS = [("s19_maintains_state", s19_maintains_state, 1.0)]
