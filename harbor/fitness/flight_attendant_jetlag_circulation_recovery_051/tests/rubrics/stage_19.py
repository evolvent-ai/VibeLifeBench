from __future__ import annotations

from ._helpers import health_has, stage_record


def chk_s19_work_steps_not_training(env) -> bool:
    source = health_has(env, ("steps", "score"), (("longhaul_duty_steps",), ("not_training_completion=true",), ("fatigue=7/10",)))
    recorded = stage_record(
        env,
        "stage_progress.md",
        19,
        (("16840", "steps"), ("duty", "standing", "transfers"), ("training completion",), ("separate", "not counted", "not combined")),
        ("Facts read", "Decision", "Action/result"),
    )
    return source and recorded


CHECKS = [("chk_s19_work_steps_not_training", chk_s19_work_steps_not_training, 1.25)]
