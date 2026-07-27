"""SQLite backend for listing_platform_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS listings (
  listing_id     TEXT PRIMARY KEY,
  category       TEXT NOT NULL CHECK(category IN ('rent','sale_house','used_car','secondhand')),
  title          TEXT NOT NULL,
  city           TEXT NOT NULL,
  district       TEXT,
  community       TEXT,
  price_minor    INTEGER NOT NULL,           -- rent: monthly rent (分); sale/car/secondhand: total price (分)
  area_sqm       REAL,                       -- floor area for housing listings
  rooms          INTEGER,                    -- bedroom count for housing listings
  metro          TEXT,                       -- nearest metro line/station, e.g. '2号线·静安寺站 350m'
  attrs_json     TEXT NOT NULL DEFAULT '{}', -- flexible per-category attributes (orientation, floor, mileage...)
  description    TEXT,
  photos_json    TEXT NOT NULL DEFAULT '[]', -- list of text photo captions (offline; no binary)
  agent_id       TEXT,                       -- listing agent (NULL for user self-listings)
  owner_user_id  TEXT,                       -- set when a user self-lists via post_listing
  status         TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','delisted')),
  listed_at      TEXT NOT NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

CREATE INDEX IF NOT EXISTS idx_listings_cat   ON listings(category, status);
CREATE INDEX IF NOT EXISTS idx_listings_city  ON listings(city, district);
CREATE INDEX IF NOT EXISTS idx_listings_price ON listings(category, price_minor);
CREATE INDEX IF NOT EXISTS idx_listings_owner ON listings(owner_user_id);

CREATE TABLE IF NOT EXISTS agents (
  agent_id     TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  agency       TEXT NOT NULL,             -- e.g. 链家 / 我爱我家
  phone        TEXT NOT NULL,
  rating       REAL NOT NULL DEFAULT 0,   -- 0.0 - 5.0
  deals_count  INTEGER NOT NULL DEFAULT 0,
  service_area TEXT                       -- districts/communities the agent covers
);

CREATE TABLE IF NOT EXISTS saved_listings (
  user_id     TEXT NOT NULL,
  listing_id  TEXT NOT NULL,
  saved_at    TEXT NOT NULL,
  PRIMARY KEY (user_id, listing_id),
  FOREIGN KEY (listing_id) REFERENCES listings(listing_id)
);

CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_listings(user_id);

CREATE TABLE IF NOT EXISTS viewings (
  viewing_id   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL,
  listing_id   TEXT NOT NULL,
  agent_id     TEXT,
  scheduled_at TEXT NOT NULL,             -- ISO-8601 with timezone
  status       TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled','cancelled')),
  created_at   TEXT NOT NULL,
  FOREIGN KEY (listing_id) REFERENCES listings(listing_id)
);

CREATE INDEX IF NOT EXISTS idx_viewings_user ON viewings(user_id, status);

CREATE TABLE IF NOT EXISTS contacts (
  contact_id  TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL,
  listing_id  TEXT NOT NULL,
  agent_id    TEXT,
  message     TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  FOREIGN KEY (listing_id) REFERENCES listings(listing_id)
);

CREATE INDEX IF NOT EXISTS idx_contacts_user ON contacts(user_id);

CREATE TABLE IF NOT EXISTS market_stats (
  stat_id            TEXT PRIMARY KEY,
  area               TEXT NOT NULL,        -- 小区 or 板块/district name (matched by get_market_stats)
  city               TEXT,
  category           TEXT NOT NULL CHECK(category IN ('rent','sale_house','used_car','secondhand')),
  avg_price_minor    INTEGER NOT NULL,     -- avg transaction price (rent: 月租分; sale: 总价分 or 单价分/㎡)
  unit               TEXT NOT NULL,        -- 'per_month' | 'total' | 'per_sqm'
  sample_size        INTEGER NOT NULL DEFAULT 0,
  period             TEXT NOT NULL         -- e.g. '2026-04' transaction window
);

CREATE INDEX IF NOT EXISTS idx_stats_area ON market_stats(area);

CREATE TABLE IF NOT EXISTS search_subscriptions (
  subscription_id TEXT PRIMARY KEY,
  user_id         TEXT NOT NULL,
  query_json      TEXT NOT NULL,           -- saved search criteria
  created_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_subs_user ON search_subscriptions(user_id);

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
