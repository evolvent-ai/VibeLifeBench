from ._helpers import *


def r038_check_009_review_noise(env) -> bool:
    return bool(
        tool_stage_result_has(env, 4, 'review_platform', None, result_parts=['rv_river_noise', 'renovation noise'])
        and tool_stage_result_has(env, 4, 'review_platform', None, result_parts=['rv_maple_quiet', 'traffic noise'])
        and state_evidence(env, 4, [C.A, 'noise'], ['risk_log.md', 'child_safety_checklist.md'])
        and state_evidence(env, 4, [C.B, 'noise'], ['risk_log.md', 'child_safety_checklist.md'])
    )


def r038_check_010_review_voc_mold(env) -> bool:
    return bool(
        tool_stage_result_has(env, 4, 'review_platform', None, result_parts=['rv_river_noise', 'newly renovated', 'odor'])
        and state_evidence(env, 4, [C.A, 'newly renovated'], ['risk_log.md', 'child_safety_checklist.md'])
        and (
            state_evidence(env, 4, [C.A, 'odor', 'on-site'], ['risk_log.md', 'child_safety_checklist.md'])
            or state_evidence(env, 4, [C.A, 'formaldehyde', 'verification'], ['risk_log.md', 'child_safety_checklist.md'])
        )
    )


def r038_check_011_child_safety_checklist(env) -> bool:
    return bool(
        tool_stage_result_has(env, 4, 'review_platform', None, result_parts=['rv_maple_child', 'fire safety', 'window lock'])
        and tool_stage_result_has(env, 4, 'review_platform', None, result_parts=['rv_sunbay_guardrail', 'railing', 'child'])
        and state_evidence(env, 4, [C.B, 'window lock', 'fire safety'], ['child_safety_checklist.md', 'risk_log.md'])
        and state_evidence(env, 4, [C.C, 'railing', 'on-site'], ['child_safety_checklist.md', 'risk_log.md'])
    )


CHECKS = [
    ("r038_check_009_review_noise", r038_check_009_review_noise, 1.25),
    ("r038_check_010_review_voc_mold", r038_check_010_review_voc_mold, 2.0),
    ("r038_check_011_child_safety_checklist", r038_check_011_child_safety_checklist, 1.75),
]
