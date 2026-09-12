"""Lightweight argument validators shared by services.

Validators raise ``BadArgError`` (or another ``EmailsMockError``) on
failure so the tool decorator converts them into structured JSON.
"""
import re
from typing import Tuple

from .exceptions import BadArgError, ValidationError

_FOLDER_RE = re.compile(r"^[A-Za-z0-9 _\-./]+$")
_MAX_PAGE_SIZE = 50
_DEFAULT_PAGE_SIZE = 20


def validate_page_params(page: int, page_size: int) -> Tuple[int, int]:
    """Clamp ``page`` / ``page_size`` to the supported range."""
    try:
        p = int(page)
        ps = int(page_size)
    except (TypeError, ValueError):
        raise BadArgError("page and page_size must be integers")
    if p < 1:
        p = 1
    if ps < 1:
        ps = _DEFAULT_PAGE_SIZE
    if ps > _MAX_PAGE_SIZE:
        ps = _MAX_PAGE_SIZE
    return p, ps


def validate_folder_name(name: str) -> str:
    """Trim + sanity-check a folder name."""
    if not name or not isinstance(name, str):
        raise BadArgError("folder_name is required")
    n = name.strip()
    if not n:
        raise BadArgError("folder_name is required")
    if len(n) > 128:
        raise ValidationError("folder_name too long (max 128 chars)")
    if not _FOLDER_RE.match(n):
        raise ValidationError(
            "folder_name may only contain letters, digits, space, '_', '-', '.', '/'"
        )
    return n


def validate_query(query: str) -> str:
    if not query or not isinstance(query, str):
        raise BadArgError("query is required")
    q = query.strip()
    if not q:
        raise BadArgError("query is required")
    if len(q) > 512:
        raise ValidationError("query too long (max 512 chars)")
    return q


def validate_email_id(value: str) -> int:
    """Email / draft IDs are stored as INTEGER PKs but exposed as strings."""
    try:
        v = int(str(value))
    except (TypeError, ValueError):
        raise BadArgError(f"invalid id: {value!r}")
    if v <= 0:
        raise BadArgError(f"invalid id: {value!r}")
    return v
