"""SQLite backend: connection management, migrations, and CRUD helpers."""

import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from typing import Iterable, List, Optional, Tuple

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS places (
  place_id      TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  category      TEXT NOT NULL,
  lat           REAL NOT NULL,
  lng           REAL NOT NULL,
  country       TEXT NOT NULL,
  city          TEXT NOT NULL,
  rating        REAL,
  price_level   INTEGER,
  hours_json    TEXT,
  phone         TEXT,
  website       TEXT,
  formatted     TEXT
);
CREATE INDEX IF NOT EXISTS idx_places_city     ON places(city);
CREATE INDEX IF NOT EXISTS idx_places_category ON places(category);
CREATE INDEX IF NOT EXISTS idx_places_latlng   ON places(lat, lng);

CREATE TABLE IF NOT EXISTS place_reviews (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  place_id   TEXT NOT NULL REFERENCES places(place_id),
  author     TEXT NOT NULL,
  rating     INTEGER NOT NULL,
  text       TEXT NOT NULL,
  time       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reviews_place ON place_reviews(place_id);

CREATE TABLE IF NOT EXISTS roads (
  road_id   TEXT PRIMARY KEY,
  name      TEXT NOT NULL,
  city      TEXT NOT NULL,
  geom_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transit_stops (
  stop_id TEXT PRIMARY KEY,
  name    TEXT NOT NULL,
  lat     REAL NOT NULL,
  lng     REAL NOT NULL,
  city    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transit_lines (
  line_id  TEXT PRIMARY KEY,
  name     TEXT NOT NULL,
  mode     TEXT NOT NULL CHECK (mode IN ('subway','train','bus','shinkansen')),
  operator TEXT,
  segment_minutes_json TEXT
);

CREATE TABLE IF NOT EXISTS transit_schedule (
  schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
  line_id   TEXT NOT NULL REFERENCES transit_lines(line_id),
  stop_id   TEXT NOT NULL REFERENCES transit_stops(stop_id),
  direction TEXT NOT NULL,
  stop_seq  INTEGER NOT NULL,
  time      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sched_line_time ON transit_schedule(line_id, direction, time);
CREATE INDEX IF NOT EXISTS idx_sched_stop      ON transit_schedule(stop_id);

CREATE TABLE IF NOT EXISTS road_events (
  event_id  TEXT PRIMARY KEY,
  road_id   TEXT NOT NULL REFERENCES roads(road_id),
  start_dt  TEXT NOT NULL,
  end_dt    TEXT NOT NULL,
  kind      TEXT NOT NULL CHECK (kind IN ('closure','heavy_traffic','accident')),
  magnitude REAL,
  note      TEXT,
  active    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_road_events_active ON road_events(active);

CREATE TABLE IF NOT EXISTS transit_events (
  event_id  TEXT PRIMARY KEY,
  line_id   TEXT REFERENCES transit_lines(line_id),
  stop_id   TEXT REFERENCES transit_stops(stop_id),
  start_dt  TEXT NOT NULL,
  end_dt    TEXT NOT NULL,
  kind      TEXT NOT NULL CHECK (kind IN ('suspended','delayed')),
  note      TEXT,
  active    INTEGER NOT NULL DEFAULT 0,
  CHECK (line_id IS NOT NULL OR stop_id IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS idx_transit_events_active ON transit_events(active);

CREATE TABLE IF NOT EXISTS notifications (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at   TEXT NOT NULL,
  channel      TEXT NOT NULL,
  payload_json TEXT NOT NULL
);
"""


class SqliteBackend:
    """Thin wrapper around sqlite3 with per-domain CRUD helpers.

    Holds a single Connection in check_same_thread=False mode so the FastMCP
    asyncio runtime can hit it from worker threads.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        parent = os.path.dirname(os.path.abspath(db_path))
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------
    def run_migrations(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(SCHEMA_SQL)
        self.conn.commit()
        logger.info("maps_mock schema migrations applied")

    def reset(self) -> None:
        """Drop all user tables (preserves sqlite_sequence)."""
        cur = self.conn.cursor()
        names = [r[0] for r in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()]
        for n in names:
            cur.execute(f"DROP TABLE IF EXISTS {n}")
        self.conn.commit()

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

    @contextmanager
    def transaction(self):
        try:
            self.conn.execute("BEGIN")
            yield self.conn
            self.conn.execute("COMMIT")
        except Exception:
            self.conn.execute("ROLLBACK")
            raise

    # ------------------------------------------------------------------
    # simple generic helpers
    # ------------------------------------------------------------------
    def execute(self, sql: str, params: Tuple = ()) -> sqlite3.Cursor:
        return self.conn.execute(sql, params)

    def executemany(self, sql: str, seq: Iterable[Tuple]) -> sqlite3.Cursor:
        return self.conn.executemany(sql, seq)

    def fetchall(self, sql: str, params: Tuple = ()) -> List[sqlite3.Row]:
        return list(self.conn.execute(sql, params).fetchall())

    def fetchone(self, sql: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        return self.conn.execute(sql, params).fetchone()

    # ------------------------------------------------------------------
    # places
    # ------------------------------------------------------------------
    def list_places(self) -> List[sqlite3.Row]:
        return self.fetchall("SELECT * FROM places ORDER BY place_id ASC")

    def get_place(self, place_id: str) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM places WHERE place_id = ?", (place_id,))

    def list_place_reviews(self, place_id: str) -> List[sqlite3.Row]:
        return self.fetchall(
            "SELECT author, rating, text, time FROM place_reviews WHERE place_id = ? ORDER BY time DESC",
            (place_id,),
        )

    # ------------------------------------------------------------------
    # transit
    # ------------------------------------------------------------------
    def list_transit_stops(self) -> List[sqlite3.Row]:
        return self.fetchall("SELECT * FROM transit_stops ORDER BY stop_id ASC")

    def get_transit_stop(self, stop_id: str) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM transit_stops WHERE stop_id = ?", (stop_id,))

    def list_transit_lines(self) -> List[sqlite3.Row]:
        return self.fetchall("SELECT * FROM transit_lines ORDER BY line_id ASC")

    def get_transit_line(self, line_id: str) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM transit_lines WHERE line_id = ?", (line_id,))

    def line_schedule(self, line_id: str, direction: str) -> List[sqlite3.Row]:
        return self.fetchall(
            """SELECT schedule_id, line_id, stop_id, direction, stop_seq, time
               FROM transit_schedule
               WHERE line_id = ? AND direction = ?
               ORDER BY time, stop_seq""",
            (line_id, direction),
        )

    def lines_serving_stop(self, stop_id: str) -> List[sqlite3.Row]:
        return self.fetchall(
            """SELECT DISTINCT line_id, direction
               FROM transit_schedule
               WHERE stop_id = ?""",
            (stop_id,),
        )

    # ------------------------------------------------------------------
    # events + notifications
    # ------------------------------------------------------------------
    def list_road_events(self, only_active: bool = False) -> List[sqlite3.Row]:
        if only_active:
            return self.fetchall("SELECT * FROM road_events WHERE active = 1")
        return self.fetchall("SELECT * FROM road_events")

    def list_transit_events(self, only_active: bool = False) -> List[sqlite3.Row]:
        if only_active:
            return self.fetchall("SELECT * FROM transit_events WHERE active = 1")
        return self.fetchall("SELECT * FROM transit_events")

    def get_road_event(self, event_id: str) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM road_events WHERE event_id = ?", (event_id,))

    def get_transit_event(self, event_id: str) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM transit_events WHERE event_id = ?", (event_id,))

    def insert_road_event(self, ev: dict) -> None:
        self.execute(
            """INSERT OR REPLACE INTO road_events
               (event_id, road_id, start_dt, end_dt, kind, magnitude, note, active)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                ev["event_id"], ev["road_id"], ev["start_dt"], ev["end_dt"],
                ev["kind"], ev.get("magnitude"), ev.get("note"),
                1 if ev.get("active") else 0,
            ),
        )

    def insert_transit_event(self, ev: dict) -> None:
        self.execute(
            """INSERT OR REPLACE INTO transit_events
               (event_id, line_id, stop_id, start_dt, end_dt, kind, note, active)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                ev["event_id"], ev.get("line_id"), ev.get("stop_id"),
                ev["start_dt"], ev["end_dt"], ev["kind"], ev.get("note"),
                1 if ev.get("active") else 0,
            ),
        )

    def set_road_event_active(self, event_id: str, active: bool) -> None:
        self.execute(
            "UPDATE road_events SET active = ? WHERE event_id = ?",
            (1 if active else 0, event_id),
        )

    def set_transit_event_active(self, event_id: str, active: bool) -> None:
        self.execute(
            "UPDATE transit_events SET active = ? WHERE event_id = ?",
            (1 if active else 0, event_id),
        )

    def insert_notification(self, created_at: str, channel: str, payload: dict) -> int:
        cur = self.execute(
            "INSERT INTO notifications(created_at, channel, payload_json) VALUES (?,?,?)",
            (created_at, channel, json.dumps(payload, ensure_ascii=False)),
        )
        return int(cur.lastrowid)

    def list_notifications(self) -> List[sqlite3.Row]:
        return self.fetchall("SELECT * FROM notifications ORDER BY id ASC")

    # ------------------------------------------------------------------
    # roads
    # ------------------------------------------------------------------
    def list_roads(self) -> List[sqlite3.Row]:
        return self.fetchall("SELECT * FROM roads ORDER BY road_id ASC")

    def get_road(self, road_id: str) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM roads WHERE road_id = ?", (road_id,))

    def roads_in_city(self, city: str) -> List[sqlite3.Row]:
        return self.fetchall("SELECT * FROM roads WHERE city = ?", (city,))

    # ------------------------------------------------------------------
    # counts
    # ------------------------------------------------------------------
    def count_places(self) -> int:
        return int(self.fetchone("SELECT COUNT(*) AS c FROM places")["c"])


def ensure_db(db_path: str) -> SqliteBackend:
    """Open (creating if needed) a SQLite DB and migrate it.

    Schema is always (re)applied idempotently. Callers inject row state
    separately via ``apply_init_sql``.
    """
    backend = SqliteBackend(db_path)
    backend.run_migrations()
    return backend
