"""SQLite backend: connection, schema, helpers.

Schema is the only thing shipped inside the package. State enters via
the env directory's ``init.sql``.
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS accounts (
  account_id     TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL,
  broker         TEXT NOT NULL,
  account_type   TEXT NOT NULL CHECK(account_type IN ('cash','margin')),
  cash_minor     INTEGER NOT NULL DEFAULT 0,
  opened_at      TEXT NOT NULL,
  status         TEXT NOT NULL DEFAULT 'active'
);
CREATE INDEX IF NOT EXISTS idx_accounts_user ON accounts(user_id);

CREATE TABLE IF NOT EXISTS positions (
  position_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id       TEXT NOT NULL,
  symbol           TEXT NOT NULL,
  kind             TEXT NOT NULL CHECK(kind IN ('stock','fund')),
  qty_milli        INTEGER NOT NULL DEFAULT 0,
  avg_cost_minor   INTEGER NOT NULL DEFAULT 0,
  UNIQUE(account_id, symbol),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_positions_account ON positions(account_id);

CREATE TABLE IF NOT EXISTS orders (
  order_id           TEXT PRIMARY KEY,
  account_id         TEXT NOT NULL,
  symbol             TEXT NOT NULL,
  side               TEXT NOT NULL CHECK(side IN ('buy','sell')),
  qty_milli          INTEGER NOT NULL,
  order_type         TEXT NOT NULL CHECK(order_type IN ('market','limit')),
  limit_price_minor  INTEGER,
  tif                TEXT NOT NULL DEFAULT 'day',
  status             TEXT NOT NULL CHECK(status IN ('pending','filled','cancelled','rejected')),
  placed_at          TEXT NOT NULL,
  filled_at          TEXT,
  fill_price_minor   INTEGER,
  FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_orders_account ON orders(account_id);
CREATE INDEX IF NOT EXISTS idx_orders_status  ON orders(status);

CREATE TABLE IF NOT EXISTS symbols (
  symbol      TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  kind        TEXT NOT NULL CHECK(kind IN ('stock','fund'))
);

CREATE TABLE IF NOT EXISTS quotes_daily (
  symbol       TEXT NOT NULL,
  date         TEXT NOT NULL,
  open_minor   INTEGER NOT NULL,
  close_minor  INTEGER NOT NULL,
  high_minor   INTEGER NOT NULL,
  low_minor    INTEGER NOT NULL,
  volume       INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (symbol, date)
);
CREATE INDEX IF NOT EXISTS idx_quotes_date ON quotes_daily(date);

CREATE TABLE IF NOT EXISTS funds (
  fund_code         TEXT PRIMARY KEY,
  fund_name         TEXT NOT NULL,
  category          TEXT NOT NULL CHECK(category IN ('money_market','bond','equity','mixed','index')),
  current_nav_minor INTEGER NOT NULL,
  ytd_return_bp     INTEGER NOT NULL DEFAULT 0,
  risk_level        INTEGER NOT NULL DEFAULT 3,
  manager           TEXT,
  inception         TEXT
);

CREATE TABLE IF NOT EXISTS fund_navs (
  fund_code  TEXT NOT NULL,
  date       TEXT NOT NULL,
  nav_minor  INTEGER NOT NULL,
  PRIMARY KEY (fund_code, date),
  FOREIGN KEY (fund_code) REFERENCES funds(fund_code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS portfolio_snapshots (
  account_id            TEXT NOT NULL,
  date                  TEXT NOT NULL,
  cash_minor            INTEGER NOT NULL,
  positions_value_minor INTEGER NOT NULL,
  total_value_minor     INTEGER NOT NULL,
  PRIMARY KEY (account_id, date),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS _counters (
  name  TEXT PRIMARY KEY,
  value INTEGER NOT NULL DEFAULT 0
);
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    """Open a SQLite connection with project PRAGMA defaults."""
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


def latest_quote_date(conn: sqlite3.Connection, symbol: str) -> str | None:
    """Return the most recent ``quotes_daily.date`` for ``symbol``, or None."""
    row = conn.execute(
        "SELECT MAX(date) AS d FROM quotes_daily WHERE symbol = ?",
        (symbol,),
    ).fetchone()
    return row["d"] if row and row["d"] else None


def latest_snapshot_date(conn: sqlite3.Connection, account_id: str) -> str | None:
    """Return the most recent ``portfolio_snapshots.date`` for ``account_id``."""
    row = conn.execute(
        "SELECT MAX(date) AS d FROM portfolio_snapshots WHERE account_id = ?",
        (account_id,),
    ).fetchone()
    return row["d"] if row and row["d"] else None


def next_counter(conn: sqlite3.Connection, key: str) -> int:
    """Atomically bump and return a counter's new value."""
    conn.execute(
        "INSERT INTO _counters (name, value) VALUES (?, 0) ON CONFLICT(name) DO NOTHING",
        (key,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE name = ?", (key,))
    row = conn.execute(
        "SELECT value FROM _counters WHERE name = ?", (key,)
    ).fetchone()
    return int(row["value"])
