import os
import sqlite3
import logging

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS hotels (
  hotel_id          TEXT PRIMARY KEY,
  name              TEXT NOT NULL,
  city              TEXT NOT NULL,
  district          TEXT,
  geo_lat           REAL NOT NULL,
  geo_lng           REAL NOT NULL,
  star_rating       INTEGER NOT NULL CHECK(star_rating BETWEEN 1 AND 5),
  user_rating       REAL NOT NULL CHECK(user_rating BETWEEN 0 AND 10),
  user_rating_count INTEGER NOT NULL DEFAULT 0,
  amenities_json    TEXT NOT NULL,
  address_json      TEXT NOT NULL,
  policies_json     TEXT NOT NULL,
  description       TEXT,
  capacity_estimate INTEGER NOT NULL DEFAULT 20
);

CREATE INDEX IF NOT EXISTS idx_hotels_city     ON hotels(city);
CREATE INDEX IF NOT EXISTS idx_hotels_district ON hotels(district);

CREATE TABLE IF NOT EXISTS rate_plans (
  rate_plan_row_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  hotel_id             TEXT NOT NULL,
  date                 TEXT NOT NULL,
  room_type            TEXT NOT NULL,
  flavor               TEXT NOT NULL CHECK(flavor IN ('flex','semi','prepaid')),
  nightly_price        INTEGER NOT NULL,
  currency             TEXT NOT NULL DEFAULT 'JPY',
  inventory_remaining  INTEGER NOT NULL,
  inventory_capacity   INTEGER NOT NULL,
  cancellation_policy  TEXT NOT NULL,
  refundable_until     TEXT,
  breakfast_included   INTEGER NOT NULL DEFAULT 0,
  max_occupancy        INTEGER NOT NULL DEFAULT 2,
  UNIQUE (hotel_id, date, room_type, flavor),
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_rateplans_hotel_date ON rate_plans(hotel_id, date);

CREATE TABLE IF NOT EXISTS reservations (
  reservation_id        TEXT PRIMARY KEY,
  confirmation_code     TEXT NOT NULL UNIQUE,
  user_id               TEXT NOT NULL,
  hotel_id              TEXT NOT NULL,
  check_in              TEXT NOT NULL,
  check_out             TEXT NOT NULL,
  room_type             TEXT NOT NULL,
  flavor                TEXT NOT NULL,
  status                TEXT NOT NULL CHECK(status IN ('confirmed','modified','cancelled','walked','checked_out')),
  total_charged         INTEGER NOT NULL,
  currency              TEXT NOT NULL DEFAULT 'JPY',
  refundable            INTEGER NOT NULL DEFAULT 1,
  refundable_until      TEXT,
  created_at            TEXT NOT NULL,
  updated_at            TEXT NOT NULL,
  guest_profile_json    TEXT NOT NULL,
  payment_method_id     TEXT NOT NULL,
  special_requests_json TEXT NOT NULL DEFAULT '{}',
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);

CREATE INDEX IF NOT EXISTS idx_reservations_user   ON reservations(user_id);
CREATE INDEX IF NOT EXISTS idx_reservations_hotel  ON reservations(hotel_id);
CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);

CREATE TABLE IF NOT EXISTS reservation_nights (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  reservation_id     TEXT NOT NULL,
  date               TEXT NOT NULL,
  rate_plan_row_id   INTEGER NOT NULL,
  nightly_price      INTEGER NOT NULL,
  FOREIGN KEY (reservation_id)   REFERENCES reservations(reservation_id) ON DELETE CASCADE,
  FOREIGN KEY (rate_plan_row_id) REFERENCES rate_plans(rate_plan_row_id)
);

CREATE INDEX IF NOT EXISTS idx_resnights_res  ON reservation_nights(reservation_id);
CREATE INDEX IF NOT EXISTS idx_resnights_date ON reservation_nights(date);

CREATE TABLE IF NOT EXISTS special_requests (
  ticket_id       TEXT PRIMARY KEY,
  reservation_id  TEXT NOT NULL,
  text            TEXT NOT NULL,
  status          TEXT NOT NULL,
  created_at      TEXT NOT NULL,
  updated_at      TEXT NOT NULL,
  FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sreq_res ON special_requests(reservation_id);

CREATE TABLE IF NOT EXISTS notifications (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT NOT NULL,
  channel       TEXT NOT NULL CHECK(channel IN ('email','sms','webhook','system')),
  payload_json  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at);

CREATE TABLE IF NOT EXISTS scenario_clock (
  clock_id     TEXT PRIMARY KEY CHECK(clock_id = 'default'),
  scenario_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS _counters (
  name  TEXT PRIMARY KEY,
  value INTEGER NOT NULL
);
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    """Return a SQLite connection with the project's PRAGMA defaults applied."""
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
    conn.executescript(SCHEMA_SQL)


def next_counter(conn: sqlite3.Connection, name: str) -> int:
    """Atomically bump and return the named counter's new value."""
    conn.execute(
        "INSERT INTO _counters (name, value) VALUES (?, 0) "
        "ON CONFLICT(name) DO NOTHING",
        (name,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE name = ?", (name,))
    row = conn.execute("SELECT value FROM _counters WHERE name = ?", (name,)).fetchone()
    return int(row["value"])
