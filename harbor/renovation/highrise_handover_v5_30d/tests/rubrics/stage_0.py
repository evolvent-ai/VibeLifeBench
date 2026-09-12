"""Stage 0 checks."""
from __future__ import annotations

from .shared import _helpers as H


def s0_servers(env) -> bool:
    return H.stage_servers(env, 0, ("email", "calendar", "ecommerce"), 2)


def s0_args(env) -> bool:
    return H.stage_args(env, 0, ("ord_hhigh_0001", "chu.nuo.hd@gmail.com", "handover"), 1)


def s0_result(env) -> bool:
    return H.email_search_has_details(env, (("交付资料目录", "handover document index"), ("竣工资料", "住宅质量保证书", "completion documents", "residential quality warranty")), query="交付", folder="INBOX", page=1, page_size=20) and H.artifact_has(env, ("control", "evidence"), (("handover documents", "document index"), ("pending verification", "open"), ("source",)))


def s0_files(env) -> bool:
    return all(H.artifact_fields(env, key) for key in ("control", "defects", "claims", "evidence"))


CHECKS = [
    ("s0_servers", s0_servers, 0.5),
    ("s0_args", s0_args, 1.0),
    ("s0_result", s0_result, 1.5),
    ("s0_files", s0_files, 0.5),
]
