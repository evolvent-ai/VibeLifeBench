from __future__ import annotations
from ._helpers import *


def s24_final_page(env) -> bool:
    wrote = used_tool(env, 24, "notion", "API-post-page") or used_tool(env, 24, "notion", "API-patch-block-children") or used_tool(env, 24, "notion", "API-update-a-block")
    return wrote and final_review_written(env) and workspace_file_has(env, "POST_EVENT_REVIEW.md", [["budget"], ["invoice"], ["supplier"], ["safety", "privacy"], ["unpaid", "pending confirmation"], ["SOP", "remediation"]])


CHECKS = [("s24_final_page", s24_final_page, 2.5)]
