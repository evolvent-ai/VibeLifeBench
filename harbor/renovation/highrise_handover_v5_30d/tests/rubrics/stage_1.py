"""Stage 1 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s1_servers(env) -> bool:
    return H.stage_servers(env, 1, ("email", "calendar"), 1)


def s1_args(env) -> bool:
    return H.stage_args(env, 1, ("handover", "inspection", "2026-06-17"), 1)


def s1_result(env) -> bool:
    return H.artifact_has(env, ("control",), (("documents",), ("pending verification", "open"), ("source",), ("due_at",)))


CHECKS = [
    ("s1_servers", s1_servers, 0.5),
    ("s1_args", s1_args, 0.5),
    ("s1_result", s1_result, 1.0),
]
