from . import _helpers as H


def interview_prep_is_job_specific(env):
    return H.interview_job_is_reflected(env)


CHECKS = [("tax_s15_interview_prep_is_job_specific", interview_prep_is_job_specific, 1.5)]
