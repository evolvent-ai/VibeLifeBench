from __future__ import annotations

from ._helpers import _workspace_file_text


def _near(text: str, anchors: tuple[str, ...], terms: tuple[str, ...], radius: int = 120) -> bool:
    for anchor in anchors:
        start = 0
        while True:
            index = text.find(anchor, start)
            if index < 0:
                break
            context = text[max(0, index - radius): index + len(anchor) + radius]
            if all(any(option in context for option in group.split("|")) for group in terms):
                return True
            start = index + len(anchor)
    return False


def s5_records_mobility_preferences(env) -> bool:
    text = _workspace_file_text(env, "trip_plan.md") + "\n" + _workspace_file_text(env, "decision_log.md")
    father = _near(text, ("father", "paternal", "dad"), ("red-eye|overnight flight", "early|too early|very early"))
    mother = _near(text, ("mother", "maternal", "mom"), ("accessible|step-free|mobility accessibility|no steps", "elevator|lift|near the elevator", "station|walk|rail station|walking"))
    return bool(father and mother)


CHECKS = [("s5_records_mobility_preferences", s5_records_mobility_preferences, 2.0)]
