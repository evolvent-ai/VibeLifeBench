from . import _helpers as H


def privacy_safe_direct_hire_candidates_recorded(env):
    text = H.pipeline(env)
    semantics = H.has_terms(text, ("Shanghai",), ("direct_full_time", "direct full-time", "direct employment"), ("privacy_requirements", "privacy"), ("job_id",))
    return bool(H.pipeline_rows_are_complete(env, min_rows=2) and semantics and H.pipeline_jobs_are_real_and_eligible(env, min_jobs=2))


CHECKS = [("med_s08_privacy_safe_direct_hire_candidates_recorded", privacy_safe_direct_hire_candidates_recorded, 1.5)]
