from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable, Optional


DDL = """
CREATE TABLE IF NOT EXISTS climate_profiles (
    profile_id                TEXT PRIMARY KEY,
    seasonal_temp_means_json  TEXT NOT NULL,
    precip_freq_json          TEXT NOT NULL,
    wind_baseline_kmh         REAL NOT NULL,
    humidity_baseline_pct     REAL NOT NULL,
    aqi_baseline_json         TEXT NOT NULL,
    notes                     TEXT
);

CREATE TABLE IF NOT EXISTS locations (
    geo_key             TEXT PRIMARY KEY,
    city                TEXT NOT NULL,
    country             TEXT NOT NULL,
    lat                 REAL NOT NULL,
    lng                 REAL NOT NULL,
    timezone            TEXT NOT NULL,
    climate_profile_id  TEXT NOT NULL REFERENCES climate_profiles(profile_id),
    kind                TEXT NOT NULL DEFAULT 'city'
);

CREATE TABLE IF NOT EXISTS daily_weather (
    geo_key      TEXT NOT NULL REFERENCES locations(geo_key),
    date         TEXT NOT NULL,
    tmin         REAL NOT NULL,
    tmax         REAL NOT NULL,
    condition    TEXT NOT NULL,
    precip_mm    REAL NOT NULL,
    precip_prob  REAL NOT NULL,
    wind_kmh     REAL NOT NULL,
    PRIMARY KEY (geo_key, date)
);

CREATE TABLE IF NOT EXISTS hourly_weather (
    geo_key    TEXT NOT NULL REFERENCES locations(geo_key),
    datetime   TEXT NOT NULL,
    temp_c     REAL NOT NULL,
    humidity   REAL NOT NULL,
    condition  TEXT NOT NULL,
    precip_mm  REAL NOT NULL,
    wind_kmh   REAL NOT NULL,
    PRIMARY KEY (geo_key, datetime)
);

CREATE INDEX IF NOT EXISTS idx_hourly_geo_dt ON hourly_weather(geo_key, datetime);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id     TEXT PRIMARY KEY,
    kind         TEXT NOT NULL,
    severity     TEXT NOT NULL,
    start_dt     TEXT NOT NULL,
    end_dt       TEXT NOT NULL,
    areas_json   TEXT NOT NULL,
    description  TEXT NOT NULL,
    active       INTEGER NOT NULL DEFAULT 1,
    created_at   TEXT NOT NULL,
    source_event TEXT
);

CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts(active);

CREATE TABLE IF NOT EXISTS alert_subscriptions (
    sub_id      TEXT PRIMARY KEY,
    geo_key     TEXT NOT NULL REFERENCES locations(geo_key),
    sink        TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    active      INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS notifications (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at   TEXT NOT NULL,
    channel      TEXT NOT NULL,
    sub_id       TEXT REFERENCES alert_subscriptions(sub_id),
    alert_id     TEXT REFERENCES alerts(alert_id),
    payload_json TEXT NOT NULL,
    delivered    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS typhoon_tracks (
    storm_id   TEXT NOT NULL,
    dt         TEXT NOT NULL,
    lat        REAL NOT NULL,
    lng        REAL NOT NULL,
    intensity  TEXT NOT NULL,
    PRIMARY KEY (storm_id, dt)
);

CREATE TABLE IF NOT EXISTS daily_aqi (
    geo_key             TEXT NOT NULL REFERENCES locations(geo_key),
    date                TEXT NOT NULL,
    aqi                 INTEGER NOT NULL,
    category            TEXT NOT NULL,
    dominant_pollutant  TEXT NOT NULL,
    observed_at         TEXT NOT NULL,
    PRIMARY KEY (geo_key, date)
);

CREATE TABLE IF NOT EXISTS _counters (
    name  TEXT PRIMARY KEY,
    value INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS _sim_clock (
    id      INTEGER PRIMARY KEY,
    sim_now TEXT NOT NULL
);
"""


def _row_factory(cursor: sqlite3.Cursor, row: tuple) -> dict:
    cols = [c[0] for c in cursor.description]
    return dict(zip(cols, row))


class SQLiteBackend:
    """Thin SQLite wrapper with DDL bootstrap + convenience helpers."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        parent = Path(db_path).parent
        if str(parent) and not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(
            db_path, check_same_thread=False, isolation_level=None
        )
        self.conn.row_factory = _row_factory
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA foreign_keys=ON;")
        self.conn.executescript(DDL)

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

    # --- generic helpers -------------------------------------------------

    def execute(self, sql: str, params: tuple | dict | None = None) -> sqlite3.Cursor:
        return self.conn.execute(sql, params or ())

    def executemany(self, sql: str, seq: Iterable[tuple | dict]) -> sqlite3.Cursor:
        return self.conn.executemany(sql, seq)

    def fetchone(self, sql: str, params: tuple | dict | None = None) -> Optional[dict]:
        cur = self.conn.execute(sql, params or ())
        return cur.fetchone()

    def fetchall(self, sql: str, params: tuple | dict | None = None) -> list[dict]:
        cur = self.conn.execute(sql, params or ())
        return cur.fetchall()

    def apply_init_sql(self, init_sql_path: str) -> None:
        path = Path(init_sql_path)
        with open(path, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())
