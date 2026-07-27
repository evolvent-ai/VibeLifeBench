"""ID and code generators.

All IDs are domain-prefixed. Tracking numbers and confirmation codes are
deterministic hashes of their input strings — identical inputs always
produce the same value (no RNG).
"""
import hashlib

# Numeric-only tracking number style (mirrors 顺丰 / 京东 / 中通 length).
TRACKING_DIGITS = 13


CARRIER_PREFIX = {
    "SF Express": "SF",
    "JD Logistics": "JD",
    "ZTO Express": "ZTO",
    "YTO": "YT",
    "STO": "ST",
}


def shipment_id(seq: int) -> str:
    return f"ship_{seq:08d}"


def pickup_id(seq: int) -> str:
    return f"pck_{seq:08d}"


def ticket_id(seq: int) -> str:
    return f"tkt_{seq:08d}"


def event_id(seq: int) -> str:
    return f"evt_{seq:010d}"


def subscription_id(seq: int) -> str:
    return f"sub_{seq:08d}"


def address_id(seq: int) -> str:
    return f"addr_{seq:06d}"


def tracking_no(carrier: str, input_str: str) -> str:
    """Numeric-only carrier-prefixed tracking number, fully deterministic in ``input_str``."""
    digest = hashlib.sha256(input_str.encode("utf-8")).hexdigest()
    # Map hex → decimal digits by taking the integer value of the digest and
    # padding/truncating to TRACKING_DIGITS.
    n = int(digest, 16) % (10 ** TRACKING_DIGITS)
    digits = str(n).rjust(TRACKING_DIGITS, "0")
    prefix = CARRIER_PREFIX.get(carrier, "DL")
    return f"{prefix}{digits}"


def confirmation_code(input_str: str) -> str:
    """Carrier confirmation code in ``DL-XXXX-XXXX`` form, deterministic in ``input_str``."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    digest = hashlib.sha256(input_str.encode("utf-8")).hexdigest().upper()
    # Map two hex chars to one alphabet char by reducing mod len(alphabet).
    pairs = [digest[i : i + 2] for i in range(0, 16, 2)]
    chars = [alphabet[int(p, 16) % len(alphabet)] for p in pairs]
    a = "".join(chars[:4])
    b = "".join(chars[4:8])
    return f"DL-{a}-{b}"


def stable_hash_int(*parts: str) -> int:
    """Deterministic non-negative int from string parts (for carrier selection)."""
    blob = "|".join(parts).encode("utf-8")
    return int(hashlib.sha256(blob).hexdigest(), 16)
