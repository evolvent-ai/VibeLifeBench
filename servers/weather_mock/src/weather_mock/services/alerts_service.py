from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from ..backends.sqlite_backend import SQLiteBackend
from ..backends.notification_sink import deliver, validate_file_sink
from ..utils.exceptions import WeatherNotFound, SinkOutsideWorkspace
from ..utils.geo_resolver import resolve_geo


class AlertsService:
    """Read-through over the ``alerts`` table plus subscription writes.

    ``active`` is honored as a literal column — the orchestrator (not the
    server) flips alerts on/off via stage `mutation` events.
    """

    def __init__(self, be: SQLiteBackend, workspace_root: Optional[str] = None) -> None:
        self.be = be
        self.workspace_root = workspace_root

    @staticmethod
    def alert_id_for(kind: str, source_key: str, seq: int = 0) -> str:
        base = f"{kind}:{source_key}:{seq}".encode("utf-8")
        h = hashlib.sha256(base).hexdigest()[:10]
        return f"alt_{kind}_{h}"

    def _resolve(self, geo: Any) -> dict:
        row = resolve_geo(
            geo,
            self.be.fetchall("SELECT * FROM locations ORDER BY geo_key"),
        )
        if row is None:
            raise WeatherNotFound("no_nearby_location")
        return row

    def get_active_alerts_for_geo(self, geo: Any) -> list[dict]:
        loc = self._resolve(geo)
        rows = self.be.fetchall(
            "SELECT * FROM alerts WHERE active = 1 ORDER BY start_dt"
        )
        out: list[dict] = []
        for r in rows:
            areas = json.loads(r["areas_json"])
            if loc["geo_key"] not in areas:
                continue
            out.append(
                {
                    "alert_id": r["alert_id"],
                    "kind": r["kind"],
                    "severity": r["severity"],
                    "start": r["start_dt"],
                    "end": r["end_dt"],
                    "areas": areas,
                    "description": r["description"],
                }
            )
        return out

    # ------------------------------------------------------------------
    # Subscription handling
    # ------------------------------------------------------------------

    def create_subscription(self, geo: Any, sink: str) -> dict:
        loc = self._resolve(geo)
        try:
            validate_file_sink(sink, self.workspace_root)
        except SinkOutsideWorkspace as e:
            raise SinkOutsideWorkspace(str(e))
        sub_id = "sub_" + uuid.uuid4().hex[:20]
        now = datetime.now(timezone.utc).isoformat() + "Z"
        self.be.execute(
            """INSERT INTO alert_subscriptions (sub_id, geo_key, sink, created_at, active)
               VALUES (?, ?, ?, ?, 1)""",
            (sub_id, loc["geo_key"], sink, now),
        )
        return {
            "subscription_id": sub_id,
            "geo_key": loc["geo_key"],
            "sink": sink,
        }

    def fan_out(self) -> int:
        """Deliver any active alerts to matching subscriptions, once per pair."""
        subs = self.be.fetchall(
            "SELECT * FROM alert_subscriptions WHERE active = 1"
        )
        active_alerts = self.be.fetchall(
            "SELECT * FROM alerts WHERE active = 1"
        )
        delivered_count = 0
        for sub in subs:
            for alert in active_alerts:
                areas = json.loads(alert["areas_json"])
                if sub["geo_key"] not in areas:
                    continue
                prior = self.be.fetchone(
                    """SELECT id FROM notifications
                       WHERE sub_id = ? AND alert_id = ? LIMIT 1""",
                    (sub["sub_id"], alert["alert_id"]),
                )
                if prior:
                    continue
                now = datetime.now(timezone.utc).isoformat() + "Z"
                payload = {
                    "alert_id": alert["alert_id"],
                    "geo_key": sub["geo_key"],
                    "kind": alert["kind"],
                    "severity": alert["severity"],
                    "start": alert["start_dt"],
                    "end": alert["end_dt"],
                    "description": alert["description"],
                    "delivered_at": now,
                }
                ok = False
                try:
                    ok = deliver(sub["sink"], payload, workspace_root=self.workspace_root)
                except SinkOutsideWorkspace:
                    ok = False
                except Exception:
                    ok = False
                self.be.execute(
                    """INSERT INTO notifications
                       (created_at, channel, sub_id, alert_id, payload_json, delivered)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        now,
                        sub["sink"],
                        sub["sub_id"],
                        alert["alert_id"],
                        json.dumps(payload, ensure_ascii=False),
                        1 if ok else 0,
                    ),
                )
                if ok:
                    delivered_count += 1
        return delivered_count
