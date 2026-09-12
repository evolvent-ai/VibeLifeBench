from ._helpers import *


def s17_template_created(env):
    return (
        (notion_write_for(env, 17, 'factual statement') or notion_write_for(env, 17, 'witness'))
        and notion_backend_has_content(env, 'factual witness statement template', 'personal confirmation')
        and doc_value(env, 'witness_statement_template.json', 'requires_diego_confirmation', True)
        and doc_text_has(env, 'witness_statement_template.json', 'status', 'draft', 'review')
    )


def s17_uncertainties_listed(env):
    return (
        notion_write_used(env, 17)
        and notion_backend_has_content(env, 'factual witness statement template', 'unresolved')
        and record_has_tokens(env, 'witness_statement_template.json', 'uncertainties', 'delivery', 'time', 'conflict', unresolved=True)
        and record_has_tokens(env, 'witness_statement_template.json', 'uncertainties', 'food', 'internal', 'condition', unresolved=True)
    )


CHECKS = [('s17_template_created', s17_template_created, 1.75), ('s17_uncertainties_listed', s17_uncertainties_listed, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
