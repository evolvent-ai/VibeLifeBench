from . import _helpers as H


def direct_hire_candidates_recorded(env):
    text = H.pipeline(env)
    jobs = H.direct_hire_pipeline_jobs(env)
    return len({str(job.get("job_id")) for job in jobs}) >= 2 and H.has_terms(text, ("Shanghai",), ("direct_full_time", "permanent employee", "company direct hire"), ("job_id",))


CHECKS = [("tax_s08_direct_hire_candidates_recorded", direct_hire_candidates_recorded, 1.5)]
