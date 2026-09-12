from __future__ import annotations
from ._helpers import *


def s12_backup_and_lead_ranked(env) -> bool:
    return (
        stage_ok(env, 12, "s12")
        and listing_d_backup_backend_ready(env)
        and listing_e_conditional_backend_ready(env)
        and b_detour_backend_ready(env)
        and notion_has_any(env, ([C.LIST_D, "transportation backup", C.LIST_E, "conditional candidate", C.LIST_B, "eliminated"], ["Yunanli", "backup", "South Creek Garden", "condition", "Mingcheng Court", "83"]))
    )


CHECKS = [("s12_backup_and_lead_ranked", s12_backup_and_lead_ranked, 1.5)]
