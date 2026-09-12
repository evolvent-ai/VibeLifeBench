from ._helpers import guard_stage_checks
from . import _helpers as H
def s22_consistency(env): return H._count_any(H.scoped_text(env, ["tracker", "decision", "risk"], idx=22), ["consistent", "reconcile", "conflict", "check", "store", "forwarding", "credit card"]) >= 4
CHECKS = guard_stage_checks(22, [("s22_consistency", s22_consistency, 2.0)])
