from __future__ import annotations
from ._helpers import *


def s24_inspection_classified(env) -> bool:
    return (
        stage24_inspection_record_exact(env)
        and notion_has_any(env, ([C.LIST_H, "elevator operational", "hallway", "bedroom", "night noise", "unconfirmed"], ["Clearwave Residence", "on-site observation", "second listening", "do not sign"]))
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [("s24_inspection_classified", s24_inspection_classified, 1.25)]
