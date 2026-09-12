"""Stage 4 — measure commute with maps; reject over-commute candidates."""
from __future__ import annotations
from ._helpers import agent_used_tool, file_has, has_any, has_regex, stage_corpus, tool_call_arg_has_any

def s4_transit_measured(env) -> bool:
    measured = agent_used_tool(env, 'maps', 'get_transit', stage=4)
    spoke = has_regex(stage_corpus(env, 4), '(commute|Software Avenue|metro|travel time|report to work).{0,14}\\d+\\s*(minutes|min|minutes|seconds|s)')
    return measured and spoke

def s4_reject_over_commute(env) -> bool:
    text = stage_corpus(env, 4)
    if not text.strip():
        return False
    explicit = has_any(text, ['over 40', 'over 40', '>40', 'over commute limit', 'commute over', 'measured over', 'exclude for excessive time', 'commute fails limit', 'commute exceeds limit'])
    pattern = has_regex(text, '(exclude|exclude|exclude|exclude).{0,16}(commute|minutes)')
    durable = file_has(env, 'candidates.md', ['commute', 'exclude'], minimum=2) or file_has(env, 'audit_journal.md', ['commute', '40'], minimum=2)
    return (explicit or pattern) and durable

def s4_target_and_decoy_transit_params(env) -> bool:
    calls_target = tool_call_arg_has_any(env, 'maps', 'get_transit', ['pl_corr_08', 'Mingfa Riverside New City'], stage=4)
    calls_over = tool_call_arg_has_any(env, 'maps', 'get_transit', ['pl_corr_02', 'Qiaobei Waterfront'], stage=4)
    dest_ok = tool_call_arg_has_any(env, 'maps', 'get_transit', ['pl_company', 'Software Avenue'], stage=4)
    durable = file_has(env, 'candidates.md', ['Mingfa', 'Qiaobei', '42', '21'], minimum=3) or file_has(env, 'audit_journal.md', ['Mingfa', 'Qiaobei', 'commute'], minimum=3)
    return calls_target and calls_over and dest_ok and durable
CHECKS = [('s4_transit_measured', s4_transit_measured, 0.1863799283154122), ('s4_reject_over_commute', s4_reject_over_commute, 1.4910394265232976), ('s4_target_and_decoy_transit_params', s4_target_and_decoy_transit_params, 3.727598566308244)]
