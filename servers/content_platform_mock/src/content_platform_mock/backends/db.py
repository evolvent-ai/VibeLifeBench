"""SQLite backend for content_platform_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
  user_id        TEXT PRIMARY KEY,
  handle         TEXT NOT NULL,
  nickname       TEXT NOT NULL,
  bio            TEXT,
  is_official    INTEGER NOT NULL DEFAULT 0,
  follower_count INTEGER NOT NULL DEFAULT 0,
  note_count     INTEGER NOT NULL DEFAULT 0,
  joined_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_users_handle ON users(handle);

CREATE TABLE IF NOT EXISTS notes (
  note_id         TEXT PRIMARY KEY,
  author_id       TEXT NOT NULL,
  title           TEXT NOT NULL,
  body            TEXT NOT NULL,
  category        TEXT NOT NULL CHECK(category IN ('备考','装修','健身','旅行','母婴','其他')),
  tags            TEXT NOT NULL DEFAULT '[]',
  image_captions  TEXT NOT NULL DEFAULT '[]',
  like_count      INTEGER NOT NULL DEFAULT 0,
  collect_count   INTEGER NOT NULL DEFAULT 0,
  comment_count   INTEGER NOT NULL DEFAULT 0,
  view_count      INTEGER NOT NULL DEFAULT 0,
  published_at    TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_notes_author   ON notes(author_id);
CREATE INDEX IF NOT EXISTS idx_notes_category ON notes(category);
CREATE INDEX IF NOT EXISTS idx_notes_published ON notes(published_at);

CREATE TABLE IF NOT EXISTS comments (
  comment_id    TEXT PRIMARY KEY,
  note_id       TEXT NOT NULL,
  user_id       TEXT NOT NULL,
  body          TEXT NOT NULL,
  like_count    INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL,
  FOREIGN KEY (note_id) REFERENCES notes(note_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_comments_note ON comments(note_id, created_at);

CREATE TABLE IF NOT EXISTS follows (
  follower_id   TEXT NOT NULL,
  followee_id   TEXT NOT NULL,
  created_at    TEXT NOT NULL,
  PRIMARY KEY (follower_id, followee_id),
  FOREIGN KEY (follower_id) REFERENCES users(user_id),
  FOREIGN KEY (followee_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_follows_follower ON follows(follower_id);
CREATE INDEX IF NOT EXISTS idx_follows_followee ON follows(followee_id);

CREATE TABLE IF NOT EXISTS likes (
  user_id     TEXT NOT NULL,
  note_id     TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  PRIMARY KEY (user_id, note_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (note_id) REFERENCES notes(note_id)
);

CREATE INDEX IF NOT EXISTS idx_likes_note ON likes(note_id);

CREATE TABLE IF NOT EXISTS collections (
  user_id     TEXT NOT NULL,
  note_id     TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  PRIMARY KEY (user_id, note_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (note_id) REFERENCES notes(note_id)
);

CREATE INDEX IF NOT EXISTS idx_collections_user ON collections(user_id, created_at);

CREATE TABLE IF NOT EXISTS topics (
  topic_id      TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  category      TEXT NOT NULL CHECK(category IN ('备考','装修','健身','旅行','母婴','其他')),
  description   TEXT,
  note_count    INTEGER NOT NULL DEFAULT 0,
  view_count    INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_topics_name ON topics(name);

CREATE TABLE IF NOT EXISTS note_topics (
  note_id   TEXT NOT NULL,
  topic_id  TEXT NOT NULL,
  PRIMARY KEY (note_id, topic_id),
  FOREIGN KEY (note_id) REFERENCES notes(note_id),
  FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

CREATE INDEX IF NOT EXISTS idx_note_topics_topic ON note_topics(topic_id);

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
