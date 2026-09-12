"""Stage 13: testing institution replacement."""
from __future__ import annotations
from ._helpers import _stage_corpus, _notifications
from .cross_stage import d_inspect_reselect

def s13_detects_withdraw(env) -> bool:
    notifs = _notifications(env)
    if notifs is None: return False
    notice = any(str(item.get("notification_id") or "") == "ntf_food_s13_inspector_pause" or (any(k in f"{item.get('title','')} {item.get('body','')}" for k in ("JY-006", "Huizheng")) and any(k in f"{item.get('title','')} {item.get('body','')}" for k in ("paused", "disabled", "unusable"))) for item in notifs)
    return notice and any(k in _stage_corpus(env, 13) for k in ("JY-006", "Huizheng", "paused", "unusable", "disabled", "replace", "change institution", "choose another"))
CHECKS = [("s13_detects_withdraw", s13_detects_withdraw, 0.5), ("d_inspect_reselect", d_inspect_reselect, 3.389)]

