"""External state loader.

``apply_init_sql`` runs an external SQL script against the open sqlite
connection. The script is the env's ``init.sql`` and is responsible for
populating all rows (visa products, entry rules, advisories, in-flight
applications, etc.) — the package itself ships no seed data.
"""

import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)


def apply_init_sql(conn: sqlite3.Connection, init_sql_path: str) -> None:
    """Run an external init.sql script against ``conn``."""
    path = Path(init_sql_path)
    if not path.exists():
        raise FileNotFoundError(f"init_sql not found: {path}")
    logger.info("Applying init_sql from %s", path)
    conn.executescript(path.read_text(encoding="utf-8"))
