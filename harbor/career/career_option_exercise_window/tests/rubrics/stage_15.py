from . import _helpers as H

def interview_prep_is_job_specific(env):
    return H.pipeline_has_qingyuan_job(env) and H.has_terms(H.pipeline(env), ("job_id",), ("platform reliability",), ("distributed",), ("next_follow_up", "next step"))

CHECKS = [("opt_s15_interview_prep_is_job_specific", interview_prep_is_job_specific, 1.5)]
