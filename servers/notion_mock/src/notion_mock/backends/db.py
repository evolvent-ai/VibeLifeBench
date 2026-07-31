"""SQLite backend for notion_mock.

Schema-only — no bundled seed data. State enters via ``init.sql`` under
the env directory passed to ``--env``. The v3 server always opens a
fresh scratch DB on cold start (caller wipes it on exit).
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
  user_id     TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  avatar_url  TEXT,
  email       TEXT,
  type        TEXT NOT NULL DEFAULT 'person' CHECK(type IN ('person','bot'))
);

CREATE TABLE IF NOT EXISTS workspaces (
  workspace_id    TEXT PRIMARY KEY,
  name            TEXT NOT NULL,
  owner_user_id   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pages (
  page_id            TEXT PRIMARY KEY,
  parent_type        TEXT NOT NULL CHECK(parent_type IN ('workspace','page_id','database_id')),
  parent_id          TEXT NOT NULL,
  title              TEXT NOT NULL DEFAULT '',
  archived           INTEGER NOT NULL DEFAULT 0,
  created_time       TEXT NOT NULL,
  last_edited_time   TEXT NOT NULL,
  properties_json    TEXT NOT NULL DEFAULT '{}',
  icon               TEXT,
  cover              TEXT
);

CREATE INDEX IF NOT EXISTS idx_pages_parent ON pages(parent_type, parent_id);

CREATE TABLE IF NOT EXISTS databases (
  database_id        TEXT PRIMARY KEY,
  parent_type        TEXT NOT NULL CHECK(parent_type IN ('workspace','page_id')),
  parent_id          TEXT NOT NULL,
  title              TEXT NOT NULL DEFAULT '',
  schema_json        TEXT NOT NULL DEFAULT '{}',
  archived           INTEGER NOT NULL DEFAULT 0,
  created_time       TEXT NOT NULL,
  last_edited_time   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_databases_parent ON databases(parent_type, parent_id);

CREATE TABLE IF NOT EXISTS database_rows (
  row_id             TEXT PRIMARY KEY,  -- also acts as a page_id (Notion DB rows are pages)
  database_id        TEXT NOT NULL,
  properties_json    TEXT NOT NULL DEFAULT '{}',
  created_time       TEXT NOT NULL,
  last_edited_time   TEXT NOT NULL,
  archived           INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (database_id) REFERENCES databases(database_id)
);

CREATE INDEX IF NOT EXISTS idx_dbrows_db ON database_rows(database_id);

CREATE TABLE IF NOT EXISTS blocks (
  block_id            TEXT PRIMARY KEY,
  parent_block_id     TEXT,       -- nullable: top-level blocks are page children
  parent_page_id      TEXT,       -- nullable: nested blocks belong to a parent block
  type                TEXT NOT NULL,
  content_json        TEXT NOT NULL DEFAULT '{}',
  has_children        INTEGER NOT NULL DEFAULT 0,
  archived            INTEGER NOT NULL DEFAULT 0,
  position            INTEGER NOT NULL DEFAULT 0,
  created_time        TEXT NOT NULL,
  last_edited_time    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_blocks_parent_page  ON blocks(parent_page_id, position);
CREATE INDEX IF NOT EXISTS idx_blocks_parent_block ON blocks(parent_block_id, position);

CREATE TABLE IF NOT EXISTS comments (
  comment_id       TEXT PRIMARY KEY,
  parent_page_id   TEXT,
  discussion_id    TEXT,
  content_json     TEXT NOT NULL DEFAULT '{}',
  created_by       TEXT,
  created_time     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS counters (
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
    """Create the notion_mock schema (idempotent)."""
    conn.executescript(SCHEMA_SQL)
