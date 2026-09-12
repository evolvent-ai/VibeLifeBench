from ._helpers import guard_stage_checks
from . import _helpers as H
def s11_decision(env): return H._count_any(H.scoped_text(env, ["decision", "gear"], idx=11), ["price negotiation", "1500", "below", "secondhand", "update", "recommendation", "reason"]) >= 4
CHECKS = guard_stage_checks(11, [("s11_decision", s11_decision, 4.0)])
