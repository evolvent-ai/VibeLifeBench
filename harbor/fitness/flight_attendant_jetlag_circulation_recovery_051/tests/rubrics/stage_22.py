from __future__ import annotations

from ._helpers import calendar_has, no_duplicate_sock_order, order_delayed, stage_record


def chk_s22_order_delay_alt(env) -> bool:
    budget = stage_record(
        env,
        "equipment_budget.md",
        22,
        (("delayed", "shipped"), ("September 27", "9/27", "0927"), ("no duplicate purchase", "do not buy again")),
        ("Order/status", "Verified at"),
    )
    calendar = stage_record(env, "calendar_change_log.md", 22, (("equipment-free",), ("recovery", "alternative")), ("New window", "Backend verification"))
    return budget and calendar and order_delayed(env) and no_duplicate_sock_order(env) and calendar_has(env, (("equipment-free", "bodyweight", "recovery"),))


CHECKS = [("chk_s22_order_delay_alt", chk_s22_order_delay_alt, 1.75)]
