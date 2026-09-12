from ._helpers import *


def s5_legal_sources_saved(env):
    return (
        legal_research_tool_used_through(env, 5)
        and legal_detail_tool_used_through(env, 5)
        and legal_backend_has_core_sources(env)
        and len(saved_legal_cases(env)) >= 1
    )


def s5_three_properties_scaffold(env):
    return (
        legal_research_tool_used_through(env, 5)
        and legal_backend_has_core_sources(env)
        and doc_value(env, 'evidence_three_properties.json', 'has_authenticity', True)
        and doc_value(env, 'evidence_three_properties.json', 'has_relevance', True)
        and doc_value(env, 'evidence_three_properties.json', 'has_legality_privacy', True)
    )


CHECKS = [('s5_legal_sources_saved', s5_legal_sources_saved, 1.75), ('s5_three_properties_scaffold', s5_three_properties_scaffold, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
