from datetime import datetime


def now_iso_z() -> str:
    """UTC ISO timestamp in Z form, used for ``date`` / ``updated_at`` fields."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
