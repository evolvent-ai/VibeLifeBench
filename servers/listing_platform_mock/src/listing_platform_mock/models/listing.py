from dataclasses import dataclass
from typing import Optional


@dataclass
class Listing:
    """A classified marketplace listing.

    ``price_minor`` is integer minor units (分). For ``rent`` it is the
    monthly rent; for ``sale_house`` / ``used_car`` / ``secondhand`` it is
    the total asking price. ``attrs_json`` / ``photos_json`` are JSON-encoded
    flexible fields stored as TEXT.
    """
    listing_id: str
    category: str  # rent | sale_house | used_car | secondhand
    title: str
    city: str
    district: Optional[str]
    community: Optional[str]
    price_minor: int
    area_sqm: Optional[float]
    rooms: Optional[int]
    metro: Optional[str]
    attrs_json: str
    description: Optional[str]
    photos_json: str
    agent_id: Optional[str]
    owner_user_id: Optional[str]
    status: str  # active | delisted
    listed_at: str


@dataclass
class Agent:
    """A listing agent (经纪人)."""
    agent_id: str
    name: str
    agency: str
    phone: str
    rating: float
    deals_count: int
    service_area: Optional[str]
