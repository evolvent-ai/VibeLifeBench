from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional
from zoneinfo import ZoneInfo

from ..backends.sqlite_backend import SQLiteBackend
from ..utils.exceptions import WeatherNotFound
from ..utils.geo_resolver import resolve_geo


def _category(aqi: int) -> str:
    if aqi <= 50:
        return "good"
    if aqi <= 100:
        return "moderate"
    if aqi <= 150:
        return "unhealthy_for_sensitive"
    if aqi <= 200:
        return "unhealthy"
    if aqi <= 300:
        return "very_unhealthy"
    return "hazardous"


class AQIService:
    """AQI lookup with two-tier resolution:

    1. Seeded ``daily_aqi`` row for (geo_key, today) supplies the answer
       if present.
    2. Otherwise fall back to the location's climate-profile baseline.

    "Today" is the real wall-clock date in the location's local timezone.
    """

    def __init__(self, be: SQLiteBackend) -> None:
        self.be = be

    def _resolve(self, geo: Any) -> dict:
        row = resolve_geo(
            geo, self.be.fetchall("SELECT * FROM locations ORDER BY geo_key")
        )
        if row is None:
            raise WeatherNotFound("no_nearby_location")
        return row

    def _baseline(self, profile_id: str) -> tuple[int, str]:
        row = self.be.fetchone(
            "SELECT aqi_baseline_json FROM climate_profiles WHERE profile_id = ?",
            (profile_id,),
        )
        if not row:
            return 50, "pm25"
        data = json.loads(row["aqi_baseline_json"])
        return int(data["aqi"]), str(data.get("dominant", "pm25"))

    def _seeded_daily(self, geo_key: str, date_str: str) -> Optional[dict]:
        return self.be.fetchone(
            """SELECT aqi, dominant_pollutant, observed_at
               FROM daily_aqi WHERE geo_key = ? AND date = ?""",
            (geo_key, date_str),
        )

    def _now_in(self, tz: str) -> datetime:
        row = self.be.fetchone("SELECT sim_now FROM _sim_clock WHERE id = 1")
        if row and row.get("sim_now"):
            return datetime.fromisoformat(str(row["sim_now"])).astimezone(ZoneInfo(tz))
        return datetime.now(timezone.utc).astimezone(ZoneInfo(tz))

    def get_aqi(self, geo: Any) -> dict:
        loc = self._resolve(geo)
        now = self._now_in(loc["timezone"])
        seeded = self._seeded_daily(loc["geo_key"], now.date().isoformat())
        if seeded:
            aqi = int(seeded["aqi"])
            dominant = str(seeded["dominant_pollutant"])
        else:
            aqi, dominant = self._baseline(loc["climate_profile_id"])
        return {
            "geo_key": loc["geo_key"],
            "aqi": aqi,
            "category": _category(aqi),
            "dominant_pollutant": dominant,
            "observed_at": now.replace(minute=0, second=0, microsecond=0).isoformat(),
        }
