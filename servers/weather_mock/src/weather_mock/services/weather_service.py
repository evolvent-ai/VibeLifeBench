from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from zoneinfo import ZoneInfo

from ..backends.sqlite_backend import SQLiteBackend
from ..utils.exceptions import WeatherNotFound
from ..utils.geo_resolver import resolve_geo


def _now_in(tz: str, be: SQLiteBackend | None = None) -> datetime:
    if be is not None:
        row = be.fetchone("SELECT sim_now FROM _sim_clock WHERE id = 1")
        if row and row.get("sim_now"):
            return datetime.fromisoformat(str(row["sim_now"])).astimezone(ZoneInfo(tz))
    return datetime.now(timezone.utc).astimezone(ZoneInfo(tz))


class WeatherService:
    """Read-through lookup against the pre-baked weather rows in init.sql.

    Anchors "now" on the real wall-clock in the location's local timezone.
    If a row is missing for the requested hour/day, returns an empty list
    (forecasts) or a ``WeatherNotFound`` error (get_current).
    """

    def __init__(self, be: SQLiteBackend) -> None:
        self.be = be

    # ------------------------------------------------------------------

    def _all_locations(self) -> list[dict]:
        return self.be.fetchall("SELECT * FROM locations ORDER BY geo_key")

    def _resolve(self, geo: Any) -> dict:
        row = resolve_geo(geo, self._all_locations())
        if row is None:
            raise WeatherNotFound("no_nearby_location")
        return row

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_current(self, geo: Any) -> dict:
        loc = self._resolve(geo)
        tz = loc["timezone"]
        now_local = _now_in(tz, self.be)
        hour_dt = now_local.replace(minute=0, second=0, microsecond=0)
        row = self.be.fetchone(
            "SELECT * FROM hourly_weather WHERE geo_key = ? AND datetime = ?",
            (loc["geo_key"], hour_dt.isoformat()),
        )
        if not row:
            raise WeatherNotFound("observation missing")
        return {
            "geo_key": loc["geo_key"],
            "city": loc["city"],
            "temp_c": row["temp_c"],
            "humidity": row["humidity"],
            "wind_kmh": row["wind_kmh"],
            "condition": row["condition"],
            "precip_mm": row["precip_mm"],
            "observed_at": hour_dt.isoformat(),
        }

    def get_forecast_hourly(self, geo: Any, hours: int = 72) -> list[dict]:
        hours = max(1, min(120, int(hours)))
        loc = self._resolve(geo)
        tz = loc["timezone"]
        now_local = _now_in(tz, self.be)
        start = (now_local + timedelta(hours=1)).replace(
            minute=0, second=0, microsecond=0
        )
        out: list[dict] = []
        for i in range(hours):
            dt = start + timedelta(hours=i)
            row = self.be.fetchone(
                "SELECT * FROM hourly_weather WHERE geo_key = ? AND datetime = ?",
                (loc["geo_key"], dt.isoformat()),
            )
            if row is None:
                continue
            out.append(
                {
                    "dt": dt.isoformat(),
                    "temp_c": row["temp_c"],
                    "condition": row["condition"],
                    "precip_mm": row["precip_mm"],
                    "wind_kmh": row["wind_kmh"],
                }
            )
        return out

    def get_forecast_daily(self, geo: Any, days: int = 10) -> list[dict]:
        days = max(1, min(14, int(days)))
        loc = self._resolve(geo)
        tz = loc["timezone"]
        start_date = _now_in(tz, self.be).date()
        out: list[dict] = []
        for i in range(days):
            d = start_date + timedelta(days=i)
            date_str = d.isoformat()
            row = self.be.fetchone(
                "SELECT * FROM daily_weather WHERE geo_key = ? AND date = ?",
                (loc["geo_key"], date_str),
            )
            if row is None:
                continue
            out.append(
                {
                    "date": date_str,
                    "tmin": row["tmin"],
                    "tmax": row["tmax"],
                    "condition": row["condition"],
                    "precip_prob": row["precip_prob"],
                    "wind_kmh": row["wind_kmh"],
                }
            )
        return out
