"""SQLite backend for health_tracker_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS metrics (
  metric_id    TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL,
  type         TEXT NOT NULL CHECK(type IN
                 ('weight','steps','heart_rate','sleep_minutes',
                  'blood_pressure','body_fat','finger_pain','score')),
  value        REAL NOT NULL,
  value_text   TEXT,
  unit         TEXT NOT NULL,
  recorded_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_metrics_user_type ON metrics(user_id, type, recorded_at);

CREATE TABLE IF NOT EXISTS workouts (
  workout_id    TEXT PRIMARY KEY,
  user_id       TEXT NOT NULL,
  type          TEXT NOT NULL,
  duration_min  INTEGER NOT NULL,
  calories      INTEGER,
  distance_m    INTEGER,
  started_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_workouts_user ON workouts(user_id, started_at);

CREATE TABLE IF NOT EXISTS goals (
  goal_id     TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL,
  type        TEXT NOT NULL,
  target      REAL NOT NULL,
  unit        TEXT NOT NULL,
  period      TEXT NOT NULL CHECK(period IN ('day','week','month','once')),
  direction   TEXT NOT NULL CHECK(direction IN ('at_least','at_most')),
  start_date  TEXT NOT NULL,
  status      TEXT NOT NULL CHECK(status IN ('active','achieved','abandoned'))
);

CREATE INDEX IF NOT EXISTS idx_goals_user ON goals(user_id, status);

CREATE TABLE IF NOT EXISTS nutrition_logs (
  nutrition_id  TEXT PRIMARY KEY,
  user_id       TEXT NOT NULL,
  meal          TEXT NOT NULL CHECK(meal IN ('breakfast','lunch','dinner','snack')),
  description   TEXT,
  calories      INTEGER NOT NULL,
  protein_g     REAL,
  carbs_g       REAL,
  fat_g         REAL,
  logged_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_nutrition_user ON nutrition_logs(user_id, logged_at);

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
