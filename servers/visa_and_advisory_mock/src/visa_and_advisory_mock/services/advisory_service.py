"""Advisory get/subscribe + fan-out helper."""

from datetime import datetime, timezone
from typing import Any, Dict, List

from ..backends.advisory_backend import AdvisoryBackend
from ..models.advisory import Advisory, AdvisorySubscription
from ..utils.ids import IdGenerator
from ..utils.validators import normalize_country_code
from .notification_service import NotificationService


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class AdvisoryService:
    def __init__(
        self,
        advisory_backend: AdvisoryBackend,
        ids: IdGenerator,
        notifications: NotificationService,
    ):
        self.advisory_backend = advisory_backend
        self.ids = ids
        self.notifications = notifications

    def get_advisory(self, country_code: str) -> Dict[str, Any]:
        code = normalize_country_code(country_code)
        adv = self.advisory_backend.get(code)
        if adv is None:
            return {
                "country_code": code,
                "level": 1,
                "text": "No advisory on file.",
                "last_updated": None,
            }
        return {
            "country_code": adv.country_code,
            "level": int(adv.level),
            "text": adv.text,
            "last_updated": adv.updated_at,
        }

    def subscribe(self, country_code: str, sink: str) -> Dict[str, Any]:
        code = normalize_country_code(country_code)
        sub_id = self.ids.subscription_id()
        sub = AdvisorySubscription(
            sub_id=sub_id,
            country_code=code,
            sink=sink,
            created_at=_now_iso(),
        )
        self.advisory_backend.insert_subscription(sub)
        return {"subscription_id": sub_id, "country_code": code, "sink": sink}

    # ---- helpers used by admin_service -------------------------------------

    def upsert_advisory(self, country_code: str, level: int, text: str) -> tuple[Advisory, int]:
        """Upsert and return (new_advisory, previous_level).

        previous_level == new level when the row didn't exist before (treated
        as no-change for fan-out purposes).
        """
        code = normalize_country_code(country_code)
        prior = self.advisory_backend.get(code)
        prev_level = int(prior.level) if prior is not None else int(level)
        new_text = text or (prior.text if prior is not None else "")
        adv = Advisory(
            country_code=code,
            level=int(level),
            text=new_text,
            updated_at=_now_iso(),
        )
        self.advisory_backend.upsert(adv)
        return adv, prev_level

    def fanout_advisory_change(
        self,
        country_code: str,
        from_level: int,
        to_level: int,
        text: str,
    ) -> int:
        """Write one notifications row per active subscription. Returns count."""
        subs = self.advisory_backend.list_subscriptions_for(country_code)
        for sub in subs:
            self.notifications.write(
                channel="advisory",
                payload={
                    "country_code": country_code,
                    "from_level": int(from_level),
                    "to_level": int(to_level),
                    "text": text,
                    "sink": sub.sink,
                    "subscription_id": sub.sub_id,
                },
            )
        return len(subs)
