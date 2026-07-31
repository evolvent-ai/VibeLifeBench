"""SQLite backend for banking_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS accounts (
  account_id     TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL,
  type           TEXT NOT NULL CHECK(type IN ('checking','savings','money_market','education_fund')),
  name           TEXT NOT NULL,
  balance_minor  INTEGER NOT NULL DEFAULT 0,
  currency       TEXT NOT NULL DEFAULT 'CNY',
  opened_at      TEXT NOT NULL,
  frozen         INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_accounts_user ON accounts(user_id);

CREATE TABLE IF NOT EXISTS transactions (
  tx_id                 TEXT PRIMARY KEY,
  account_id            TEXT NOT NULL,
  posted_at             TEXT NOT NULL,
  amount_minor          INTEGER NOT NULL,
  kind                  TEXT NOT NULL CHECK(kind IN
                          ('deposit','withdrawal','transfer_in','transfer_out',
                           'payment','fee','interest')),
  counterparty          TEXT,
  memo                  TEXT,
  balance_after_minor   INTEGER NOT NULL,
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE INDEX IF NOT EXISTS idx_tx_account_posted ON transactions(account_id, posted_at);
CREATE INDEX IF NOT EXISTS idx_tx_kind ON transactions(kind);

CREATE TABLE IF NOT EXISTS payees (
  payee_id            TEXT PRIMARY KEY,
  user_id             TEXT NOT NULL,
  name                TEXT NOT NULL,
  account_no          TEXT NOT NULL,
  account_no_masked   TEXT NOT NULL,
  bank_name           TEXT NOT NULL,
  added_at            TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_payees_user ON payees(user_id);

CREATE TABLE IF NOT EXISTS recurring_payments (
  schedule_id     TEXT PRIMARY KEY,
  user_id         TEXT NOT NULL,
  account_id      TEXT NOT NULL,
  payee_id        TEXT NOT NULL,
  amount_minor    INTEGER NOT NULL,
  freq            TEXT NOT NULL CHECK(freq IN ('daily','weekly','monthly')),
  start_date      TEXT NOT NULL,
  end_date        TEXT,
  next_run_date   TEXT NOT NULL,
  status          TEXT NOT NULL CHECK(status IN ('active','paused','cancelled','ended')),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id),
  FOREIGN KEY (payee_id)   REFERENCES payees(payee_id)
);

CREATE INDEX IF NOT EXISTS idx_recurring_user   ON recurring_payments(user_id);
CREATE INDEX IF NOT EXISTS idx_recurring_status ON recurring_payments(status);
CREATE INDEX IF NOT EXISTS idx_recurring_next   ON recurring_payments(next_run_date);

CREATE TABLE IF NOT EXISTS pending_payments (
  pending_id      TEXT PRIMARY KEY,
  account_id      TEXT NOT NULL,
  payee_id        TEXT NOT NULL,
  amount_minor    INTEGER NOT NULL,
  memo            TEXT,
  scheduled_for   TEXT NOT NULL,
  status          TEXT NOT NULL CHECK(status IN ('pending','posted','cancelled')),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id),
  FOREIGN KEY (payee_id)   REFERENCES payees(payee_id)
);

CREATE INDEX IF NOT EXISTS idx_pending_sched ON pending_payments(scheduled_for, status);

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
