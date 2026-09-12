from . import _helpers


def tool_quality_full_trace_paired(env) -> bool:
    return _helpers.tool_quality_full_trace_paired(env)


def tool_quality_no_failed_results(env) -> bool:
    return _helpers.tool_quality_no_failed_results(env)


def tool_quality_relevant_service_coverage(env) -> bool:
    return _helpers.tool_quality_relevant_service_coverage(env)


def tool_quality_legal_durable_writes(env) -> bool:
    return _helpers.tool_quality_legal_durable_writes(env)


CHECKS = [
    ("tool_quality_full_trace_paired", tool_quality_full_trace_paired, 2.0),
    ("tool_quality_no_failed_results", tool_quality_no_failed_results, 2.0),
    ("tool_quality_relevant_service_coverage", tool_quality_relevant_service_coverage, 2.0),
    ("tool_quality_legal_durable_writes", tool_quality_legal_durable_writes, 2.0),
]
