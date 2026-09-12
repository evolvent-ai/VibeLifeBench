"""Init-SQL applier.

Per the engineering brief, the package ships ZERO bundled data — state
arrives only via an external `--init_sql` file mounted by the caller.
This module exposes a single helper that applies that file inside a
transaction. No JSON expansion, no template rendering.
"""
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


def apply_init_sql(conn: sqlite3.Connection, init_sql_path: str) -> None:
    """Execute the SQL script at `init_sql_path` against `conn`.

    Caller is responsible for deciding when to invoke this (e.g. only on
    fresh DB creation, or when `--reset_db` was passed).
    """
    p = Path(init_sql_path)
    if not p.exists():
        raise FileNotFoundError(f"init_sql not found: {init_sql_path}")
    logger.info("applying init_sql from %s", p)
    sql = p.read_text(encoding="utf-8")
    conn.executescript(sql)
