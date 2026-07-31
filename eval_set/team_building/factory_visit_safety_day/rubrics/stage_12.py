from __future__ import annotations
from ._helpers import *


def s12_driver_route_rechecked(env) -> bool:
    route = used_tool_with_value(env, 12, "maps", "directions", ["pl_sh_office", "pl_jx_factory"]) or used_tool_with_value(env, 12, "maps", "get_traffic_estimate", ["上海", "嘉兴"])
    return route and used_tool(env, 12, "email", "search_emails") and durable_has(env, [["司机"], ["资质", "补件"], ["复核", "替换", "备车"]])


def s12_no_final_notice(env) -> bool:
    drafted = used_tool(env, 12, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["司机", "资质"]],
        recipient_terms=["wei.ran"],
        body_groups=[["司机"], ["待核验", "补件", "未完成"], ["暂不", "不要", "未最终"]],
    )
    sent = "\n".join(flat(row) for row in sent_emails(env)).lower()
    return drafted and not ("最终通知" in sent and "工厂参访" in sent)


CHECKS = [("s12_driver_route_rechecked", s12_driver_route_rechecked, 1.25), ("s12_no_final_notice", s12_no_final_notice, 0.75)]
