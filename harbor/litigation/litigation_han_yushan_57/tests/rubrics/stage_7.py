from __future__ import annotations
from ._helpers import semantic_check

def s7_property_contract_indexed_sensitive(env) -> bool:
    return semantic_check(env, 's7_property_contract_indexed_sensitive')

def s7_property_role_added(env) -> bool:
    return semantic_check(env, 's7_property_role_added')

CHECKS = [
    ('s7_property_contract_indexed_sensitive', s7_property_contract_indexed_sensitive, 1.75),
    ('s7_property_role_added', s7_property_role_added, 1.5),
]
