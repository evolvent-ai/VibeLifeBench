from ._stage_checks import run_stage


def s3_docs_email_ingested(env):
    return run_stage(env, 3)


CHECKS = [("s3_docs_email_ingested", s3_docs_email_ingested, 2.0)]
