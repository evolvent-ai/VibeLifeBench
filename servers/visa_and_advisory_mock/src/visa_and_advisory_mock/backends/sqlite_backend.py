"""SQLite connection helpers and schema initialization.

A single shared connection is used per process. PRAGMA foreign_keys = ON.
Foreign keys are enforced on every connection.
"""

import os
import sqlite3
import threading
from typing import Optional

_SCHEMA = """
CREATE TABLE IF NOT EXISTS entry_requirements (
    origin_nationality       TEXT NOT NULL,
    destination              TEXT NOT NULL,
    purpose                  TEXT NOT NULL,
    visa_required            INTEGER NOT NULL,
    allowed_stay_days        INTEGER,
    passport_validity_months INTEGER NOT NULL DEFAULT 6,
    docs_needed_json         TEXT NOT NULL DEFAULT '[]',
    notes                    TEXT NOT NULL DEFAULT '',
    updated_at               TEXT NOT NULL,
    PRIMARY KEY (origin_nationality, destination, purpose)
);

CREATE TABLE IF NOT EXISTS visa_products (
    product_id            TEXT PRIMARY KEY,
    destination           TEXT NOT NULL,
    nationality           TEXT NOT NULL,
    name                  TEXT NOT NULL,
    processing_time_days  INTEGER NOT NULL,
    fee_amount            INTEGER NOT NULL,
    fee_currency          TEXT NOT NULL,
    delivery              TEXT NOT NULL,
    form_schema_json      TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_visa_products_dest_nat
    ON visa_products(destination, nationality);

CREATE TABLE IF NOT EXISTS visa_applications (
    application_id  TEXT PRIMARY KEY,
    user_id         TEXT NOT NULL,
    product_id      TEXT NOT NULL,
    status          TEXT NOT NULL,
    applicant_json  TEXT NOT NULL DEFAULT '{}',
    answers_json    TEXT NOT NULL DEFAULT '{}',
    decision_day    INTEGER,
    decision_note   TEXT,
    evisa_doc_ref   TEXT,
    history_json    TEXT NOT NULL DEFAULT '[]',
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES visa_products(product_id)
);

CREATE INDEX IF NOT EXISTS idx_visa_applications_user
    ON visa_applications(user_id);

CREATE INDEX IF NOT EXISTS idx_visa_applications_status_day
    ON visa_applications(status, decision_day);

CREATE TABLE IF NOT EXISTS application_documents (
    doc_id          TEXT PRIMARY KEY,
    application_id  TEXT NOT NULL,
    kind            TEXT NOT NULL,
    ref             TEXT NOT NULL,
    uploaded_at     TEXT NOT NULL,
    FOREIGN KEY (application_id) REFERENCES visa_applications(application_id)
);

CREATE INDEX IF NOT EXISTS idx_application_documents_app_kind
    ON application_documents(application_id, kind);

CREATE TABLE IF NOT EXISTS advisories (
    country_code  TEXT PRIMARY KEY,
    level         INTEGER NOT NULL,
    text          TEXT NOT NULL,
    updated_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS advisory_subscriptions (
    sub_id        TEXT PRIMARY KEY,
    country_code  TEXT NOT NULL,
    sink          TEXT NOT NULL,
    created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_advisory_subscriptions_country
    ON advisory_subscriptions(country_code);

CREATE TABLE IF NOT EXISTS notifications (
    id           TEXT PRIMARY KEY,
    created_at   TEXT NOT NULL,
    channel      TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS _counters (
    name  TEXT PRIMARY KEY,
    value INTEGER NOT NULL
);
"""


def get_connection(db_path: str) -> sqlite3.Connection:
    """Return a sqlite3 connection with foreign keys enforced."""

    parent = os.path.dirname(os.path.abspath(db_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(_SCHEMA)


class SqliteBackend:
    """Thin wrapper around a sqlite3 connection with a write lock."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = get_connection(db_path)
        self.lock = threading.RLock()
        init_schema(self.conn)

    def execute(self, sql: str, params: tuple | list = ()):
        with self.lock:
            return self.conn.execute(sql, params)

    def executemany(self, sql: str, params_iter):
        with self.lock:
            return self.conn.executemany(sql, params_iter)

    def fetchone(self, sql: str, params: tuple | list = ()) -> Optional[sqlite3.Row]:
        with self.lock:
            return self.conn.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple | list = ()) -> list[sqlite3.Row]:
        with self.lock:
            return self.conn.execute(sql, params).fetchall()

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass
