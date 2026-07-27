"""Market data dataclasses (quotes, funds)."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QuoteDaily:
    symbol: str
    date: str
    open_minor: int
    close_minor: int
    high_minor: int
    low_minor: int
    volume: int


@dataclass(frozen=True)
class Fund:
    fund_code: str
    fund_name: str
    category: str
    current_nav_minor: int
    ytd_return_bp: int
    risk_level: int
    manager: Optional[str]
    inception: Optional[str]
