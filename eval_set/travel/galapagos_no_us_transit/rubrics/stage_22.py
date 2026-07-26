from ._stage_checks import run_stage


def s22_midtrip_schedule_weather(env):
    return run_stage(env, 22)


CHECKS = [("s22_midtrip_schedule_weather", s22_midtrip_schedule_weather, 2.0)]
