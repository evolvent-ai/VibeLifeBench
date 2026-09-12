from __future__ import annotations
from ._helpers import semantic_check

def s16_format_requirements_indexed(env) -> bool:
    return semantic_check(env, 's16_format_requirements_indexed')

CHECKS = [
    ('s16_format_requirements_indexed', s16_format_requirements_indexed, 1.5),
]
