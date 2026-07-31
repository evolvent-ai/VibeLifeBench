"""Page CRUD: create, retrieve, patch, retrieve a single property."""
import logging
import sqlite3
from typing import Any, Dict, List, Optional

from ..models import row_to_page
from ..utils.exceptions import (
    BadArgError,
    BadParentError,
    BadPropertyError,
    PageNotFoundError,
)
from ..utils.ids import next_uuid, normalize_id
from ._common import dump_json, extract_title, now_for, parse_json_col

logger = logging.getLogger(__name__)


# --- parent helpers ----------------------------------------------------------

def _parent_kind(parent: Dict[str, Any]) -> str:
    """Map a user-supplied ``parent`` dict to one of our parent_type values.

    Real Notion accepts ``page_id``, ``database_id``, ``workspace`` and
    (rarely) ``block_id``. We collapse ``block_id`` to ``page_id`` for
    the mock since blocks-as-page-parents is exotic.
    """
    if not isinstance(parent, dict):
        raise BadParentError("parent must be an object with type+id")
    t = parent.get("type")
    if t is None:
        # Infer from key.
        for k in ("page_id", "database_id", "workspace"):
            if k in parent:
                t = k
                break
    if t not in ("page_id", "database_id", "workspace"):
        raise BadParentError(f"unsupported parent type: {t}")
    return t


def _parent_id(parent: Dict[str, Any], parent_type: str) -> str:
    if parent_type == "workspace":
        return "workspace"
    pid = parent.get(parent_type)
    if not pid:
        raise BadParentError(f"parent.{parent_type} is required")
    return normalize_id(str(pid))


class PageService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- read --------------------------------------------------------------
    def retrieve_page(self, page_id: str) -> Dict[str, Any]:
        pid = normalize_id(page_id)
        row = self.conn.execute(
            "SELECT * FROM pages WHERE page_id = ?", (pid,)
        ).fetchone()
        if row:
            return row_to_page(row)
        # Maybe it's a database row (Notion treats DB rows as pages too).
        drow = self.conn.execute(
            "SELECT * FROM database_rows WHERE row_id = ?", (pid,)
        ).fetchone()
        if drow:
            from ..models import row_to_database_row_page
            return row_to_database_row_page(drow, drow["database_id"])
        raise PageNotFoundError(f"page not found: {page_id}")

    def retrieve_page_property(self, page_id: str, property_id: str) -> Dict[str, Any]:
        if not property_id:
            raise BadArgError("property_id is required")
        pid = normalize_id(page_id)
        row = self.conn.execute(
            "SELECT properties_json, title FROM pages WHERE page_id = ?",
            (pid,),
        ).fetchone()
        if row is None:
            drow = self.conn.execute(
                "SELECT properties_json FROM database_rows WHERE row_id = ?",
                (pid,),
            ).fetchone()
            if drow is None:
                raise PageNotFoundError(f"page not found: {page_id}")
            props = parse_json_col(drow["properties_json"], {})
        else:
            props = parse_json_col(row["properties_json"], {})
            # synthesize default title property if absent
            if "title" not in props and row["title"]:
                props["title"] = {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": row["title"], "link": None},
                            "plain_text": row["title"],
                        }
                    ],
                }
        # property_id may be the property name or its synthetic id.
        if property_id in props:
            return props[property_id]
        for name, val in props.items():
            if isinstance(val, dict) and val.get("id") == property_id:
                return val
        raise BadPropertyError(f"property not found: {property_id}")

    # ---- write -------------------------------------------------------------
    def create_page(
        self,
        parent: Dict[str, Any],
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Any] = None,
        cover: Optional[Any] = None,
        children: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        parent = parent or {}
        properties = properties or {}
        parent_type = _parent_kind(parent)
        parent_id = _parent_id(parent, parent_type)

        # Validate parent exists when it's a page or database.
        if parent_type == "page_id":
            ok = self.conn.execute(
                "SELECT 1 FROM pages WHERE page_id = ?", (parent_id,)
            ).fetchone()
            if not ok:
                raise BadParentError(f"parent page not found: {parent_id}")
        elif parent_type == "database_id":
            ok = self.conn.execute(
                "SELECT 1 FROM databases WHERE database_id = ?", (parent_id,)
            ).fetchone()
            if not ok:
                raise BadParentError(f"parent database not found: {parent_id}")

        now = now_for(self.conn)
        page_id = next_uuid(self.conn, "page")

        if parent_type == "database_id":
            # DB row pages go into database_rows.
            self.conn.execute(
                """
                INSERT INTO database_rows
                  (row_id, database_id, properties_json, created_time,
                   last_edited_time, archived)
                VALUES (?, ?, ?, ?, ?, 0)
                """,
                (page_id, parent_id, dump_json(properties), now, now),
            )
            if children:
                from .block_service import BlockService
                BlockService(self.conn).append_children(page_id, children)
            # Reuse retrieve for canonical shape.
            return self.retrieve_page(page_id)

        title = extract_title(properties)
        self.conn.execute(
            """
            INSERT INTO pages
              (page_id, parent_type, parent_id, title, archived,
               created_time, last_edited_time, properties_json, icon, cover)
            VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?, ?)
            """,
            (
                page_id, parent_type, parent_id, title, now, now,
                dump_json(properties),
                dump_json(icon) if icon is not None else None,
                dump_json(cover) if cover is not None else None,
            ),
        )

        if children:
            from .block_service import BlockService
            BlockService(self.conn).append_children(page_id, children)

        return self.retrieve_page(page_id)

    def patch_page(
        self,
        page_id: str,
        properties: Optional[Dict[str, Any]] = None,
        icon: Optional[Any] = None,
        cover: Optional[Any] = None,
        archived: Optional[bool] = None,
        in_trash: Optional[bool] = None,
    ) -> Dict[str, Any]:
        pid = normalize_id(page_id)
        row = self.conn.execute(
            "SELECT * FROM pages WHERE page_id = ?", (pid,)
        ).fetchone()
        if row is None:
            # try DB row
            drow = self.conn.execute(
                "SELECT * FROM database_rows WHERE row_id = ?", (pid,)
            ).fetchone()
            if drow is None:
                raise PageNotFoundError(f"page not found: {page_id}")
            return self._patch_db_row(drow, properties, archived, in_trash)

        merged_props = parse_json_col(row["properties_json"], {})
        if properties:
            for k, v in properties.items():
                merged_props[k] = v
        new_title = extract_title(merged_props) or row["title"]
        new_archived = row["archived"]
        if archived is not None:
            new_archived = 1 if archived else 0
        if in_trash is not None:
            new_archived = 1 if in_trash else new_archived
        new_icon = dump_json(icon) if icon is not None else row["icon"]
        new_cover = dump_json(cover) if cover is not None else row["cover"]
        now = now_for(self.conn)
        self.conn.execute(
            """
            UPDATE pages SET
              properties_json = ?, title = ?, archived = ?,
              icon = ?, cover = ?, last_edited_time = ?
            WHERE page_id = ?
            """,
            (
                dump_json(merged_props), new_title, new_archived,
                new_icon, new_cover, now, pid,
            ),
        )
        return self.retrieve_page(pid)

    def _patch_db_row(
        self,
        drow: sqlite3.Row,
        properties: Optional[Dict[str, Any]],
        archived: Optional[bool],
        in_trash: Optional[bool],
    ) -> Dict[str, Any]:
        merged = parse_json_col(drow["properties_json"], {})
        if properties:
            for k, v in properties.items():
                merged[k] = v
        new_archived = drow["archived"]
        if archived is not None:
            new_archived = 1 if archived else 0
        if in_trash is not None:
            new_archived = 1 if in_trash else new_archived
        now = now_for(self.conn)
        self.conn.execute(
            """
            UPDATE database_rows SET
              properties_json = ?, archived = ?, last_edited_time = ?
            WHERE row_id = ?
            """,
            (dump_json(merged), new_archived, now, drow["row_id"]),
        )
        return self.retrieve_page(drow["row_id"])
