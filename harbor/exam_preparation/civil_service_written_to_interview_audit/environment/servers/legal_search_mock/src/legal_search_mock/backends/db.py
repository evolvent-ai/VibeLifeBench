"""SQLite backend for legal_search_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).

Models a Chinese legal-research corpus: case judgments, statutes with their
articles, citations linking cases to articles/cases, courts, and a per-user
saved-cases list with optional notes. All party names are anonymized
(Chinese placeholder style); all text is
original/synthesized or simplified public-domain statute text.
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS courts (
  court_id   TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  level      TEXT NOT NULL,
  region     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cases (
  case_id        TEXT PRIMARY KEY,
  case_number    TEXT NOT NULL,
  title          TEXT NOT NULL,
  court_id       TEXT NOT NULL,
  case_type      TEXT NOT NULL,
  cause          TEXT NOT NULL,
  judgment_date  TEXT NOT NULL,
  parties        TEXT NOT NULL,
  summary        TEXT NOT NULL,
  facts          TEXT NOT NULL,
  reasoning      TEXT NOT NULL,
  holding        TEXT NOT NULL,
  ruling         TEXT NOT NULL,
  outcome        TEXT NOT NULL,
  keywords       TEXT NOT NULL DEFAULT '',
  FOREIGN KEY (court_id) REFERENCES courts(court_id)
);

CREATE INDEX IF NOT EXISTS idx_cases_court ON cases(court_id);
CREATE INDEX IF NOT EXISTS idx_cases_type  ON cases(case_type);
CREATE INDEX IF NOT EXISTS idx_cases_date  ON cases(judgment_date);

CREATE TABLE IF NOT EXISTS statutes (
  statute_id   TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  short_name   TEXT NOT NULL DEFAULT '',
  issuer       TEXT NOT NULL,
  effective_date TEXT NOT NULL,
  status       TEXT NOT NULL,
  summary      TEXT NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_statutes_status ON statutes(status);

CREATE TABLE IF NOT EXISTS statute_articles (
  article_id    TEXT PRIMARY KEY,
  statute_id    TEXT NOT NULL,
  article_no    TEXT NOT NULL,
  seq           INTEGER NOT NULL DEFAULT 0,
  heading       TEXT NOT NULL DEFAULT '',
  text          TEXT NOT NULL,
  FOREIGN KEY (statute_id) REFERENCES statutes(statute_id)
);

CREATE INDEX IF NOT EXISTS idx_articles_statute ON statute_articles(statute_id, seq);

CREATE TABLE IF NOT EXISTS citations (
  citation_id    TEXT PRIMARY KEY,
  case_id        TEXT NOT NULL,
  target_type    TEXT NOT NULL CHECK(target_type IN ('article','case')),
  target_id      TEXT NOT NULL,
  label          TEXT NOT NULL DEFAULT '',
  FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

CREATE INDEX IF NOT EXISTS idx_citations_case ON citations(case_id);
CREATE INDEX IF NOT EXISTS idx_citations_target ON citations(target_type, target_id);

CREATE TABLE IF NOT EXISTS saved_cases (
  saved_id   TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL,
  case_id    TEXT NOT NULL,
  note       TEXT,
  saved_at   TEXT NOT NULL,
  FOREIGN KEY (case_id) REFERENCES cases(case_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_saved_user_case ON saved_cases(user_id, case_id);
CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_cases(user_id);

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
    conn.execute("PRAGMA journal_mode = DELETE;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    # Out-wait an external writer (the task world-controller holds
    # BEGIN IMMEDIATE across service databases with its own 10s busy_timeout).
    # Without this the server inherits sqlite3's 5s default and loses the race,
    # surfacing "database is locked" for a write that would have succeeded.
    conn.execute("PRAGMA busy_timeout = 20000;")
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
