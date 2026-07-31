from ._helpers import trace_stage, text_stage


def s20_reinspection_refresh(env) -> bool:
    return trace_stage(env, 20) and text_stage(env, 20, [["reinspection", "复检"], ["schedule", "日程"], ["materials", "材料"], ["旧", "stale", "更新"]])


CHECKS = [
    ("s20_reinspection_refresh", s20_reinspection_refresh, 1.3),
]
