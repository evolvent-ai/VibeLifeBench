"""Lightweight value validators for ISO codes and enum-like strings."""

import re

from .exceptions import ValidationError

_ALPHA2_RE = re.compile(r"^[A-Z]{2}$")

PURPOSES = ("tourism", "business", "transit")
DOC_KINDS = ("passport", "photo", "itinerary", "bank_statement")
DELIVERY_TYPES = ("evisa", "paper", "embassy")


def is_iso_alpha2(code: str) -> bool:
    return isinstance(code, str) and bool(_ALPHA2_RE.match(code))


def normalize_country_code(code: str) -> str:
    if not isinstance(code, str):
        raise ValidationError(f"country code must be a string, got {type(code).__name__}")
    norm = code.strip().upper()
    if not _ALPHA2_RE.match(norm) and norm != "*" and norm != "EU":
        raise ValidationError(f"invalid ISO alpha-2 country code: {code!r}")
    return norm


def validate_purpose(purpose: str) -> str:
    if purpose not in PURPOSES:
        raise ValidationError(
            f"invalid purpose: {purpose!r}; must be one of {PURPOSES}",
            code="invalid_purpose",
        )
    return purpose


def validate_doc_kind(kind: str) -> str:
    if kind not in DOC_KINDS:
        raise ValidationError(
            f"invalid document kind: {kind!r}; must be one of {DOC_KINDS}",
            code="invalid_kind",
        )
    return kind


def validate_delivery(delivery: str) -> str:
    if delivery not in DELIVERY_TYPES:
        raise ValidationError(
            f"invalid delivery: {delivery!r}; must be one of {DELIVERY_TYPES}",
            code="invalid_delivery",
        )
    return delivery
