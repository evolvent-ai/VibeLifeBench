"""ID helpers.

Real Notion uses dashed UUIDs as object identifiers (pages, blocks,
databases, users, comments). We keep the dashed-UUID shape so existing
agent prompts that grep for UUIDs still match. IDs accept input with
or without dashes — we normalize on read.

v3: IDs are fully deterministic. ``next_uuid`` increments a row in the
``counters`` table per ``kind`` and feeds ``"<kind>:<n>"`` into
``sha256`` to materialise a UUID-v4-shaped string. No ``random`` or
``uuid.uuid4`` anywhere.
"""
import hashlib
import sqlite3
import uuid


def _next_counter(conn: sqlite3.Connection, key: str) -> int:
    """Increment ``counters.value`` for ``key`` and return the new value."""
    conn.execute(
        "INSERT INTO counters(key, value) VALUES(?, 1) "
        "ON CONFLICT(key) DO UPDATE SET value = value + 1",
        (key,),
    )
    row = conn.execute(
        "SELECT value FROM counters WHERE key = ?", (key,),
    ).fetchone()
    return int(row["value"])


def next_uuid(conn: sqlite3.Connection, kind: str) -> str:
    """Deterministic dashed-UUID-shaped id for an object of ``kind``.

    ``kind`` partitions the sequence (so page ids do not collide with
    block ids). The output looks like a UUID-v4 but is fully
    reproducible from (``kind``, n).
    """
    n = _next_counter(conn, kind)
    h = hashlib.sha256(f"{kind}:{n}".encode("utf-8")).hexdigest()
    # Format as dashed UUID; force version 4 + RFC 4122 variant bits.
    return f"{h[0:8]}-{h[8:12]}-4{h[13:16]}-8{h[17:20]}-{h[20:32]}"


def normalize_id(s: str) -> str:
    """Strip dashes to compare two UUIDs regardless of formatting.

    Returns the canonical dashed form when ``s`` is a 32-hex string.
    """
    if not s:
        return s
    stripped = s.replace("-", "").strip().lower()
    if len(stripped) == 32:
        try:
            return str(uuid.UUID(stripped))
        except ValueError:
            return s
    return s
