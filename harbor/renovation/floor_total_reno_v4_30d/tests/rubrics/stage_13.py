"""Stage 13 — reconcile flooring money states without counting promises as cash."""
from .shared import _helpers as R
from .shared import _helpers as H

def s13_budget(env):
    return H.claim(env, "rejected", 2418000) and H.duplicate_tx(env) and H.no_duplicate_dispute(env) and (R.artifact_fields_set(env, "/workspace/budget.md", ("currency", "paid_minor", "refund_pending_minor", "refunded_minor", "holdback_minor", "resale_received_minor", "source_objects", "as_of_stage")) and R.artifact_has(env, "/workspace/budget.md", (("construction payment",), ("retainage",), ("leveling", "rework"), ("surplus materials",), ("pending review", "pending"), ("posted", "posted"))))

CHECKS = [("s13_budget", s13_budget, 3.0)]
