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
from ..utils.world_clock import now_iso_z as _world_now_iso_z


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

    @staticmethod
    def _covers_location(geo_row: dict, areas: Any) -> bool:
        """True when the alert's ``areas_json`` names this location.

        Alerts are seeded with human-readable area strings (city/district)
        while locations are keyed by ``geo_key``, so a raw ``geo_key in areas``
        membership test never matches. Match the location's identifying tokens
        (its geo_key or city name) against the area strings instead.
        """
        if not isinstance(areas, list):
            return False
        tokens = {
            str(geo_row.get("geo_key") or "").strip(),
            str(geo_row.get("city") or "").strip(),
        }
        tokens.discard("")
        for area in areas:
            text = str(area).strip()
            if text and (text in tokens or any(token in text for token in tokens)):
                return True
        return False

    def get_active_alerts_for_geo(self, geo: Any) -> list[dict]:
        loc = self._resolve(geo)
        rows = self.be.fetchall(
            "SELECT * FROM alerts WHERE active = 1 ORDER BY start_dt"
        )
        out: list[dict] = []
        for r in rows:
            areas = json.loads(r["areas_json"])
            if not self._covers_location(loc, areas):
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
                    # The activation flag is part of the row's authoritative
                    # state; dropping it makes "is this alert on?" unreadable.
                    "active": int(r["active"]),
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
        now = _world_now_iso_z()
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
            try:
                sub_loc = self._resolve(sub["geo_key"])
            except Exception:
                continue
            for alert in active_alerts:
                areas = json.loads(alert["areas_json"])
                if not self._covers_location(sub_loc, areas):
                    continue
                prior = self.be.fetchone(
                    """SELECT id FROM notifications
                       WHERE sub_id = ? AND alert_id = ? LIMIT 1""",
                    (sub["sub_id"], alert["alert_id"]),
                )
                if prior:
                    continue
                now = _world_now_iso_z()
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
