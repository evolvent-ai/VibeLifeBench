from ._helpers import NO_PROMISE_TERMS, trace_stage, text_stage


def s19_neighbor_no_false_promise(env) -> bool:
    return trace_stage(env, 19) and text_stage(env, 19, [["neighbor", "邻居"], ["parking", "停车"], ["access", "通行"], ["rent", "出租"], NO_PROMISE_TERMS])


CHECKS = [
    ("s19_neighbor_no_false_promise", s19_neighbor_no_false_promise, 1.4),
]
