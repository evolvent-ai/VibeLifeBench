"""Deterministic ID generators backed by a sqlite ``_counters`` table.

Every ID has the same shape it had under the old RNG-driven scheme (so
checkers that match on prefix still pass) but the variable bytes are now
either monotonic sequence numbers or content-hash digests — no RNG.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from typing import Any


# Per SPEC Appendix B: 24 symbols, no I, O, 0, 1.
_PNR_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def stable_hash_int(*parts: Any) -> int:
    """Deterministic 63-bit int hash over JSON-serialized inputs.

    Python's builtin ``hash()`` is salted per process, which breaks replay
    determinism. Callers that need a content hash should use this instead.
    """
    blob = json.dumps(list(parts), sort_keys=True, default=str).encode("utf-8")
    digest = hashlib.sha256(blob).digest()
    return int.from_bytes(digest[:8], "big") & ((1 << 63) - 1)


def next_counter(conn: sqlite3.Connection, name: str) -> int:
    """Atomically bump and return the named counter."""
    conn.execute(
        "INSERT INTO _counters (name, value) VALUES (?, 0) "
        "ON CONFLICT(name) DO NOTHING",
        (name,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE name = ?", (name,))
    row = conn.execute("SELECT value FROM _counters WHERE name = ?", (name,)).fetchone()
    # These generators are also used by read-like search endpoints. Without an
    # explicit commit, an empty-result search can leave the process-wide
    # connection in a write transaction indefinitely and block task runtime
    # mutations issued through a second SQLite connection.
    conn.commit()
    return int(row[0] if not isinstance(row, sqlite3.Row) else row["value"])


def _hash_hex(seed: str, n_chars: int) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:n_chars]


def pnr_gen(conn: sqlite3.Connection, seed: str = "") -> str:
    """Return a 6-char PNR from the PNR alphabet, derived from a content hash.

    Two PNRs for the same ``seed`` are identical, so callers must include
    enough discriminating bytes (offer_id + counter, etc.).
    """
    n = next_counter(conn, "pnr_seq")
    raw = hashlib.sha256(f"pnr|{n}|{seed}".encode("utf-8")).digest()
    out = []
    for b in raw[:6]:
        out.append(_PNR_ALPHABET[b % len(_PNR_ALPHABET)])
    return "".join(out)


def offer_id_gen(conn: sqlite3.Connection, seed: str = "") -> str:
    n = next_counter(conn, "offer_seq")
    return f"ofr_{_hash_hex(f'offer|{n}|{seed}', 14)}"


def sub_id_gen(conn: sqlite3.Connection, seed: str = "") -> str:
    n = next_counter(conn, "sub_seq")
    return f"sub_{_hash_hex(f'sub|{n}|{seed}', 10)}"


def boarding_pass_id_gen(conn: sqlite3.Connection, seed: str = "") -> str:
    n = next_counter(conn, "bp_seq")
    return "BP" + _hash_hex(f"bp|{n}|{seed}", 8).upper()


def ticket_number_gen(conn: sqlite3.Connection, seed: str = "") -> str:
    """Return a 13-digit ``172-XXXXXXXXX`` ticket number."""
    n = next_counter(conn, "ticket_seq")
    digest = hashlib.sha256(f"ticket|{n}|{seed}".encode("utf-8")).hexdigest()
    digits = "".join(c for c in digest if c.isdigit())
    while len(digits) < 9:
        digits += digits  # extremely unlikely on a sha256 hex but keep it safe
    return "172-" + digits[:9]


def search_id_gen(conn: sqlite3.Connection, seed: str = "") -> str:
    n = next_counter(conn, "search_seq")
    return f"srch_{_hash_hex(f'search|{n}|{seed}', 8)}"
