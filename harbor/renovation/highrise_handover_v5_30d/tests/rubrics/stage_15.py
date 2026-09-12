"""Stage 15 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s15_servers(env) -> bool:
    return H.stage_servers(env, 15, ("weather", "calendar", "email"), 1)


def s15_result(env) -> bool:
    return H.artifact_has(env, ("defects", "evidence"), (("exterior window",), ("floor drain",), ("entrance door",), ("present", "owner")))


def s15_weather(env) -> bool:
    return H.artifact_has(env, ("evidence",), (("rainfall", "rain conditions"), ("wind direction",), ("window sash",), ("continuous video",), ("captured_at",)))


CHECKS = [
    ("s15_servers", s15_servers, 0.5),
    ("s15_result", s15_result, 3.0),
    ("s15_weather", s15_weather, 2.5),
]
