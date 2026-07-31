import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS cards (
  card_id                    TEXT PRIMARY KEY,
  user_id                    TEXT NOT NULL,
  issuer                     TEXT NOT NULL,
  product_name               TEXT NOT NULL,
  masked_no                  TEXT NOT NULL,
  type                       TEXT NOT NULL,                -- Visa | Mastercard | UnionPay | ...
  credit_limit_minor         INTEGER NOT NULL,
  available_credit_minor     INTEGER NOT NULL,
  statement_balance_minor    INTEGER NOT NULL DEFAULT 0,
  unbilled_balance_minor     INTEGER NOT NULL DEFAULT 0,
  min_payment_due_minor      INTEGER NOT NULL DEFAULT 0,
  due_date                   TEXT,
  cycle_start_day            INTEGER NOT NULL DEFAULT 1,
  cycle_end_day              INTEGER NOT NULL DEFAULT 28,
  grace_period_days          INTEGER NOT NULL DEFAULT 14,
  status                     TEXT NOT NULL DEFAULT 'active'
                             CHECK(status IN ('active','frozen','expired','closed')),
  interest_apr_bp            INTEGER NOT NULL DEFAULT 1800
);

CREATE INDEX IF NOT EXISTS idx_cards_user ON cards(user_id);

CREATE TABLE IF NOT EXISTS statements (
  statement_id               TEXT PRIMARY KEY,
  card_id                    TEXT NOT NULL,
  period_start               TEXT NOT NULL,
  period_end                 TEXT NOT NULL,
  opening_balance_minor      INTEGER NOT NULL DEFAULT 0,
  new_charges_minor          INTEGER NOT NULL DEFAULT 0,
  payments_minor             INTEGER NOT NULL DEFAULT 0,
  closing_balance_minor      INTEGER NOT NULL DEFAULT 0,
  min_payment_due_minor      INTEGER NOT NULL DEFAULT 0,
  due_date                   TEXT NOT NULL,
  status                     TEXT NOT NULL DEFAULT 'open'
                             CHECK(status IN ('open','paid','overdue','partial')),
  FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_statements_card    ON statements(card_id, period_end);
CREATE INDEX IF NOT EXISTS idx_statements_status  ON statements(status);

CREATE TABLE IF NOT EXISTS statement_lines (
  line_id                    TEXT PRIMARY KEY,
  statement_id               TEXT NOT NULL,
  posted_at                  TEXT NOT NULL,
  amount_minor               INTEGER NOT NULL,             -- + for charge/fee/interest, - for refund/payment/adj
  merchant_name              TEXT NOT NULL DEFAULT '',
  mcc                        TEXT,
  category                   TEXT,
  kind                       TEXT NOT NULL
                             CHECK(kind IN ('purchase','refund','payment','fee','interest','adjustment')),
  FOREIGN KEY (statement_id) REFERENCES statements(statement_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_lines_statement ON statement_lines(statement_id, posted_at);

CREATE TABLE IF NOT EXISTS unbilled_transactions (
  tx_id                      TEXT PRIMARY KEY,
  card_id                    TEXT NOT NULL,
  posted_at                  TEXT NOT NULL,
  amount_minor               INTEGER NOT NULL,
  merchant_name              TEXT NOT NULL DEFAULT '',
  mcc                        TEXT,
  category                   TEXT,
  kind                       TEXT NOT NULL
                             CHECK(kind IN ('purchase','refund','payment','fee','interest','adjustment')),
  FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_unbilled_card ON unbilled_transactions(card_id, posted_at);

CREATE TABLE IF NOT EXISTS payments (
  payment_id                       TEXT PRIMARY KEY,
  card_id                          TEXT NOT NULL,
  posted_at                        TEXT NOT NULL,
  amount_minor                     INTEGER NOT NULL,
  source_hint                      TEXT NOT NULL DEFAULT '',
  applied_to_statement_minor       INTEGER NOT NULL DEFAULT 0,
  applied_to_unbilled_minor        INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_payments_card ON payments(card_id, posted_at);

CREATE TABLE IF NOT EXISTS disputes (
  dispute_id                 TEXT PRIMARY KEY,
  card_id                    TEXT NOT NULL,
  tx_id                      TEXT NOT NULL,
  reason                     TEXT NOT NULL DEFAULT '',
  status                     TEXT NOT NULL DEFAULT 'under_review'
                             CHECK(status IN ('under_review','approved','denied','withdrawn')),
  opened_at                  TEXT NOT NULL,
  expected_resolution_date   TEXT NOT NULL,
  resolved_at                TEXT,
  FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_disputes_card   ON disputes(card_id, opened_at);
CREATE INDEX IF NOT EXISTS idx_disputes_tx     ON disputes(tx_id);
CREATE INDEX IF NOT EXISTS idx_disputes_status ON disputes(status);

CREATE TABLE IF NOT EXISTS rewards_balances (
  card_id                    TEXT PRIMARY KEY,
  points_balance             INTEGER NOT NULL DEFAULT 0,
  ytd_earned                 INTEGER NOT NULL DEFAULT 0,
  lifetime_earned            INTEGER NOT NULL DEFAULT 0,
  updated_at                 TEXT NOT NULL,
  FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rewards_ledger (
  ledger_id                  TEXT PRIMARY KEY,
  card_id                    TEXT NOT NULL,
  posted_at                  TEXT NOT NULL,
  kind                       TEXT NOT NULL
                             CHECK(kind IN ('earn','redeem','adjust','expire')),
  delta                      INTEGER NOT NULL,
  balance_after              INTEGER NOT NULL,
  note                       TEXT,
  FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_ledger_card ON rewards_ledger(card_id, posted_at);

CREATE TABLE IF NOT EXISTS _counters (
  key                        TEXT PRIMARY KEY,
  value                      INTEGER NOT NULL DEFAULT 0
);
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    """Return a SQLite connection with project PRAGMA defaults applied."""
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


def next_counter(conn: sqlite3.Connection, key: str) -> int:
    """Atomically bump and return a counter's new value."""
    conn.execute(
        "INSERT INTO _counters (key, value) VALUES (?, 0) ON CONFLICT(key) DO NOTHING",
        (key,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE key = ?", (key,))
    row = conn.execute("SELECT value FROM _counters WHERE key = ?", (key,)).fetchone()
    return int(row["value"])
