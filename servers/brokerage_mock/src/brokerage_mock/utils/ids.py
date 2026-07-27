"""ID minting helpers."""
from datetime import datetime


def order_id(seq: int) -> str:
    return f"ord_{seq:08d}"


def now_iso_z() -> str:
    """Current UTC time in Z-iso format (audit trail only)."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
