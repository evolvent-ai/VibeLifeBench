"""Cross-stage checks — """
from __future__ import annotations

from .checks import cs_evidence, cs_auth, cs_updated, cs_funds

CHECKS = [
    ("cs_evidence", cs_evidence, 5.0),
    ("cs_auth", cs_auth, 5.0),
    ("cs_updated", cs_updated, 4.5),
    ("cs_funds", cs_funds, 4.5),
]
