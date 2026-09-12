from . import _helpers as H


def final_privacy_chain_answers_six_questions(env):
    text = H.privacy_log(env)
    semantics = H.has_terms(text, ("requester", "who requested"), ("data_category", "what was requested"), ("purpose", "why"), ("authorized_recipient", "authorized recipient"), ("actual_disclosure", "actual sending"), ("next_action", "next step"))
    return bool(H.privacy_log_rows_are_complete(env, min_rows=8) and semantics and H.all_trace_references_real(env))


CHECKS = [("med_s25_final_privacy_chain_answers_six_questions", final_privacy_chain_answers_six_questions, 2.5)]
