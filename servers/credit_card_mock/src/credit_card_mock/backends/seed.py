"""External init_sql application.

The package ships schema only (see db.py). State enters via either:
  - a pre-built SQLite file mounted at --db_path (used as-is), OR
  - an init.sql file passed via --init_sql (applied once after schema init).

This module owns the second path; no JSON / no templating.
"""
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


def apply_init_sql(conn: sqlite3.Connection, path: str) -> None:
    """Execute the contents of `path` as a single SQL script against `conn`."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"init_sql not found: {p}")
    sql = p.read_text(encoding="utf-8")
    logger.info(f"applying init_sql from {p} ({len(sql)} bytes)")
    conn.executescript(sql)
