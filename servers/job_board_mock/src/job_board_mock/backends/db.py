"""SQLite backend for job_board_mock.

Schema-only — no bundled seed data. State enters via the env directory's
``init.sql`` (run by ``server.py`` on cold start).
"""
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS companies (
  company_id     TEXT PRIMARY KEY,
  name           TEXT NOT NULL,
  industry       TEXT NOT NULL,
  size           TEXT NOT NULL,
  stage          TEXT,
  city           TEXT NOT NULL,
  intro          TEXT NOT NULL,
  rating         REAL NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_companies_city ON companies(city);

CREATE TABLE IF NOT EXISTS jobs (
  job_id              TEXT PRIMARY KEY,
  company_id          TEXT NOT NULL,
  title               TEXT NOT NULL,
  city                TEXT NOT NULL,
  category            TEXT NOT NULL,
  salary_min_minor    INTEGER NOT NULL,
  salary_max_minor    INTEGER NOT NULL,
  salary_months       INTEGER NOT NULL DEFAULT 12,
  experience          TEXT NOT NULL CHECK(experience IN
                        ('intern','fresh_grad','1-3','3-5','5-10','10+')),
  education           TEXT NOT NULL CHECK(education IN
                        ('unlimited','college','bachelor','master','phd')),
  jd                  TEXT NOT NULL,
  requirements        TEXT NOT NULL,
  tags                TEXT,
  status              TEXT NOT NULL DEFAULT 'open'
                        CHECK(status IN ('open','closed')),
  posted_at           TEXT NOT NULL,
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_city ON jobs(city);
CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs(category);

CREATE TABLE IF NOT EXISTS resumes (
  resume_id      TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL,
  name           TEXT NOT NULL,
  headline       TEXT NOT NULL,
  years_exp      INTEGER NOT NULL DEFAULT 0,
  education      TEXT NOT NULL,
  skills         TEXT,
  summary        TEXT,
  updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_resumes_user ON resumes(user_id);

CREATE TABLE IF NOT EXISTS saved_jobs (
  user_id    TEXT NOT NULL,
  job_id     TEXT NOT NULL,
  saved_at   TEXT NOT NULL,
  PRIMARY KEY (user_id, job_id),
  FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_jobs(user_id);

CREATE TABLE IF NOT EXISTS applications (
  application_id   TEXT PRIMARY KEY,
  user_id          TEXT NOT NULL,
  job_id           TEXT NOT NULL,
  resume_id        TEXT NOT NULL,
  cover_letter     TEXT,
  status           TEXT NOT NULL DEFAULT 'submitted'
                     CHECK(status IN ('submitted','viewed','interview','offer','rejected')),
  applied_at       TEXT NOT NULL,
  updated_at       TEXT NOT NULL,
  FOREIGN KEY (job_id)    REFERENCES jobs(job_id),
  FOREIGN KEY (resume_id) REFERENCES resumes(resume_id)
);

CREATE INDEX IF NOT EXISTS idx_apps_user ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_apps_status ON applications(status);

CREATE TABLE IF NOT EXISTS chats (
  chat_id        TEXT PRIMARY KEY,
  user_id        TEXT NOT NULL,
  job_id         TEXT NOT NULL,
  company_id     TEXT NOT NULL,
  recruiter_name TEXT NOT NULL,
  created_at     TEXT NOT NULL,
  last_at        TEXT NOT NULL,
  FOREIGN KEY (job_id)     REFERENCES jobs(job_id),
  FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE INDEX IF NOT EXISTS idx_chats_user ON chats(user_id);

CREATE TABLE IF NOT EXISTS chat_messages (
  message_id   TEXT PRIMARY KEY,
  chat_id      TEXT NOT NULL,
  sender       TEXT NOT NULL CHECK(sender IN ('user','recruiter')),
  body         TEXT NOT NULL,
  sent_at      TEXT NOT NULL,
  FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_chat ON chat_messages(chat_id, sent_at);

CREATE TABLE IF NOT EXISTS job_alerts (
  alert_id     TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL,
  query_json   TEXT NOT NULL,
  created_at   TEXT NOT NULL,
  active       INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_alerts_user ON job_alerts(user_id);

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
