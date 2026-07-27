"""SQLite backend for review_platform_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).

Conventions:
- Money in integer minor units (分; ¥1 = 100).
- Ratings stored as INTEGER tenths on a 1.0-5.0 scale (e.g. 46 -> 4.6).
- Timestamps ISO-8601; dates ISO ``YYYY-MM-DD``.
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS merchants (
  merchant_id        TEXT PRIMARY KEY,
  name               TEXT NOT NULL,
  category           TEXT NOT NULL CHECK(category IN
                       ('restaurant','venue','vet','home_service')),
  city               TEXT NOT NULL,
  area               TEXT NOT NULL,
  address            TEXT NOT NULL,
  phone              TEXT,
  rating_tenths      INTEGER NOT NULL DEFAULT 0,
  review_count       INTEGER NOT NULL DEFAULT 0,
  avg_price_minor    INTEGER NOT NULL DEFAULT 0,
  price_band         TEXT NOT NULL CHECK(price_band IN ('$','$$','$$$','$$$$')),
  hours              TEXT,
  tags               TEXT,
  has_private_room   INTEGER NOT NULL DEFAULT 0,
  max_party_size     INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_merchants_cat  ON merchants(category);
CREATE INDEX IF NOT EXISTS idx_merchants_area ON merchants(city, area);

CREATE TABLE IF NOT EXISTS reviews (
  review_id      TEXT PRIMARY KEY,
  merchant_id    TEXT NOT NULL,
  user_id        TEXT NOT NULL,
  rating         INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
  body           TEXT NOT NULL,
  image_captions TEXT,
  created_at     TEXT NOT NULL,
  FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE INDEX IF NOT EXISTS idx_reviews_merchant ON reviews(merchant_id, created_at);

CREATE TABLE IF NOT EXISTS deals (
  deal_id        TEXT PRIMARY KEY,
  merchant_id    TEXT NOT NULL,
  title          TEXT NOT NULL,
  description    TEXT,
  price_minor    INTEGER NOT NULL,
  list_price_minor INTEGER NOT NULL,
  serves         INTEGER NOT NULL DEFAULT 1,
  valid_until    TEXT,
  status         TEXT NOT NULL CHECK(status IN ('active','sold_out','expired')),
  FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE INDEX IF NOT EXISTS idx_deals_merchant ON deals(merchant_id);

CREATE TABLE IF NOT EXISTS reservations (
  reservation_id TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL,
  merchant_id    TEXT NOT NULL,
  datetime       TEXT NOT NULL,
  party_size     INTEGER NOT NULL,
  deal_id        TEXT,
  status         TEXT NOT NULL CHECK(status IN ('confirmed','cancelled')),
  created_at     TEXT NOT NULL,
  FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
  FOREIGN KEY (deal_id)     REFERENCES deals(deal_id)
);

CREATE INDEX IF NOT EXISTS idx_reservations_user ON reservations(user_id, datetime);

CREATE TABLE IF NOT EXISTS merchant_qa (
  qa_id        TEXT PRIMARY KEY,
  merchant_id  TEXT NOT NULL,
  user_id      TEXT NOT NULL,
  question     TEXT NOT NULL,
  answer       TEXT,
  answered_by  TEXT,
  created_at   TEXT NOT NULL,
  FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE INDEX IF NOT EXISTS idx_qa_merchant ON merchant_qa(merchant_id, created_at);

CREATE TABLE IF NOT EXISTS saved_merchants (
  user_id      TEXT NOT NULL,
  merchant_id  TEXT NOT NULL,
  saved_at     TEXT NOT NULL,
  PRIMARY KEY (user_id, merchant_id),
  FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_merchants(user_id);

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
