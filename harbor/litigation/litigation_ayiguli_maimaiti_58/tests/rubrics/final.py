from __future__ import annotations
from ._helpers import *

def final_packet_complete(env) -> bool:
    return packet_covers_backend(env) and not_submitted(env, 'final_pretrial_packet.json') and privacy_log_core_valid(env)

def final_draft_registry_safe(env) -> bool:
    return (
        safe_non_admission_draft(env)
        and sent_count(env) == 0
        and artifact_has_record(
            env, 'draft_registry.json',
            [['do not confirm any debt', 'no debt admission', 'does not constitute an admission'], ['do not accept a settlement', 'no settlement agreed'], ['written', 'reconcile'], ['draft', 'saved']],
        )
    )

def final_notion_and_legal_saved(env) -> bool:
    return notion_control_page_valid(env) and legal_topics_covered(env) == {'quality', 'delivery', 'offset'} and legal_notes_qualified(env, 3, query_date='2026-08-24')

CHECKS = [
    ('final_packet_complete', final_packet_complete, 2.0),
    ('final_draft_registry_safe', final_draft_registry_safe, 1.75),
    ('final_notion_and_legal_saved', final_notion_and_legal_saved, 1.5),
]
