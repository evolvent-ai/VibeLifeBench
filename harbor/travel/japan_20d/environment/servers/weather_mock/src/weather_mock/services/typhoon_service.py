from __future__ import annotations

from datetime import datetime

from ..backends.sqlite_backend import SQLiteBackend
from ..utils.exceptions import UnknownStorm
from ..utils.world_clock import now as _world_now


class TyphoonService:
    """Agent-facing read-only access to ``typhoon_tracks`` rows."""

    def __init__(self, be: SQLiteBackend) -> None:
        self.be = be

    def get_track(self, storm_id: str) -> list[dict]:
        rows = self.be.fetchall(
            "SELECT * FROM typhoon_tracks WHERE storm_id = ? ORDER BY dt",
            (storm_id,),
        )
        cutoff = _world_now()
        rows = [
            row
            for row in rows
            if datetime.fromisoformat(str(row["dt"]).replace("Z", "+00:00")) <= cutoff
        ]
        if not rows:
            raise UnknownStorm(f"unknown_storm:{storm_id}")
        return [
            {"dt": r["dt"], "lat": r["lat"], "lng": r["lng"], "intensity": r["intensity"]}
            for r in rows
        ]
