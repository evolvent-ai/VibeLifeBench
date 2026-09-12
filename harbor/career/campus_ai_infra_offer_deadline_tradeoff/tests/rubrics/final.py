from __future__ import annotations

from ._helpers import _check


def final_no_accept_or_reject_without_authorization(env) -> bool:
    return _check("stage_20_no_accept_or_reject", env)


CHECKS = [
    ("final_no_accept_or_reject_without_authorization", final_no_accept_or_reject_without_authorization, 2.0),
]
