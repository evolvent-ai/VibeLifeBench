"""Lightweight serialization helpers — DB rows → Notion-shaped dicts.

We don't use dataclasses because the Notion API surface is JSON-blob
heavy; explicit ``row_to_*`` functions are simpler and avoid spurious
field-mismatch errors.
"""
from .notion_objects import (
    row_to_block,
    row_to_database,
    row_to_database_row_page,
    row_to_page,
    row_to_user,
    wrap_list,
)

__all__ = [
    "row_to_block",
    "row_to_database",
    "row_to_database_row_page",
    "row_to_page",
    "row_to_user",
    "wrap_list",
]
