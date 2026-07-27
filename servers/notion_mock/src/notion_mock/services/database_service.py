"""Database query service.

Implements ``API-post-database-query`` against ``database_rows``. Filter
support is intentionally narrow — it covers ``equals``, ``contains``,
``starts_with`` on string-shaped properties, plus ``checkbox.equals``.
Sorts use ``timestamp`` (created_time / last_edited_time) or property
names that resolve to scalar values.
"""
import logging
import sqlite3
from typing import Any, Dict, List, Optional

from ..models import row_to_database, row_to_database_row_page, wrap_list
from ..utils.exceptions import BadArgError, DatabaseNotFoundError
from ..utils.ids import normalize_id
from ._common import parse_json_col

logger = logging.getLogger(__name__)


# Stringy property types the simple filter understands.
STRINGY_TYPES = (
    "rich_text", "title", "url", "email", "phone_number", "select", "status",
)


class DatabaseService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- read --------------------------------------------------------------
    def retrieve_database(self, database_id: str) -> Dict[str, Any]:
        did = normalize_id(database_id)
        row = self.conn.execute(
            "SELECT * FROM databases WHERE database_id = ?", (did,)
        ).fetchone()
        if row is None:
            raise DatabaseNotFoundError(f"database not found: {database_id}")
        return row_to_database(row)

    def query_database(
        self,
        database_id: str,
        filter_: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        did = normalize_id(database_id)
        db_row = self.conn.execute(
            "SELECT database_id FROM databases WHERE database_id = ?", (did,)
        ).fetchone()
        if db_row is None:
            raise DatabaseNotFoundError(f"database not found: {database_id}")

        rows = self.conn.execute(
            """
            SELECT * FROM database_rows
            WHERE database_id = ? AND archived = 0
            ORDER BY created_time ASC, row_id ASC
            """,
            (did,),
        ).fetchall()

        # Materialize → filter in Python (Notion filter is JSON-shaped;
        # rebuilding it in SQL would be brittle and the row count is
        # bounded in this mock).
        pages = [row_to_database_row_page(r, did) for r in rows]
        if filter_:
            pages = [p for p in pages if _match_filter(p["properties"], filter_)]
        if sorts:
            pages = _apply_sorts(pages, sorts)
        if not isinstance(page_size, int) or page_size < 1:
            raise BadArgError("page_size must be >= 1")
        pages = pages[: min(int(page_size), 100)]
        out = wrap_list(pages, type_="page_or_database")
        out["page_or_database"] = {}
        return out


# ---------------------------------------------------------------------------
# Filter / sort helpers — covers the common cases benchmark tasks use.
# ---------------------------------------------------------------------------

def _stringy(value: Any) -> str:
    """Coerce a property value to a plain string for comparison."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        # rich_text / title style
        for key in ("rich_text", "title"):
            rich = value.get(key)
            if isinstance(rich, list):
                parts = []
                for chunk in rich:
                    if isinstance(chunk, dict):
                        t = chunk.get("plain_text")
                        if t is None and isinstance(chunk.get("text"), dict):
                            t = chunk["text"].get("content", "")
                        parts.append(t or "")
                return "".join(parts)
        if value.get("type") == "select" and isinstance(value.get("select"), dict):
            return value["select"].get("name", "") or ""
        if value.get("type") == "status" and isinstance(value.get("status"), dict):
            return value["status"].get("name", "") or ""
        # last resort
        return str(value.get("content") or value.get("name") or "")
    return str(value)


def _sortable(value: Any) -> Any:
    """Pick a sort key out of a property value.

    Numbers / dates / checkboxes sort by their scalar; string-y types
    sort by their plain text via ``_stringy``.
    """
    if isinstance(value, dict):
        if "number" in value and isinstance(value.get("number"), (int, float)):
            return value["number"]
        if "checkbox" in value:
            return 1 if value.get("checkbox") else 0
        date_val = value.get("date")
        if isinstance(date_val, dict):
            return date_val.get("start") or ""
    return _stringy(value)


def _match_filter(properties: Dict[str, Any], filt: Dict[str, Any]) -> bool:
    """Tiny filter evaluator covering the common shapes:
      - {"and": [...]} / {"or": [...]}
      - {"property": "Name", "<type>": {"<op>": value}}
    """
    if "and" in filt and isinstance(filt["and"], list):
        return all(_match_filter(properties, sub) for sub in filt["and"])
    if "or" in filt and isinstance(filt["or"], list):
        return any(_match_filter(properties, sub) for sub in filt["or"])

    prop_name = filt.get("property")
    if not prop_name:
        return True
    prop_value = properties.get(prop_name)

    # Checkbox is special: boolean equality.
    if isinstance(filt.get("checkbox"), dict):
        want = filt["checkbox"].get("equals")
        got = False
        if isinstance(prop_value, dict):
            got = bool(prop_value.get("checkbox", False))
        return bool(got) == bool(want)

    # Number
    if isinstance(filt.get("number"), dict):
        cond = filt["number"]
        num = None
        if isinstance(prop_value, dict):
            num = prop_value.get("number")
        if num is None:
            return False
        if "equals" in cond:
            return num == cond["equals"]
        if "greater_than" in cond:
            return num > cond["greater_than"]
        if "less_than" in cond:
            return num < cond["less_than"]
        if "greater_than_or_equal_to" in cond:
            return num >= cond["greater_than_or_equal_to"]
        if "less_than_or_equal_to" in cond:
            return num <= cond["less_than_or_equal_to"]

    # String-y types
    for ftype in STRINGY_TYPES:
        if isinstance(filt.get(ftype), dict):
            cond = filt[ftype]
            haystack = _stringy(prop_value)
            if "equals" in cond:
                return haystack == str(cond["equals"])
            if "contains" in cond:
                return str(cond["contains"]).lower() in haystack.lower()
            if "starts_with" in cond:
                return haystack.lower().startswith(str(cond["starts_with"]).lower())
            if "ends_with" in cond:
                return haystack.lower().endswith(str(cond["ends_with"]).lower())
            if cond.get("is_empty"):
                return haystack == ""
            if cond.get("is_not_empty"):
                return haystack != ""

    return True


def _apply_sorts(pages: List[Dict[str, Any]], sorts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def _key(p: Dict[str, Any]):
        out = []
        for sort in sorts:
            direction = -1 if sort.get("direction") == "descending" else 1
            if "timestamp" in sort:
                ts = sort["timestamp"]
                v = p.get("created_time" if ts == "created_time" else "last_edited_time", "")
                out.append((direction, v))
            elif "property" in sort:
                v = _sortable(p["properties"].get(sort["property"]))
                out.append((direction, v))
        return out

    def cmp_to_key():
        from functools import cmp_to_key as ck

        def compare(a, b):
            ka, kb = _key(a), _key(b)
            for (da, va), (_db, vb) in zip(ka, kb):
                try:
                    lt = va < vb
                    gt = va > vb
                except TypeError:
                    lt = str(va) < str(vb)
                    gt = str(va) > str(vb)
                if lt:
                    return -1 * da
                if gt:
                    return 1 * da
            return 0

        return ck(compare)

    return sorted(pages, key=cmp_to_key())
