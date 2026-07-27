from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Product:
    product_id: str
    title: str
    brand: str
    category: str
    description: str
    rating: float
    rating_count: int
    sales_count: int
    base_price_minor: int
    return_policy: str


@dataclass(frozen=True)
class Sku:
    sku_id: str
    product_id: str
    attrs: Dict[str, str]
    price_minor: int
