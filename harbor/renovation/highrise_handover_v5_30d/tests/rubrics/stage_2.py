"""Stage 2 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s2_servers(env) -> bool:
    return H.stage_servers(env, 2, ("email", "weather", "ecommerce"), 2)


def s2_args(env) -> bool:
    return H.stage_args(env, 2, ("ord_hhigh_0001", "exterior window", "floor drain"), 1)


def s2_result(env) -> bool:
    return H.artifact_has(env, ("defects", "evidence"), (("exterior window",), ("floor drain",), ("entrance door",), ("evidence_id", "evidence_ids")))


def s2_options(env) -> bool:
    return H.artifact_has(env, ("control", "defects"), (("rainfall", "rain conditions"), ("retest",), ("photo", "video"), ("responsible party", "owner")))


CHECKS = [
    ("s2_servers", s2_servers, 0.5),
    ("s2_args", s2_args, 1.0),
    ("s2_result", s2_result, 2.0),
    ("s2_options", s2_options, 2.0),
]
