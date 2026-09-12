"""External init_sql application.

No bundled seed data: callers provide their own state via --init_sql.
"""
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


def apply_init_sql(conn: sqlite3.Connection, path: str) -> None:
    """Run an external INSERT-only SQL script against the open connection."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"init_sql file not found: {p}")
    logger.info("Applying init_sql from %s", p)
    conn.executescript(p.read_text(encoding="utf-8"))
