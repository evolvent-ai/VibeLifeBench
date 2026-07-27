import hashlib
import sqlite3
from datetime import datetime


def confirmation_code(seed: str) -> str:
    """Deterministic MOCK-AAAA-BBBB confirmation code from a content hash."""
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest().upper()
    a = digest[0:4]
    b = digest[4:8]
    return f"MOCK-{a}-{b}"


def reservation_id(sim_date: str, seq: int) -> str:
    compact = sim_date.replace("-", "")
    return f"res_{compact}_{seq:06d}"


def ticket_id(seq: int) -> str:
    return f"tkt_{seq:06d}"


def now_iso_z() -> str:
    """Wall-clock UTC in Z-iso format (audit-trail only)."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def slugify(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--", "-")
