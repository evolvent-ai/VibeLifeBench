from ._helpers import guard_stage_checks
from . import _helpers as H
def s21_checklist(env): return H._count_any(H.scoped_text(env, ["decision", "tracker", "summary"], idx=21), ["repayment", "shipment", "warranty", "proceeds", "dispute", "completed", "pending confirmation"]) >= 5
CHECKS = guard_stage_checks(21, [("s21_checklist", s21_checklist, 2.0)])
