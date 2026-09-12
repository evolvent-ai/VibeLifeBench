from . import _helpers as H

def final_handoff_is_populated(env):
    return H.fields_have_values(H.handoff(env), ("current_status", "completed_actions", "open_items", "authorization_boundary", "equity_evidence_ids", "job_evidence_ids", "next_review_date"))

CHECKS = [("opt_s21_final_handoff_is_populated", final_handoff_is_populated, 3.0)]
