from ._stage_checks import run_stage


def s15_transfer_mutation_retime(env):
    return run_stage(env, 15)


CHECKS = [("s15_transfer_mutation_retime", s15_transfer_mutation_retime, 2.0)]
