from ._helpers import *

def r038_check_002_listing_search(env) -> bool:
    return bool(
        lp_stage(env, 1, 'search', ['rent', '1100000'])
        and lp_stage(env, 1, 'search', ['min_rooms'])
        and stage_results_mention_candidates(env, 1, [C.A, C.B, C.C, C.ORANGE, C.GREEN, C.LAKE], min_count=3)
    )

def r038_check_003_shortlist_fields(env) -> bool:
    return bool(
        stage_results_mention_candidates(env, 1, [C.A, C.B, C.C, C.ORANGE, C.GREEN, C.LAKE], min_count=3)
        and workspace_has(env, [C.A, 'rent_minor', '1048000', 'available_from', '2026-08-12'], ['rental_tracker.md'])
        and workspace_has(env, [C.B, 'rent_minor', '1060000', 'property_fee_minor', '32000'], ['rental_tracker.md', 'budget_ledger.md'])
        and workspace_has(env, [C.C, 'risk', 'railing'], ['rental_tracker.md', 'risk_log.md'])
    )

def r038_check_004_filter_non_two_bedroom(env) -> bool:
    tracker = workspace_file(env, 'rental_tracker.md').lower()
    # A negated note such as "one-bedroom is not first choice" is evidence
    # that the filter was applied. Reject only an affirmative selection.
    one_bedroom_selected = False
    for line in tracker.splitlines():
        if not re.search(r'(?:one-bedroom|1b)', line) or not re.search(r'(?:first choice|preferred)', line):
            continue
        if re.search(r'(?:first choice|preferred)\s*(?:is|:)?\s*not\s+(?:a\s+)?(?:one-bedroom|1b)', line):
            continue
        if re.search(r'(?:one-bedroom|1b)\s*(?:is|as)?\s*not\s+(?:the\s+)?(?:first choice|preferred)', line):
            continue
        one_bedroom_selected = True
        break
    return bool(
        lp_stage(env, 1, 'search', ['min_rooms'])
        and stage_results_mention_candidates(env, 1, [C.A, C.B, C.C, C.ORANGE, C.GREEN, C.LAKE], min_count=3)
        and workspace_has(env, ['rooms', '2', C.A, C.B], ['rental_tracker.md'])
        and not one_bedroom_selected
    )

CHECKS = [
    ("r038_check_002_listing_search", r038_check_002_listing_search, 1.5),
    ("r038_check_003_shortlist_fields", r038_check_003_shortlist_fields, 1.5),
    ("r038_check_004_filter_non_two_bedroom", r038_check_004_filter_non_two_bedroom, 1.25),
]
