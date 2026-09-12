"""Stage 22 checks — atomic Checker definitions and weights are in this module。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s22_consistency(env) -> bool:
    """Persist cross-service reconciliation without flattening unresolved differences."""
    return H._count_any(
        H.scoped_text(env, ['tracker', 'decision', 'risk'], idx=22),
        ['consistent', 'reconciliation', 'conflict', 'time difference', 'marketplace', 'delivery and installation', 'credit card', 'email', 'notification'],
    ) >= 5


CHECKS = guard_stage_checks(22, [
    ("s22_consistency", s22_consistency, 2.0),
])
