from datetime import datetime

from . import _helpers as H


def _parse(value):
    if isinstance(value, dict):
        value = value.get("dateTime") or value.get("date")
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def self_review_calendar_checkpoint_exists(env):
    events = H.calendar_events(env)
    matching = []
    for event in events:
        text = " ".join(str(event.get(key) or "") for key in ("summary", "description"))
        if H.has_terms(text, ("tax application", "annual settlement"), ("review", "personal operation")):
            matching.append(event)
    if len(matching) != 1:
        return False
    target = matching[0]
    start = _parse(target.get("start_dt") or target.get("start"))
    end = _parse(target.get("end_dt") or target.get("end"))
    if not start or not end or not (datetime.fromisoformat("2026-06-29T14:10:00+08:00") <= start <= datetime.fromisoformat("2026-06-30T23:00:00+08:00")):
        return False
    for event in events:
        if event is target or H.norm(event.get("status")) == "cancelled":
            continue
        other_start = _parse(event.get("start_dt") or event.get("start"))
        other_end = _parse(event.get("end_dt") or event.get("end"))
        if other_start and other_end and start < other_end and other_start < end:
            return False
    return H.norm(target.get("status")) in {"confirmed", "tentative"}


CHECKS = [("tax_s11_self_review_calendar_checkpoint_exists", self_review_calendar_checkpoint_exists, 1.5)]
