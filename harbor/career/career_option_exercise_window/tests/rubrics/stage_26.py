from . import _helpers as H

def final_records_are_traceable_and_state_separated(env):
    text = H.corpus(env)
    return H.traceability_is_backed(env) and H.has_terms(text, ("G-2021-0427",), ("20210427-grant",), ("2026-07-16",), ("tx_gk_",), ("job_",), ("valuation",), ("decision_status",), ("not submitted", "not executed"))

CHECKS = [("opt_s26_final_records_are_traceable_and_state_separated", final_records_are_traceable_and_state_separated, 2.5)]
