from __future__ import annotations
from ._helpers import *


def s16_child_deposit_terms_rechecked(env) -> bool:
    return (
        stage_listing_detail(env, 16, C.LIST_E)
        and tool_stage(env, 16, EMAIL, "search_emails", ["child-damage deposit"])
        and tool_stage_results_cover(env, 16, EMAIL, "search_emails", ["300"])
        and listing_e_child_deposit_risky(env)
        and inbox_message_has(env, body_parts=["3000", "refund conditions"], subject_parts=["South Creek Garden", "deposit"])
        and stage_notion_any(env, 16, ([C.LIST_E, "3000", "refund conditions"], ["South Creek Garden", "written clarification", "charges outside monthly rent"]))
        and notion_has_any(env, ([C.LIST_E, "3000", "refund conditions"], ["South Creek Garden", "child-damage deposit", "unclear"]))
    )


CHECKS = [("s16_child_deposit_terms_rechecked", s16_child_deposit_terms_rechecked, 2.0)]
