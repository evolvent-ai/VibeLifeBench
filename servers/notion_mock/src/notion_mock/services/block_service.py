"""Block CRUD: get children, append children, retrieve, update, archive."""
import logging
import sqlite3
from typing import Any, Dict, List, Optional

from ..models import row_to_block, wrap_list
from ..utils.exceptions import (
    BadArgError,
    BadBlockTypeError,
    BlockNotFoundError,
    PageNotFoundError,
)
from ..utils.ids import next_uuid, normalize_id
from ._common import dump_json, now_for, parse_json_col

logger = logging.getLogger(__name__)


# Block types we recognize. The mock is permissive: unknown types are
# rejected to catch typos but the content is otherwise stored verbatim.
KNOWN_BLOCK_TYPES = {
    "paragraph", "heading_1", "heading_2", "heading_3",
    "bulleted_list_item", "numbered_list_item", "to_do", "toggle",
    "quote", "callout", "divider", "code", "child_page", "child_database",
    "table", "table_row", "column_list", "column", "synced_block",
    "image", "video", "file", "pdf", "bookmark", "embed", "equation",
    "table_of_contents", "link_preview", "link_to_page", "template",
    "breadcrumb", "unsupported",
}


class BlockService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    # ---- read --------------------------------------------------------------
    def get_block_children(self, block_id: str, page_size: int = 10000) -> Dict[str, Any]:
        """List the direct children of a page or a parent block.

        Real Notion's "block_id" parameter on this endpoint accepts either
        a page id or a block id — we mirror that.

        Default page_size is intentionally large so this mock returns *all*
        children in one call (the tool docstring promises "returns all children
        in one page" and ``start_cursor`` is ignored). The previous default of
        100 silently truncated long pages, so rubric readers that don't paginate
        missed agent-written content beyond block 100 — a systematic
        false-negative. Keep large unless a caller explicitly passes a limit.
        """
        bid = normalize_id(block_id)
        # Try as parent_page first, then as parent_block.
        rows = self.conn.execute(
            """
            SELECT * FROM blocks
            WHERE parent_page_id = ? AND archived = 0
            ORDER BY position ASC, block_id ASC
            LIMIT ?
            """,
            (bid, int(page_size)),
        ).fetchall()
        if not rows:
            rows = self.conn.execute(
                """
                SELECT * FROM blocks
                WHERE parent_block_id = ? AND archived = 0
                ORDER BY position ASC, block_id ASC
                LIMIT ?
                """,
                (bid, int(page_size)),
            ).fetchall()
        # If still empty: confirm the page/block exists so we can return a
        # 404-style error vs an empty list.
        if not rows:
            exists = self.conn.execute(
                "SELECT 1 FROM pages WHERE page_id = ?", (bid,)
            ).fetchone()
            if not exists:
                exists = self.conn.execute(
                    "SELECT 1 FROM blocks WHERE block_id = ?", (bid,)
                ).fetchone()
            if not exists:
                exists = self.conn.execute(
                    "SELECT 1 FROM database_rows WHERE row_id = ?", (bid,)
                ).fetchone()
            if not exists:
                # Match real Notion: returns 404 if the parent doesn't exist.
                raise PageNotFoundError(f"parent not found: {block_id}")
        results = [row_to_block(r) for r in rows]
        out = wrap_list(results, type_="block")
        out["block"] = {}
        return out

    def retrieve_block(self, block_id: str) -> Dict[str, Any]:
        bid = normalize_id(block_id)
        row = self.conn.execute(
            "SELECT * FROM blocks WHERE block_id = ?", (bid,)
        ).fetchone()
        if row is None:
            raise BlockNotFoundError(f"block not found: {block_id}")
        return row_to_block(row)

    # ---- write -------------------------------------------------------------
    def append_children(
        self,
        block_id: str,
        children: List[Dict[str, Any]],
        after: Optional[str] = None,  # accepted for API parity; ignored (always append)
    ) -> Dict[str, Any]:
        if not isinstance(children, list) or not children:
            raise BadArgError("children must be a non-empty array")

        bid = normalize_id(block_id)
        # Determine where this parent lives.
        page_row = self.conn.execute(
            "SELECT page_id FROM pages WHERE page_id = ?", (bid,)
        ).fetchone()
        parent_is_page = page_row is not None
        if not parent_is_page:
            # Or it's a block.
            block_row = self.conn.execute(
                "SELECT block_id FROM blocks WHERE block_id = ?", (bid,)
            ).fetchone()
            if not block_row:
                # Or a database row (DB rows are pages too — they can have child blocks).
                drow = self.conn.execute(
                    "SELECT row_id FROM database_rows WHERE row_id = ?", (bid,)
                ).fetchone()
                if not drow:
                    raise PageNotFoundError(f"parent not found: {block_id}")
                parent_is_page = True  # treat DB-row pages as pages for parent linkage

        # Current max position under this parent.
        if parent_is_page:
            row = self.conn.execute(
                "SELECT COALESCE(MAX(position), -1) AS max_pos FROM blocks WHERE parent_page_id = ?",
                (bid,),
            ).fetchone()
        else:
            row = self.conn.execute(
                "SELECT COALESCE(MAX(position), -1) AS max_pos FROM blocks WHERE parent_block_id = ?",
                (bid,),
            ).fetchone()
        position = int(row["max_pos"]) + 1

        now = now_for(self.conn)
        inserted: List[Dict[str, Any]] = []
        for child in children:
            inserted.append(self._insert_block(child, bid, parent_is_page, position, now))
            position += 1

        # Bump parent's has_children flag if it's a block.
        if not parent_is_page:
            self.conn.execute(
                "UPDATE blocks SET has_children = 1, last_edited_time = ? WHERE block_id = ?",
                (now, bid),
            )
        else:
            self.conn.execute(
                "UPDATE pages SET last_edited_time = ? WHERE page_id = ?",
                (now, bid),
            )
        out = wrap_list(inserted, type_="block")
        out["block"] = {}
        return out

    def _insert_block(
        self,
        spec: Dict[str, Any],
        parent_id: str,
        parent_is_page: bool,
        position: int,
        now: str,
    ) -> Dict[str, Any]:
        if not isinstance(spec, dict):
            raise BadArgError("each child must be an object")
        btype = spec.get("type")
        if not btype:
            raise BadBlockTypeError("block.type is required")
        if btype not in KNOWN_BLOCK_TYPES:
            raise BadBlockTypeError(f"unknown block type: {btype}")
        # Content payload: real Notion puts type-specific fields under
        # ``spec[btype]``. We accept that and also tolerate the legacy
        # "flat" shape used by some older agent prompts.
        content = spec.get(btype)
        if content is None:
            content = {k: v for k, v in spec.items() if k not in ("type", "object", "children")}
        nested_children = spec.get("children")
        block_id = next_uuid(self.conn, "block")
        self.conn.execute(
            """
            INSERT INTO blocks
              (block_id, parent_block_id, parent_page_id, type, content_json,
               has_children, archived, position, created_time, last_edited_time)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
            """,
            (
                block_id,
                None if parent_is_page else parent_id,
                parent_id if parent_is_page else None,
                btype,
                dump_json(content or {}),
                1 if nested_children else 0,
                position,
                now,
                now,
            ),
        )
        if nested_children and isinstance(nested_children, list):
            # Recurse: this block becomes a parent_block.
            child_pos = 0
            for ch in nested_children:
                self._insert_block(ch, block_id, False, child_pos, now)
                child_pos += 1
        row = self.conn.execute(
            "SELECT * FROM blocks WHERE block_id = ?", (block_id,)
        ).fetchone()
        return row_to_block(row)

    def update_block(self, block_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        bid = normalize_id(block_id)
        row = self.conn.execute(
            "SELECT * FROM blocks WHERE block_id = ?", (bid,)
        ).fetchone()
        if row is None:
            raise BlockNotFoundError(f"block not found: {block_id}")

        new_archived = row["archived"]
        new_type = row["type"]
        current_content = parse_json_col(row["content_json"], {})

        for k, v in (body or {}).items():
            if k == "archived":
                new_archived = 1 if v else 0
            elif k == "in_trash":
                new_archived = 1 if v else new_archived
            elif k == "type":
                if v not in KNOWN_BLOCK_TYPES:
                    raise BadBlockTypeError(f"unknown block type: {v}")
                new_type = v
            elif k == "has_children":
                continue  # ignored: derived from actual children
            elif k == new_type or k == row["type"]:
                # Replace type-specific content.
                if isinstance(v, dict):
                    current_content = {**current_content, **v}
            else:
                # Tolerant: store under the type-specific bucket.
                if isinstance(v, dict):
                    current_content = {**current_content, **v}

        now = now_for(self.conn)
        self.conn.execute(
            """
            UPDATE blocks SET
              type = ?, content_json = ?, archived = ?, last_edited_time = ?
            WHERE block_id = ?
            """,
            (new_type, dump_json(current_content), new_archived, now, bid),
        )
        return self.retrieve_block(bid)

    def delete_block(self, block_id: str) -> Dict[str, Any]:
        bid = normalize_id(block_id)
        row = self.conn.execute(
            "SELECT * FROM blocks WHERE block_id = ?", (bid,)
        ).fetchone()
        if row is None:
            raise BlockNotFoundError(f"block not found: {block_id}")
        now = now_for(self.conn)
        self.conn.execute(
            "UPDATE blocks SET archived = 1, last_edited_time = ? WHERE block_id = ?",
            (now, bid),
        )
        return self.retrieve_block(bid)
