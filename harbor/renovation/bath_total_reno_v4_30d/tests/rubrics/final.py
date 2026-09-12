"""Final-bucket checks — independently named functions."""
from __future__ import annotations

from .checks import f_budget, f_risk, f_evidence, f_summary, f_tracker, f_no_bad

CHECKS = [
    ("f_budget", f_budget, 4.5),
    ("f_risk", f_risk, 4.5),
    ("f_evidence", f_evidence, 4.5),
    ("f_summary", f_summary, 4.0),
    ("f_tracker", f_tracker, 3.0),
    ("f_no_bad", f_no_bad, 4.0),
]
