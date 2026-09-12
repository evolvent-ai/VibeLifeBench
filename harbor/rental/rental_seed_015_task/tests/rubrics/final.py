from __future__ import annotations
from ._helpers import *


def final_primary_h_or_valid_d(env) -> bool:
    return final_h_calendar_and_backend(env) and notion_has_any(env, ([C.LIST_H, "first choice", C.LIST_D, "backup"], ["Clearwave Residence", "Yunanli", "first choice", "transportation backup"])) and no_payment_or_contract_side_effect(env)


def final_backup_and_eliminations(env) -> bool:
    return final_eliminations_backend(env) and notion_has_any(env, ([C.LIST_B, "83", C.LIST_C, "route", C.LIST_E, "deposit"], ["Mingcheng Court", "Hexi Qingyuan", "South Creek Garden", "eliminated"])) and no_payment_or_contract_side_effect(env)


def final_routes_conflicts_privacy_next_steps(env) -> bool:
    return final_privacy_and_next_steps(env) and final_h_calendar_and_backend(env) and care_matrix_backend_ready(env) and notion_has_any(env, (["morning and evening transportation chain", "calendar conflict", "child documents", "unresolved risks", "next steps"], ["75", "parent meeting", "do not send externally", "night noise"]))


CHECKS = [
    ("final_primary_h_or_valid_d", final_primary_h_or_valid_d, 1.75),
    ("final_backup_and_eliminations", final_backup_and_eliminations, 1.75),
    ("final_routes_conflicts_privacy_next_steps", final_routes_conflicts_privacy_next_steps, 2.0),
]
