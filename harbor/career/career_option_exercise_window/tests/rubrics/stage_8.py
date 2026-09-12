from . import _helpers as H

def direct_hire_candidates_with_noncompete_review_recorded(env):
    text = H.pipeline(env)
    return H.table_has_data(text) and H.pipeline_jobs_backed(env, minimum=2) and H.pipeline_has_eligible_and_near_miss(env) and H.has_terms(text, ("Shanghai",), ("direct_full_time", "direct-hire"), ("job_id",), ("noncompete",), ("uncompensated", "requires clarification", "compensation gap"))

CHECKS = [("opt_s08_direct_hire_candidates_with_noncompete_review_recorded", direct_hire_candidates_with_noncompete_review_recorded, 1.5)]
