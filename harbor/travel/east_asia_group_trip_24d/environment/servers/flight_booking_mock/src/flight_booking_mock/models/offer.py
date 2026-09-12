from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class FareBreakdown:
    base: float
    taxes: float
    fees: float
    currency: str


@dataclass
class Offer:
    offer_id: str
    created_at: str
    expires_at: str
    payload: dict[str, Any] = field(default_factory=dict)
    priced_price: Optional[float] = None
    priced_at: Optional[str] = None
    price_guarantee_until: Optional[str] = None


@dataclass
class PricedOffer:
    offer_id: str
    priced_total: dict[str, Any]
    previous_total: dict[str, Any]
    price_changed: bool
    change_percent: float
    priced_at: str
    price_guarantee_until: str
