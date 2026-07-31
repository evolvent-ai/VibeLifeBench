"""SQLite backend for notification_hub_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).

Design note: notifications are pre-seeded historical/static rows. The server
has no clock and never auto-generates time-based events. Creating a
subscription only records intent; new notifications arrive solely as
out-of-band SQL mutations injected by the orchestrator during a task.
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS subscriptions (
  subscription_id  TEXT PRIMARY KEY,
  user_id          TEXT NOT NULL,
  source           TEXT NOT NULL,
  type             TEXT NOT NULL CHECK(type IN
                     ('price_drop','restock','policy_update','new_content',
                      'price_target','keyword')),
  target           TEXT NOT NULL,
  condition_json   TEXT,
  status           TEXT NOT NULL DEFAULT 'active'
                     CHECK(status IN ('active','paused','deleted')),
  created_at       TEXT NOT NULL,
  updated_at       TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_subs_user   ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subs_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_subs_source ON subscriptions(source);

CREATE TABLE IF NOT EXISTS notifications (
  notification_id  TEXT PRIMARY KEY,
  user_id          TEXT NOT NULL,
  source           TEXT NOT NULL,
  type             TEXT NOT NULL,
  subscription_id  TEXT,
  title            TEXT NOT NULL,
  body             TEXT,
  payload_json     TEXT,
  created_at       TEXT NOT NULL,
  read             INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);

CREATE INDEX IF NOT EXISTS idx_notif_user_created ON notifications(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_notif_read         ON notifications(read);
CREATE INDEX IF NOT EXISTS idx_notif_source       ON notifications(source);

CREATE TABLE IF NOT EXISTS price_alerts (
  alert_id           TEXT PRIMARY KEY,
  user_id            TEXT NOT NULL,
  item_ref           TEXT NOT NULL,
  target_price_minor INTEGER NOT NULL,
  currency           TEXT NOT NULL DEFAULT 'CNY',
  status             TEXT NOT NULL DEFAULT 'active'
                       CHECK(status IN ('active','triggered','cancelled')),
  created_at         TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_alerts_user   ON price_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON price_alerts(status);

CREATE TABLE IF NOT EXISTS official_accounts (
  account_id   TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  category     TEXT,
  description  TEXT
);

CREATE TABLE IF NOT EXISTS official_account_subscriptions (
  user_id      TEXT NOT NULL,
  account_id   TEXT NOT NULL,
  subscribed_at TEXT NOT NULL,
  PRIMARY KEY (user_id, account_id),
  FOREIGN KEY (account_id) REFERENCES official_accounts(account_id)
);

CREATE TABLE IF NOT EXISTS official_account_posts (
  post_id      TEXT PRIMARY KEY,
  account_id   TEXT NOT NULL,
  title        TEXT NOT NULL,
  summary      TEXT,
  url          TEXT,
  published_at TEXT NOT NULL,
  FOREIGN KEY (account_id) REFERENCES official_accounts(account_id)
);

CREATE INDEX IF NOT EXISTS idx_posts_account_pub ON official_account_posts(account_id, published_at);

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
