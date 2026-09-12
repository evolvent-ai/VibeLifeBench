from __future__ import annotations

from ..backends.sqlite_backend import SQLiteBackend
from ..utils.exceptions import UnknownStorm


class TyphoonService:
    """Agent-facing read-only access to ``typhoon_tracks`` rows."""

    def __init__(self, be: SQLiteBackend) -> None:
        self.be = be

    def get_track(self, storm_id: str) -> list[dict]:
        rows = self.be.fetchall(
            "SELECT * FROM typhoon_tracks WHERE storm_id = ? ORDER BY dt",
            (storm_id,),
        )
        if not rows:
            raise UnknownStorm(f"unknown_storm:{storm_id}")
        return [
            {"dt": r["dt"], "lat": r["lat"], "lng": r["lng"], "intensity": r["intensity"]}
            for r in rows
        ]
