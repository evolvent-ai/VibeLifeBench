from __future__ import annotations
from ._helpers import *


def s21_price_drop_no_override(env) -> bool:
    return (
        stage_ok(env, 21, "s21")
        and stage21_c_price_and_route_refresh(env)
        and listing_c_route_over_limit(env, "2026-07-29")
        and inbox_message_has(env, body_parts=["Clearwave Residence", "18:30"])
        and notion_has_any(env, ([C.LIST_C, "7350", "eliminated", C.LIST_H, "viewing window"], ["Hexi Qingyuan", "route hard constraint", "Clearwave Residence"]))
    )


CHECKS = [("s21_price_drop_no_override", s21_price_drop_no_override, 1.5)]
