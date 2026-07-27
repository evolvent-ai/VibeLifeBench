from dataclasses import dataclass


@dataclass(frozen=True)
class CartItem:
    cart_item_id: str
    user_id: str
    product_id: str
    sku_id: str
    qty: int
    unit_price_minor: int
    added_at: str
