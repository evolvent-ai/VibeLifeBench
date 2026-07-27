"""SQLite backend for delivery_logistics_mock.

Schema only — no bundled seed data. State enters via ``<env>/init.sql``
applied at server start.
"""
import logging
import os
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS shipments (
  shipment_id           TEXT PRIMARY KEY,
  user_id               TEXT NOT NULL,
  tracking_no           TEXT NOT NULL UNIQUE,
  carrier               TEXT NOT NULL,
  service_level         TEXT NOT NULL,
  status                TEXT NOT NULL CHECK(status IN (
    'label_created','picked_up','in_transit','out_for_delivery',
    'delivered','exception','returned','cancelled'
  )),
  sender_json           TEXT NOT NULL,
  recipient_json        TEXT NOT NULL,
  weight_kg             REAL NOT NULL,
  dimensions_json       TEXT NOT NULL DEFAULT '{}',
  declared_value_minor  INTEGER NOT NULL DEFAULT 0,
  fee_minor             INTEGER NOT NULL,
  created_at            TEXT NOT NULL,
  eta_date              TEXT NOT NULL,
  scheduled_pickup_at   TEXT,
  updated_at            TEXT NOT NULL,
  cancel_reason         TEXT
);

CREATE INDEX IF NOT EXISTS idx_shipments_user    ON shipments(user_id);
CREATE INDEX IF NOT EXISTS idx_shipments_status  ON shipments(status);
CREATE INDEX IF NOT EXISTS idx_shipments_eta     ON shipments(eta_date);

CREATE TABLE IF NOT EXISTS shipment_events (
  event_id     TEXT PRIMARY KEY,
  shipment_id  TEXT NOT NULL,
  at           TEXT NOT NULL,
  location     TEXT NOT NULL,
  status_code  TEXT NOT NULL,
  description  TEXT NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_events_ship_at ON shipment_events(shipment_id, at);

CREATE TABLE IF NOT EXISTS pickups (
  pickup_id      TEXT PRIMARY KEY,
  shipment_id    TEXT NOT NULL,
  scheduled_at   TEXT NOT NULL,
  completed_at   TEXT,
  status         TEXT NOT NULL CHECK(status IN ('pending','completed','cancelled')),
  FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_pickups_ship ON pickups(shipment_id);

CREATE TABLE IF NOT EXISTS issue_tickets (
  ticket_id              TEXT PRIMARY KEY,
  shipment_id            TEXT NOT NULL,
  issue_type             TEXT NOT NULL CHECK(issue_type IN (
    'lost','damaged','wrong_address','missing_item','delivery_failed'
  )),
  description            TEXT NOT NULL,
  status                 TEXT NOT NULL CHECK(status IN ('open','in_review','resolved','closed')),
  opened_at              TEXT NOT NULL,
  expected_response_date TEXT NOT NULL,
  resolved_at            TEXT,
  FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tickets_ship ON issue_tickets(shipment_id);

CREATE TABLE IF NOT EXISTS status_subscriptions (
  subscription_id  TEXT PRIMARY KEY,
  shipment_id      TEXT NOT NULL,
  channel          TEXT NOT NULL CHECK(channel IN ('email','sms','webhook')),
  target           TEXT NOT NULL,
  active           INTEGER NOT NULL DEFAULT 1,
  created_at       TEXT NOT NULL,
  FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_subs_ship   ON status_subscriptions(shipment_id);
CREATE INDEX IF NOT EXISTS idx_subs_active ON status_subscriptions(active);

CREATE TABLE IF NOT EXISTS notifications_outbox (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  subscription_id TEXT NOT NULL,
  payload_json    TEXT NOT NULL,
  queued_at       TEXT NOT NULL,
  sent_at         TEXT,
  FOREIGN KEY (subscription_id) REFERENCES status_subscriptions(subscription_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_outbox_sub ON notifications_outbox(subscription_id);

CREATE TABLE IF NOT EXISTS address_book (
  address_id   TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL,
  label        TEXT NOT NULL,
  recipient    TEXT NOT NULL,
  phone        TEXT NOT NULL,
  province     TEXT NOT NULL,
  city         TEXT NOT NULL,
  district     TEXT NOT NULL,
  detail       TEXT NOT NULL,
  postal_code  TEXT,
  is_default   INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_address_user ON address_book(user_id);

CREATE TABLE IF NOT EXISTS _counters (
  key   TEXT PRIMARY KEY,
  value INTEGER NOT NULL DEFAULT 0
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


def current_date() -> str:
    """Return today's UTC date.

    v3 dropped the simulated clock table — servers no longer carry a
    notion of "today".
    Date-coupled validations (``scheduled_at`` in the past, ``new_date``
    in the past) fall back to the real wall clock. Tasks that need a
    specific frame of reference must pass explicit dates.
    """
    return datetime.utcnow().strftime("%Y-%m-%d")


def next_counter(conn: sqlite3.Connection, key: str) -> int:
    """Atomically bump and return a counter's new value."""
    conn.execute(
        "INSERT INTO _counters (key, value) VALUES (?, 0) ON CONFLICT(key) DO NOTHING",
        (key,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE key = ?", (key,))
    row = conn.execute("SELECT value FROM _counters WHERE key = ?", (key,)).fetchone()
    return int(row["value"])
