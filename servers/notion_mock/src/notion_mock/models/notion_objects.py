"""Row → Notion-shaped JSON dict converters.

The Notion API wraps lists in ``{object: "list", results: [...], has_more,
next_cursor, type}``. Single objects carry an ``object`` discriminator
(``"page"``, ``"database"``, ``"block"``, ``"user"``, ``"comment"``).
The helpers below produce dicts in those shapes from raw SQLite rows.

We don't reproduce every field of the real API — only the fields that
benchmark tasks (and the legacy Postgres mock) actually consume.
"""
import json
from typing import Any, Dict, List, Optional


def _loads(s: Optional[str], default: Any) -> Any:
    if s is None or s == "":
        return default
    try:
        return json.loads(s)
    except (TypeError, ValueError):
        return default


def _title_property(title: str) -> Dict[str, Any]:
    """Convert a plain string title into a Notion ``title`` property value."""
    if not title:
        return {
            "id": "title",
            "type": "title",
            "title": [],
        }
    return {
        "id": "title",
        "type": "title",
        "title": [
            {
                "type": "text",
                "text": {"content": title, "link": None},
                "annotations": {
                    "bold": False, "italic": False, "strikethrough": False,
                    "underline": False, "code": False, "color": "default",
                },
                "plain_text": title,
                "href": None,
            }
        ],
    }


def row_to_page(row: Any, *, include_title_in_properties: bool = True) -> Dict[str, Any]:
    props = _loads(row["properties_json"], {})
    if include_title_in_properties and "title" not in props and row["title"]:
        props = {**props, "title": _title_property(row["title"])}
    parent: Dict[str, Any] = {"type": row["parent_type"]}
    if row["parent_type"] == "workspace":
        parent["workspace"] = True
    else:
        parent[row["parent_type"]] = row["parent_id"]
    return {
        "object": "page",
        "id": row["page_id"],
        "created_time": row["created_time"],
        "last_edited_time": row["last_edited_time"],
        "archived": bool(int(row["archived"])),
        "in_trash": bool(int(row["archived"])),
        "icon": _loads(row["icon"], None),
        "cover": _loads(row["cover"], None),
        "parent": parent,
        "properties": props,
        "url": f"https://www.notion.so/{row['page_id'].replace('-', '')}",
    }


def row_to_database_row_page(row: Any, database_id: str) -> Dict[str, Any]:
    """A DB row is a page whose parent is the database."""
    props = _loads(row["properties_json"], {})
    return {
        "object": "page",
        "id": row["row_id"],
        "created_time": row["created_time"],
        "last_edited_time": row["last_edited_time"],
        "archived": bool(int(row["archived"])),
        "in_trash": bool(int(row["archived"])),
        "icon": None,
        "cover": None,
        "parent": {"type": "database_id", "database_id": database_id},
        "properties": props,
        "url": f"https://www.notion.so/{row['row_id'].replace('-', '')}",
    }


def row_to_database(row: Any) -> Dict[str, Any]:
    schema = _loads(row["schema_json"], {})
    parent: Dict[str, Any] = {"type": row["parent_type"]}
    if row["parent_type"] == "workspace":
        parent["workspace"] = True
    else:
        parent[row["parent_type"]] = row["parent_id"]
    title_rich = []
    if row["title"]:
        title_rich = [
            {
                "type": "text",
                "text": {"content": row["title"], "link": None},
                "plain_text": row["title"],
                "annotations": {
                    "bold": False, "italic": False, "strikethrough": False,
                    "underline": False, "code": False, "color": "default",
                },
                "href": None,
            }
        ]
    return {
        "object": "database",
        "id": row["database_id"],
        "created_time": row["created_time"],
        "last_edited_time": row["last_edited_time"],
        "title": title_rich,
        "description": [],
        "properties": schema,
        "parent": parent,
        "archived": bool(int(row["archived"])),
        "in_trash": bool(int(row["archived"])),
        "is_inline": False,
        "url": f"https://www.notion.so/{row['database_id'].replace('-', '')}",
    }


def row_to_block(row: Any) -> Dict[str, Any]:
    content = _loads(row["content_json"], {})
    block_type = row["type"]
    parent: Dict[str, Any]
    if row["parent_block_id"]:
        parent = {"type": "block_id", "block_id": row["parent_block_id"]}
    elif row["parent_page_id"]:
        parent = {"type": "page_id", "page_id": row["parent_page_id"]}
    else:
        parent = {"type": "workspace", "workspace": True}
    return {
        "object": "block",
        "id": row["block_id"],
        "parent": parent,
        "created_time": row["created_time"],
        "last_edited_time": row["last_edited_time"],
        "has_children": bool(int(row["has_children"])),
        "archived": bool(int(row["archived"])),
        "in_trash": bool(int(row["archived"])),
        "type": block_type,
        block_type: content,
    }


def row_to_user(row: Any) -> Dict[str, Any]:
    return {
        "object": "user",
        "id": row["user_id"],
        "name": row["name"],
        "avatar_url": row["avatar_url"],
        "type": row["type"],
        "person": {"email": row["email"]} if row["type"] == "person" and row["email"] else {},
    }


def wrap_list(results: List[Dict[str, Any]], *, type_: str = "page_or_database") -> Dict[str, Any]:
    return {
        "object": "list",
        "results": results,
        "has_more": False,
        "next_cursor": None,
        "type": type_,
    }
