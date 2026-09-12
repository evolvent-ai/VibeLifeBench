from __future__ import annotations
from ._helpers import *


def s24_final_page(env) -> bool:
    return (
        used_tool(env, 24, "notion")
        and final_review_written(env, stage=24)
        and draft_matches(env, "post-event review", "gu.ning", ["budget", "invoice", "vendor", "safety", "privacy", "unpaid", "SOP"], stage=24)
        and workspace_has(env, "POST_EVENT_REVIEW.md", ["budget", "invoice", "vendor evaluation", "safety", "privacy", "unpaid", "SOP"], 6, stage=24)
    )


CHECKS = [("s24_final_page", s24_final_page, 1.75)]
