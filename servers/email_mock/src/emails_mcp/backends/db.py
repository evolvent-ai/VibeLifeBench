"""SQLite backend for emails_mcp.

Schema-only — no bundled seed data. Tables mirror the upstream PostgreSQL
``email.*`` schema flattened to plain SQLite tables (no schema prefix):
``folders``, ``messages``, ``attachments``, ``drafts``, ``sent_log``,
``account_config``, ``_counters``.

v3: dropped the simulated-clock singleton (servers no longer carry a
notion of "today").
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS account_config (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  email       TEXT NOT NULL,
  name        TEXT,
  created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS folders (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT NOT NULL UNIQUE,
  delimiter       TEXT NOT NULL DEFAULT '/',
  flags_json      TEXT NOT NULL DEFAULT '[]',
  message_count   INTEGER NOT NULL DEFAULT 0,
  unread_count    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS messages (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  folder_id         INTEGER NOT NULL,
  message_id        TEXT,
  subject           TEXT,
  from_addr         TEXT,
  to_addr_json      TEXT NOT NULL DEFAULT '[]',
  cc_addr_json      TEXT NOT NULL DEFAULT '[]',
  bcc_addr_json     TEXT NOT NULL DEFAULT '[]',
  date              TEXT NOT NULL,
  body_text         TEXT,
  body_html         TEXT,
  is_read           INTEGER NOT NULL DEFAULT 0,
  is_important      INTEGER NOT NULL DEFAULT 0,
  is_flagged        INTEGER NOT NULL DEFAULT 0,
  in_reply_to       TEXT,
  references_header TEXT,
  headers_json      TEXT NOT NULL DEFAULT '{}',
  uid               INTEGER,
  size              INTEGER NOT NULL DEFAULT 0,
  created_at        TEXT NOT NULL,
  FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_messages_folder ON messages(folder_id);
CREATE INDEX IF NOT EXISTS idx_messages_date   ON messages(date DESC);
CREATE INDEX IF NOT EXISTS idx_messages_from   ON messages(from_addr);

CREATE TABLE IF NOT EXISTS attachments (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id    INTEGER NOT NULL,
  filename      TEXT NOT NULL,
  content_type  TEXT,
  size          INTEGER NOT NULL DEFAULT 0,
  content_b64   TEXT,
  content_id    TEXT,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_attachments_msg ON attachments(message_id);

CREATE TABLE IF NOT EXISTS drafts (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  subject       TEXT,
  from_addr     TEXT,
  to_addr_json  TEXT NOT NULL DEFAULT '[]',
  cc_addr_json  TEXT NOT NULL DEFAULT '[]',
  bcc_addr_json TEXT NOT NULL DEFAULT '[]',
  body_text     TEXT,
  body_html     TEXT,
  in_reply_to   TEXT,
  created_at    TEXT NOT NULL,
  updated_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_drafts_updated ON drafts(updated_at DESC);

CREATE TABLE IF NOT EXISTS sent_log (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id  INTEGER,
  sent_at     TEXT NOT NULL,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE SET NULL
);

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
