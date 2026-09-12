"""Stage 13 checks and weights."""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s13_budget(env) -> bool:
    """Require at least four prescribed budget keywords."""
    return H._count_any(H.scoped_text(env, ['budget'], idx=13), ['paid', 'refund pending', 'compensation pending', 'estimated', 'recovered', 'reversal', 'estimated', 'ordered']) >= 4


CHECKS = guard_stage_checks(13, [
    ("s13_budget", s13_budget, 3.0),
])
