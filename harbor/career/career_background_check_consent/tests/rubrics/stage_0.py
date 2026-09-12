"""Stage 0: establish the three-track dashboard."""
from __future__ import annotations
from ._helpers import notion_text, text_has, workspace_text


def _three_tracks(text: str) -> bool:
    return (text_has(text, [["severance", "compensation"]])
            and text_has(text, [["authorization", "authorization scope", "consent"]])
            and text_has(text, [["search", "application", "interview", "position", "offer"]]))


def s0_dual_track_tracker(env) -> bool:
    return _three_tracks(notion_text(env)) and _three_tracks(workspace_text(env))


CHECKS = [("s0_dual_track_tracker", s0_dual_track_tracker, 3.0)]
