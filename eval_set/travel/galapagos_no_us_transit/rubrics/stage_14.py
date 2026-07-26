from ._stage_checks import run_stage


def s14_permit_fee_split(env):
    return run_stage(env, 14)


CHECKS = [("s14_permit_fee_split", s14_permit_fee_split, 2.0)]
