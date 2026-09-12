from ._stage_checks import run_stage


def s23_receipts_return_closeout(env):
    return run_stage(env, 23)


CHECKS = [("s23_receipts_return_closeout", s23_receipts_return_closeout, 3.0)]
