from __future__ import annotations
from ._helpers import *


def s17_child_deposit_risk(env) -> bool:
    return (
        stage_ok(env, 17, "s17")
        and listing_e_child_deposit_risky(env)
        and inbox_message_has(env, body_parts=["3000", "child-damage deposit", "refund conditions"], subject_parts=["South Creek Garden", "deposit"], message_id="<thread-e-deposit@example.invalid>")
        and notion_has_any(env, ([C.LIST_E, "3000", "refund", "risk"], ["South Creek Garden", "child-damage deposit", "pending written confirmation"]))
    )


def s17_split_confirmation(env) -> bool:
    return (
        safe_stage17_split_record(env)
        and notion_has_any(env, (["viewing time", "deposit", "documents", "confirm separately"], ["appointment", "fee risk", "do not send by default"]))
        and non_h_viewings_absent(env)
    )


CHECKS = [
    ("s17_child_deposit_risk", s17_child_deposit_risk, 2.0),
    ("s17_split_confirmation", s17_split_confirmation, 2.0),
]
