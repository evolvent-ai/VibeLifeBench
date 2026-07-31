from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Address:
    address_id: str
    user_id: str
    recipient: str
    phone: str
    province: str
    city: str
    district: str
    detail: str
    postal_code: str
    is_default: bool


@dataclass(frozen=True)
class Coupon:
    code: str
    kind: str  # percent_off | flat_off | free_shipping
    value_bp_or_minor: int  # basis points for percent_off, 分 for flat_off, 0 for free_shipping
    min_spend_minor: int
    valid_from: str
    valid_until: str
    category_restriction: Optional[str]
    max_uses: int
    used_count: int
    active: bool
