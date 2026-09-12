"""Stage 4: record the HR proposal and health-information request."""
from __future__ import annotations

from ._helpers import derived_text, norm_num, stage_write_used, text_has, trace_result_text, used_tool


def s4_plan_logged(env) -> bool:
    if not (used_tool(env, "read_email", stage=4) or used_tool(env, "get_email", stage=4)):
        return False
    evidence = trace_result_text(env, 4, "email")
    source_bound = text_has(evidence, [
        ["<20260615-plan@liyaobio.com>", "severance proposal and health-information request"],
        ["205400"], ["2026-06-22"], ["health-information", "medical", "history", "physical-examination", "records"],
    ])
    raw = derived_text(env)
    corpus = norm_num(raw)
    recorded = "205400" in corpus and "2026-06-22" in raw and text_has(raw, [["proposal"], ["health-information", "medical", "history", "physical"]])
    return source_bound and stage_write_used(env, 4) and recorded


CHECKS = [("s4_plan_logged", s4_plan_logged, 4.0)]
