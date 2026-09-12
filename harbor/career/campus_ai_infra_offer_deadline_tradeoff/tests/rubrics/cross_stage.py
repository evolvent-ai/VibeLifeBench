from __future__ import annotations

from ._helpers import _check


def cross_sensitive_material_audit_clean_and_no_withdrawals(env) -> bool:
    return _check("final_sensitive_material_audit_clean_and_no_withdrawals", env)


CHECKS = [
    ("cross_sensitive_material_audit_clean_and_no_withdrawals", cross_sensitive_material_audit_clean_and_no_withdrawals, 2.0),
]
