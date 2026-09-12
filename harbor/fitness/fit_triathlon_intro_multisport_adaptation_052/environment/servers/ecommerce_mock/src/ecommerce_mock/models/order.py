from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Order:
    order_id: str
    user_id: str
    address_id: str
    payment_method: str
    subtotal_minor: int
    discount_minor: int
    shipping_minor: int
    total_minor: int
    status: str
    placed_at: str
    note: Optional[str]
    tracking_no: Optional[str]


@dataclass(frozen=True)
class OrderItem:
    item_id: str
    order_id: str
    product_id: str
    sku_id: str
    qty: int
    unit_price_minor: int
    line_total_minor: int


@dataclass(frozen=True)
class Refund:
    refund_id: str
    order_id: str
    item_id: str
    qty: int
    reason: str
    status: str
    opened_at: str
    resolved_at: Optional[str]
    refund_amount_minor: int
