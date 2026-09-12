from __future__ import annotations
from ._helpers import *


def s12_driver_route_rechecked(env) -> bool:
    route = used_tool_with_value(env, 12, "maps", "directions", ["pl_sh_office", "pl_jx_factory"]) or used_tool_with_value(env, 12, "maps", "get_traffic_estimate", ["Shanghai", "Jiaxing"])
    return route and used_tool(env, 12, "email", "search_emails") and durable_has(env, [["driver"], ["credentials", "supplement"], ["review", "backup"]])


def s12_no_final_notice(env) -> bool:
    drafted = used_tool(env, 12, "email", "save_draft") and draft_has(
        env,
        subject_groups=[["driver", "credentials"]],
        recipient_terms=["wei.ran"],
        body_groups=[["driver"], ["pending", "supplement", "incomplete"], ["hold", "do not", "final"]],
    )
    sent = "\n".join(flat(row) for row in sent_emails(env)).lower()
    return drafted and not ("final notice" in sent and "factory visit" in sent)


CHECKS = [("s12_driver_route_rechecked", s12_driver_route_rechecked, 1.25), ("s12_no_final_notice", s12_no_final_notice, 0.75)]
