from ._helpers import *


def s8_merchant_source_logged(env):
    return (
        email_stage_topic_used(env, 8, "Casa Luna Kitchen merchant's statement")
        and email_backend_has_message(env, "Casa Luna Kitchen merchant's statement", sender='manager@casaluna.example')
        and any(
            source_matches(row.get('source'), 'email_merchant')
            for row in list_from_doc(env, ROUTE_MATRIX, 'events')
        )
    )


def s8_no_unobserved_food_condition(env):
    return (
        email_backend_has_message(env, "Casa Luna Kitchen merchant's statement", sender='manager@casaluna.example')
        and record_has_tokens(
            env, 'witness_statement_template.json', 'limits',
            'food', 'internal', 'condition', witness_observed=False,
        )
    )


CHECKS = [('s8_merchant_source_logged', s8_merchant_source_logged, 1.5), ('s8_no_unobserved_food_condition', s8_no_unobserved_food_condition, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
