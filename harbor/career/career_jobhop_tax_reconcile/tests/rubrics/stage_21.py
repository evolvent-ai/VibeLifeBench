from . import _helpers as H


def final_handoff_is_populated(env):
    text = H.handoff(env)
    fields = H.fields_have_values(text, ("current_status", "completed_actions", "open_items", "authorization_boundary", "tax_evidence_ids", "job_evidence_ids", "next_review_date"))
    return fields and {"banking", "email", "job_board"} <= H.backend_trace_domains(env, text)


CHECKS = [("tax_s21_final_handoff_is_populated", final_handoff_is_populated, 3.0)]
