"""External state loader.

The package ships NO bundled seed data. ``apply_init_sql`` is the only
entry point — it runs a caller-supplied INSERT script against a connection
whose schema has already been created.
"""
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


def apply_init_sql(conn: sqlite3.Connection, init_sql_path: str) -> None:
    """Run an external init.sql script (INSERTs) against ``conn``."""
    path = Path(init_sql_path)
    if not path.exists():
        raise FileNotFoundError(f"init_sql not found: {path}")
    logger.info("Applying init_sql from %s", path)
    conn.executescript(path.read_text(encoding="utf-8"))
