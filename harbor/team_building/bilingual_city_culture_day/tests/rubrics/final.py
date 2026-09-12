from __future__ import annotations
from ._helpers import *


def final_review_or_handoff(env) -> bool:
    return (
        used_tool(env, 24, "notion")
        and final_review_written(env, stage=None)
        and draft_matches(env, "post-event review", "gu.ning", ["budget", "invoice", "vendor", "safety", "privacy", "unpaid", "SOP"], stage=None)
        and workspace_has(env, "POST_EVENT_REVIEW.md", ["budget", "invoice", "vendor evaluation", "safety", "privacy", "unpaid", "SOP"], 6, stage=None)
    )


def final_invoice_transaction_seen(env) -> bool:
    return (
        transaction_from_trace(env, 24, ["Yuexiu Companion Transport Services Co.", "charter transportation invoice"])
        and used_tool(env, 24, "notion")
        and workspace_has(env, "BUDGET_LEDGER.csv", ["transportation", "invoice", "1280000", "settled"], 3, stage=None)
    )


CHECKS = [("final_review_or_handoff", final_review_or_handoff, 1.5), ("final_invoice_transaction_seen", final_invoice_transaction_seen, 1.25)]
