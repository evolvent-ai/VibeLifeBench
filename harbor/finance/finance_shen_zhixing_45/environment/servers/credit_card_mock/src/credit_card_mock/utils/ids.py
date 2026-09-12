from datetime import datetime


from .world_clock import now as _world_now, now_iso as _world_now_iso, now_iso_z as _world_now_iso_z, today_utc as _world_today_utc
def compact_date(d: str) -> str:
    return d.replace("-", "")


def payment_id(sim_date: str, seq: int) -> str:
    return f"pay_{compact_date(sim_date)}_{seq:06d}"


def dispute_id(sim_date: str, seq: int) -> str:
    return f"dsp_{compact_date(sim_date)}_{seq:06d}"


def statement_id(card_id: str, period_end: str) -> str:
    return f"stm_{card_id.replace('card_', '')}_{compact_date(period_end)}"


def line_id(seq: int) -> str:
    return f"ln_{seq:08d}"


def tx_id(seq: int) -> str:
    return f"tx_{seq:08d}"


def ledger_id(seq: int) -> str:
    return f"rwl_{seq:08d}"


def now_iso_z() -> str:
    return _world_now_iso_z()
