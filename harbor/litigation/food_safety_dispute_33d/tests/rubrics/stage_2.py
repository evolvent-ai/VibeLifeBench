"""Stage 2: food-testing institution selection."""
from __future__ import annotations
from ._helpers import _stage_corpus, _notion_page_text
from .cross_stage import d_reads_inspect_roster, d_inspect_conflict_excluded, d_inspect_wrong_scope_excluded, d_inspect_no_cma_excluded, d_inspect_contingent_fee_excluded, d_inspect_over_budget_excluded, d_inspect_suspended_excluded, d_inspect_best_pick, d_inspect_budget_cap

def s2_precedent_citation(env) -> bool:
    text = _stage_corpus(env, 2)
    return any(k in text for k in ("case_f02", "no Chinese label", "imported food")) and any(k in text for k in ("refund plus tenfold compensation", "ten times the purchase price", "does not meet food safety standards", "holding"))

def s2_inspect_choice_in_notion(env) -> bool:
    text = _notion_page_text(env, "testing") or _notion_page_text(env, "food safety rights protection")
    return text is not None and any(k in text for k in ("testing", "JY-006", "Huizheng", "testing institution", "testing report", "testing fee", "CMA"))
CHECKS = [("d_reads_inspect_roster", d_reads_inspect_roster, 0.733), ("d_inspect_conflict_excluded", d_inspect_conflict_excluded, 1.099), ("d_inspect_wrong_scope_excluded", d_inspect_wrong_scope_excluded, 1.099), ("d_inspect_no_cma_excluded", d_inspect_no_cma_excluded, 1.099), ("d_inspect_contingent_fee_excluded", d_inspect_contingent_fee_excluded, 1.099), ("d_inspect_over_budget_excluded", d_inspect_over_budget_excluded, 1.099), ("d_inspect_suspended_excluded", d_inspect_suspended_excluded, 1.099), ("d_inspect_best_pick", d_inspect_best_pick, 1.099), ("d_inspect_budget_cap", d_inspect_budget_cap, 0.046)]
