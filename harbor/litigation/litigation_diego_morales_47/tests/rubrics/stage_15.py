from ._helpers import *


def s15_privacy_rule_added(env):
    return (
        tool_used(env, 'legal_search', 'search_statutes', stage=15)
        and legal_article_exists(env, 'art_privacy_min_009', 'minimum')
        and record_has(env, 'evidence_three_properties.json', 'legal_sources', 'article_id', 'art_privacy_min_009')
    )


def s15_electronic_data_rule_added(env):
    return (
        legal_article_exists(env, 'art_electronic_data_021', 'electronic data')
        and record_has(env, 'evidence_three_properties.json', 'legal_sources', 'article_id', 'art_electronic_data_021')
        and len(saved_legal_cases(env)) >= 2
    )


CHECKS = [('s15_privacy_rule_added', s15_privacy_rule_added, 1.5), ('s15_electronic_data_rule_added', s15_electronic_data_rule_added, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
