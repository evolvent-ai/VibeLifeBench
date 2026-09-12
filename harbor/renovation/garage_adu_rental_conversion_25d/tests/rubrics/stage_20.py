from ._helpers import trace_stage, text_stage


def s20_reinspection_refresh(env) -> bool:
    return trace_stage(env, 20) and text_stage(
        env,
        20,
        [
            ["reinspection", "re-inspection"],
            ["schedule", "appointment", "slot"],
            ["materials", "stock", "supplies"],
            ["stale", "old dates", "superseded", "refreshed", "updated"],
        ],
    )


CHECKS = [
    ("s20_reinspection_refresh", s20_reinspection_refresh, 1.3),
]
