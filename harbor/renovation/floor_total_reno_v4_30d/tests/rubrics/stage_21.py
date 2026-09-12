"""Stage 21 — prepare an owner/evidence/next-step flooring closeout checklist."""
from .shared import _helpers as R
from .shared import _helpers as H

def s21_checklist(env):
    return H.final_core(env) and (R.artifact_has(env, "/workspace/order_tracker.md", (("contractor", "contract"), ("pressure test",), ("leveling",), ("moisture content",), ("flatness",), ("expansion joints",), ("credit card",), ("retainage",), ("surplus materials",), ("evidence", "evidence"), ("next action", "next_action"), ("responsibility", "owner"))) and R.heartbeat_has_stage(env, 21))

CHECKS = [("s21_checklist", s21_checklist, 2.0)]
