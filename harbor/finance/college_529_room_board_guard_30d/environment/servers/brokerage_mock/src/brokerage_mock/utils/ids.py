"""ID minting helpers."""
from datetime import datetime


from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc
def order_id(seq: int) -> str:
    return f"ord_{seq:08d}"


def now_iso_z() -> str:
    """Current UTC time in Z-iso format (audit trail only)."""
    return _world_now_iso_z()
