"""Workspace search.

Real Notion's ``API-post-search`` is a full-text search across pages and
databases the bot has access to. Our mock walks both tables, filters by a
``query`` substring match against the title, and sorts on a timestamp
column.
"""
import logging
import sqlite3
from typing import Any, Dict, List, Optional

from ..models import row_to_database, row_to_page, wrap_list

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def post_search(
        self,
        query: Optional[str] = None,
        filter_: Optional[Dict[str, Any]] = None,
        sort: Optional[Dict[str, Any]] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        q = (query or "").strip().lower()

        # Filter.value ∈ {"page", "database"} narrows the object kind.
        want_pages = True
        want_dbs = True
        if isinstance(filter_, dict):
            v = filter_.get("value")
            if v == "page":
                want_dbs = False
            elif v == "database":
                want_pages = False

        results: List[Dict[str, Any]] = []

        if want_pages:
            rows = self.conn.execute(
                """
                SELECT * FROM pages
                WHERE archived = 0 AND (? = '' OR LOWER(title) LIKE ? OR LOWER(properties_json) LIKE ?)
                ORDER BY last_edited_time DESC, page_id ASC
                """,
                (q, f"%{q}%", f"%{q}%"),
            ).fetchall()
            for r in rows:
                results.append(row_to_page(r))

        if want_dbs:
            rows = self.conn.execute(
                """
                SELECT * FROM databases
                WHERE archived = 0 AND (? = '' OR LOWER(title) LIKE ?)
                ORDER BY last_edited_time DESC, database_id ASC
                """,
                (q, f"%{q}%"),
            ).fetchall()
            for r in rows:
                results.append(row_to_database(r))

        # Sort: {"direction": "ascending"|"descending", "timestamp":
        # "last_edited_time"} per spec.
        if isinstance(sort, dict):
            direction = sort.get("direction", "descending")
            ts_field = sort.get("timestamp", "last_edited_time")
            if ts_field not in ("created_time", "last_edited_time"):
                ts_field = "last_edited_time"
            reverse = direction != "ascending"
            results.sort(key=lambda r: r.get(ts_field, ""), reverse=reverse)

        ps = max(1, min(int(page_size or 100), 100))
        results = results[:ps]
        out = wrap_list(results, type_="page_or_database")
        out["page_or_database"] = {}
        return out
