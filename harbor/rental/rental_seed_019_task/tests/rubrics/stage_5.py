from __future__ import annotations
from ._helpers import *

def s5_repair_threads_indexed(env) -> bool:
    return (
        stage_read_email_ids(env, 5, ('2',))
        and stage_read_email_ids(env, 5, ('3',))
        and tool_stage(env, 5, 'email', 'read_email', ['repair'])
        and tool_stage(env, 5, 'email', 'read_email', ['damp mark'])
        and tool_stage(env, 5, 'notion', None, ['repair'])
    )

def s5_oral_written_split(env) -> bool:
    return (
        tool_stage(env, 5, 'notion', None, ['verbal'])
        and tool_stage(env, 5, 'notion', None, ['written'])
        and workspace_file_has_groups(env, 'REPAIR_EVIDENCE_INDEX.md', [('verbal',), ('written',), ('repair status',)])
    )

CHECKS = [
    ('s5_repair_threads_indexed', s5_repair_threads_indexed, 1.5),
    ('s5_oral_written_split', s5_oral_written_split, 1.5),
]
