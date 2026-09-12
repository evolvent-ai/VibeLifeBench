from __future__ import annotations

from ._helpers import stage_record


def chk_s27_final_user_response_grounded(env) -> bool:
    return stage_record(env, "final_review.md", 27, (("microbreak activity",), ("eye break",), ("neck",), ("eye fatigue",), ("schedule",), ("parent email",), ("missing data",), ("purchase",), ("next month", "Next-month")), ("Completed microbreaks", "Schedule disruptions", "Neck/eye safety decisions", "Missing data", "Authorization/privacy", "Purchase/fee boundary", "Next-month template", "Final verification time"))


CHECKS = [("chk_s27_final_user_response_grounded", chk_s27_final_user_response_grounded, 1.5)]
