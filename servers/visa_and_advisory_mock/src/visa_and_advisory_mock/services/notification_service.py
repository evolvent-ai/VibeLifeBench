"""Single writer for the ``notifications`` table.

Both the advisory and admin services use this so that channel/payload
shapes are consistent.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from ..backends.advisory_backend import AdvisoryBackend
from ..models.advisory import Notification
from ..utils.ids import IdGenerator


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class NotificationService:
    def __init__(self, advisory_backend: AdvisoryBackend, ids: IdGenerator):
        self.advisory_backend = advisory_backend
        self.ids = ids

    def write(self, channel: str, payload: Dict[str, Any]) -> Notification:
        notif = Notification(
            id=self.ids.notification_id(),
            created_at=_now_iso(),
            channel=channel,
            payload=payload,
        )
        self.advisory_backend.insert_notification(notif)
        return notif
