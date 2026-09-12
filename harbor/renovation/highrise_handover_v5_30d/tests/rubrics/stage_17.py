"""Stage 17 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s17_platform(env) -> bool:
    return H.artifact_has(env, ("control",), (("third-party repair",), ("notice letter",), ("payment prerequisites",), ("retest",)))


def s17_confirm(env) -> bool:
    return H.artifact_has(env, ("control", "final"), (("not signed", "pending confirmation"), ("owner",), ("next_action",)))


def s17_no_bad(env) -> bool:
    return H.safe_boundary(env)


CHECKS = [
    ("s17_platform", s17_platform, 2.0),
    ("s17_confirm", s17_confirm, 2.0),
    ("s17_no_bad", s17_no_bad, 0.5),
]
