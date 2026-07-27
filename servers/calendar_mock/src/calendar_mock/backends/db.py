"""SQLite backend for calendar_mock.

Schema-only — no bundled seed data. State is injected by callers via
``<env>/init.sql`` (INSERTs run after schema creation).

v3: dropped the simulated-clock singleton and the recurrence-materialized
log table. Recurring
events still carry an ``recurrence_rule`` column for round-tripping
through ``get_event``, but expansion is not performed by the server —
init.sql either pre-bakes the child rows directly or the agent treats
recurring rows as opaque single events.
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS calendars (
  calendar_id   TEXT PRIMARY KEY,
  user_id       TEXT NOT NULL,
  name          TEXT NOT NULL,
  color         TEXT,
  timezone      TEXT NOT NULL DEFAULT 'UTC',
  is_primary    INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_calendars_user ON calendars(user_id);

CREATE TABLE IF NOT EXISTS events (
  event_id        TEXT PRIMARY KEY,
  calendar_id     TEXT NOT NULL,
  summary         TEXT NOT NULL,
  description     TEXT,
  location        TEXT,
  start_dt        TEXT NOT NULL,
  end_dt          TEXT NOT NULL,
  all_day         INTEGER NOT NULL DEFAULT 0,
  status          TEXT NOT NULL CHECK(status IN ('confirmed','tentative','cancelled')) DEFAULT 'confirmed',
  created_at      TEXT NOT NULL,
  updated_at      TEXT NOT NULL,
  recurrence_rule TEXT,
  parent_event_id TEXT,
  FOREIGN KEY (calendar_id) REFERENCES calendars(calendar_id)
);

CREATE INDEX IF NOT EXISTS idx_events_calendar_start ON events(calendar_id, start_dt);
CREATE INDEX IF NOT EXISTS idx_events_start ON events(start_dt);
CREATE INDEX IF NOT EXISTS idx_events_parent ON events(parent_event_id);

CREATE TABLE IF NOT EXISTS attendees (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id        TEXT NOT NULL,
  email           TEXT NOT NULL,
  name            TEXT,
  response_status TEXT NOT NULL CHECK(response_status IN
                    ('needsAction','accepted','declined','tentative')) DEFAULT 'needsAction',
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_attendees_event ON attendees(event_id);

CREATE TABLE IF NOT EXISTS reminders (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id       TEXT NOT NULL,
  method         TEXT NOT NULL CHECK(method IN ('popup','email')) DEFAULT 'popup',
  minutes_before INTEGER NOT NULL,
  FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_reminders_event ON reminders(event_id);

CREATE TABLE IF NOT EXISTS _counters (
  key   TEXT PRIMARY KEY,
  value INTEGER NOT NULL DEFAULT 0
);
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    """Open a SQLite connection with the project's PRAGMA defaults."""
    parent = os.path.dirname(os.path.abspath(db_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(db_path, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Create schema (idempotent)."""
    conn.executescript(SCHEMA_SQL)


def next_counter(conn: sqlite3.Connection, key: str) -> int:
    """Atomically bump and return a counter's new value."""
    conn.execute(
        "INSERT INTO _counters (key, value) VALUES (?, 0) ON CONFLICT(key) DO NOTHING",
        (key,),
    )
    conn.execute(
        "UPDATE _counters SET value = value + 1 WHERE key = ?", (key,)
    )
    row = conn.execute(
        "SELECT value FROM _counters WHERE key = ?", (key,)
    ).fetchone()
    return int(row["value"])
