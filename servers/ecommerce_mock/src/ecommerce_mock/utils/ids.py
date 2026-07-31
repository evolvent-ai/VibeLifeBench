"""Deterministic ID generators. All IDs are domain-prefixed strings."""


def order_id(sim_date: str, seq: int) -> str:
    compact = sim_date.replace("-", "")
    return f"ord_{compact}_{seq:06d}"


def order_item_id(order_id_: str, idx: int) -> str:
    # idx is 1-based position within the order.
    return f"oit_{order_id_[4:]}_{idx:02d}"


def cart_item_id(seq: int) -> str:
    return f"ci_{seq:08d}"


def refund_id(sim_date: str, seq: int) -> str:
    compact = sim_date.replace("-", "")
    return f"rf_{compact}_{seq:06d}"


def address_id(seq: int) -> str:
    return f"addr_{seq:06d}"


def tracking_no(order_id_: str) -> str:
    # Stable per-order, looks like a real courier number.
    digits = "".join(c for c in order_id_ if c.isdigit())[-12:].rjust(12, "0")
    return f"SF{digits}"
