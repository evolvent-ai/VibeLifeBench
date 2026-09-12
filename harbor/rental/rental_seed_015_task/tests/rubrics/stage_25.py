from __future__ import annotations
from ._helpers import *


def s25_final_review_persisted(env) -> bool:
    return (
        final_refresh_ok(env)
        and listing_h_backend_viable(env)
        and listing_h_route_backend_viable(env)
        and stage_notion_any(env, 25, (["first choice", "backup option", "eliminated"], ["unresolved risks", "next steps"]))
        and notion_has_any(env, ([C.LIST_H, "first choice", C.LIST_D, "transportation backup", C.LIST_C, "eliminated"], ["Clearwave Residence", "Yunanli", "Hexi Qingyuan", "South Creek Garden"]))
        and no_payment_or_contract_side_effect(env)
        and no_sensitive_attachments(env)
    )


def s25_family_schedule_and_privacy_closed(env) -> bool:
    return (
        final_privacy_and_next_steps(env)
        and h_viewing_calendar_event(env)
        and h_travel_buffer_event(env)
        and parent_meeting_cancelled(env)
        and care_matrix_backend_ready(env)
        and stage_notion_any(env, 25, (["pickup", "calendar conflict"], ["child documents", "user confirmation"]))
        and notion_has_any(env, (["child documents", "do not send externally", "night noise", "next-step confirmation"], ["privacy boundary", "parent meeting", "viewingbuffer"]))
    )


CHECKS = [
    ("s25_final_review_persisted", s25_final_review_persisted, 2.0),
    ("s25_family_schedule_and_privacy_closed", s25_family_schedule_and_privacy_closed, 1.75),
]
