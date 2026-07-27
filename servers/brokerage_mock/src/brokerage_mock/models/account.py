"""Account, position, and order dataclasses (DB-row mirrors)."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Account:
    account_id: str
    user_id: str
    broker: str
    account_type: str
    cash_minor: int
    opened_at: str
    status: str


@dataclass(frozen=True)
class Position:
    position_id: int
    account_id: str
    symbol: str
    kind: str
    qty_milli: int
    avg_cost_minor: int


@dataclass(frozen=True)
class Order:
    order_id: str
    account_id: str
    symbol: str
    side: str
    qty_milli: int
    order_type: str
    limit_price_minor: Optional[int]
    tif: str
    status: str
    placed_at: str
    filled_at: Optional[str]
    fill_price_minor: Optional[int]
