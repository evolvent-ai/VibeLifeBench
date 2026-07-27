from dataclasses import dataclass
from typing import Optional


@dataclass
class Subscription:
    """A cross-platform subscription (intent to be notified).

    ``type`` is one of price_drop | restock | policy_update | new_content |
    price_target | keyword. ``source`` is the originating platform key
    (e.g. ecommerce, listing_platform, content_platform, gov_policy).
    """
    subscription_id: str
    user_id: str
    source: str
    type: str
    target: str
    condition_json: Optional[str]
    status: str  # active | paused | deleted
    created_at: str
    updated_at: str


@dataclass
class Notification:
    """A pre-seeded historical notification row in the inbox.

    Notifications are static; the server never fabricates time-based events.
    New rows arrive via out-of-band SQL mutation from the orchestrator.
    """
    notification_id: str
    user_id: str
    source: str
    type: str
    subscription_id: Optional[str]
    title: str
    body: Optional[str]
    payload_json: Optional[str]
    created_at: str
    read: bool


@dataclass
class PriceAlert:
    """A target-price watch on a product/item reference."""
    alert_id: str
    user_id: str
    item_ref: str
    target_price_minor: int
    currency: str
    status: str  # active | triggered | cancelled
    created_at: str


@dataclass
class OfficialAccount:
    """A 公众号 / official account a user can subscribe to for a feed."""
    account_id: str
    name: str
    category: Optional[str]
    description: Optional[str]


@dataclass
class OfficialAccountPost:
    """A feed post (article) published by an official account."""
    post_id: str
    account_id: str
    title: str
    summary: Optional[str]
    url: Optional[str]
    published_at: str
