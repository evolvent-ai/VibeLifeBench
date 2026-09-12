from __future__ import annotations

from ._helpers import _workspace_file_text, text_has


def s2_budget_cap_recorded(env) -> bool:
    text = _workspace_file_text(env, "trip_plan.md") + "\n" + _workspace_file_text(env, "budget_ledger.md")
    dates = text_has(text, [["2026-10-12", "October 12"], ["2026-10-19", "October 19"]])
    cap = text_has(text, [["42000", "42,000", "42,000"], ["budget cap", "budget cap", "budget cap"]])
    planning_state = text_has(text, [["tentative", "planning", "tentative", "planning"], ["unpaid", "unpaid", "not paid", "unpaid"]])
    return bool(dates and cap and planning_state)


CHECKS = [("s2_budget_cap_recorded", s2_budget_cap_recorded, 2.0)]
