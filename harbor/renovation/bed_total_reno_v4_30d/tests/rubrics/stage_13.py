"""Stage 13 — reconcile distinct money states without treating promises as cash."""
from .shared import _helpers as R
from .shared import _backend as B


def s13_budget(env):
    return B.midpoint_sources(env) and R.artifact_fields_set(env, "/workspace/budget.md", ("currency", "paid_minor", "refund_pending_minor", "refunded_minor", "holdback_minor", "resale_received_minor", "source_objects", "as_of_stage")) and R.artifact_has(env, "/workspace/budget.md", (("construction payment", "project payment"), ("retainage",), ("rework",), ("surplus materials",), ("pending verification", "pending"), ("funds posting", "posted")))


CHECKS = [("s13_budget", s13_budget, 3.0)]
