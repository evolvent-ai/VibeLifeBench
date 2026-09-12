"""Stage rubric - explicit CHECKS literal."""
from __future__ import annotations

from .stage_specs import run_check as _run

def s7_cross_category_comparison(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s7_cross_category_comparison", env)

def s7_multi_source_comparison_tools(env) -> bool:
    evidence_hint = "tool_call _call_mock workspace_file_text review_platform ecommerce banking email calendar notification_hub notion content_platform backend"
    _ = evidence_hint
    return _run("s7_multi_source_comparison_tools", env)


CHECKS = [
    ("s7_cross_category_comparison", s7_cross_category_comparison, 0.5),
    ("s7_multi_source_comparison_tools", s7_multi_source_comparison_tools, 0.5),
]
