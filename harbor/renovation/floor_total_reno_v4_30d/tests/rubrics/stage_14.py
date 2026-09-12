"""Stage 14 — preserve the under-review thermostat dispute state."""
from .shared import _helpers as R
from .shared import _helpers as H

def s14_servers(env):
    return H.dispute(env, "under_review") and (R.trace_has_success(env, 14, ("credit_card",), min_count=1) and R.artifact_active(env, "/workspace/evidence_log.md"))

def s14_result(env):
    return R.backend_and_artifact(env, "credit_card", "SELECT COUNT(*) FROM disputes WHERE dispute_id=? AND tx_id=? AND status='under_review'", ("disp_qflr_01", "tx_qflr_dup"), "/workspace/budget.md", (("disp_qflr_01",), ("under_review", "under review"), ("not reversed", "not refunded")))

def s14_no_bad(env):
    return H.dispute(env, "under_review") and (R.artifact_has(env, "/workspace/budget.md", (("under_review", "under review"), ("not reversed", "not refunded"))) and R.no_unqualified_phrase(env, ("already refunded", "refund posted", "no repayment required")))

CHECKS = [("s14_servers", s14_servers, 0.5), ("s14_result", s14_result, 3.0), ("s14_no_bad", s14_no_bad, 0.5)]
