from __future__ import annotations
from ._helpers import *

def final_packet_complete(env) -> bool:
    return final_order_batch_matrix(env)

def final_notion_and_legal_saved(env) -> bool:
    return pretrial_notes_saved(env) and notion_persisted(env)

def final_draft_registry_safe(env) -> bool:
    return recall_notice_draft_saved(env)

CHECKS = [
    ('final_packet_complete', final_packet_complete, 2.0),
    ('final_notion_and_legal_saved', final_notion_and_legal_saved, 1.5),
    ('final_draft_registry_safe', final_draft_registry_safe, 1.75),
]
