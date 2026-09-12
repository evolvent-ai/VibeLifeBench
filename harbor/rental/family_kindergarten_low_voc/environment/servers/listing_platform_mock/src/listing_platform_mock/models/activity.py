from dataclasses import dataclass
from typing import Optional


@dataclass
class SavedListing:
    user_id: str
    listing_id: str
    saved_at: str


@dataclass
class Viewing:
    viewing_id: str
    user_id: str
    listing_id: str
    agent_id: Optional[str]
    scheduled_at: str
    status: str  # scheduled | cancelled
    created_at: str


@dataclass
class Contact:
    contact_id: str
    user_id: str
    listing_id: str
    agent_id: Optional[str]
    message: str
    created_at: str


@dataclass
class MarketStat:
    stat_id: str
    area: str
    city: Optional[str]
    category: str
    avg_price_minor: int
    unit: str  # per_month | total | per_sqm
    sample_size: int
    period: str


@dataclass
class SearchSubscription:
    subscription_id: str
    user_id: str
    query_json: str
    created_at: str
