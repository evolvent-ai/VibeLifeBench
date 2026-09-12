"""Stage 21: publish the review."""
from __future__ import annotations
from ._helpers import notion_text, norm_num, text_has, used_tool


def _stage21_notion_write(env) -> bool:
    return any(used_tool(env, tool, stage=21, server="notion") for tool in ("API-post-page", "API-patch-page", "API-patch-block-children", "API-update-a-block"))


def s21_wrapup_severance(env) -> bool:
    if not _stage21_notion_write(env):
        return False
    raw = notion_text(env)
    compact = norm_num(raw)
    return all(value in compact for value in ("204500", "301500", "97000")) and text_has(raw, [["severance"], ["received", "paid"], ["shortfall", "not topped up", "still due"]]) and text_has(raw, [["authorization", "authorization scope"], ["necessity", "consent", "not authorized"], ["health", "medical", "examination"]])


def s21_wrapup_reemploy(env) -> bool:
    return _stage21_notion_write(env) and text_has(notion_text(env), [["application", "interview", "offer"], ["Meituan"], ["unresolved", "next", "pending", "follow-up"]])


CHECKS = [("s21_wrapup_severance", s21_wrapup_severance, 2.5), ("s21_wrapup_reemploy", s21_wrapup_reemploy, 2.0)]
