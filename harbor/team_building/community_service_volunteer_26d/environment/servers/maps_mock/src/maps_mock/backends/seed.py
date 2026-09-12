"""External state loader.

The package ships NO bundled seed data. ``apply_init_sql`` is the only
entry point — it runs a caller-supplied INSERT script against a backend
whose schema has already been created.
"""

from __future__ import annotations

import logging
from pathlib import Path

from .sqlite_backend import SqliteBackend

logger = logging.getLogger(__name__)


def apply_init_sql(backend: SqliteBackend, init_sql_path: str) -> None:
    """Run an external init.sql script (INSERTs) against ``backend``."""
    path = Path(init_sql_path)
    if not path.exists():
        raise FileNotFoundError(f"init_sql not found: {path}")
    logger.info("Applying init_sql from %s", path)
    backend.conn.executescript(path.read_text(encoding="utf-8"))
