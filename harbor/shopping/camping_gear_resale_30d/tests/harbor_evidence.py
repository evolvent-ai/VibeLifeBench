"""Harbor-native access to immutable frozen evidence.

The scoring side reads only ``<root>/stages/stage-NN``.  It never carries an
MCP client or a writable workspace handle, so an earlier stage cannot observe
later world mutations.  Missing, malformed, or tampered evidence raises
``EvidenceError`` instead of being converted into an empty result.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REQUIRED_FILES = ("snapshot.json", "trace.json", "response.txt", "trajectory.json")


class EvidenceError(RuntimeError):
    """Frozen evidence is missing, unreadable, or fails its manifest."""


class HarborEvidence:
    """Validated, cached reader over the private Harbor evidence tree."""

    def __init__(self, root: Path | str = DEFAULT_EVIDENCE_ROOT) -> None:
        self.root = Path(root)
        self._validated: set[int] = set()
        self._cache: dict[tuple[int, str], Any] = {}
        self._eval_stage: int | None = None

    def set_eval_stage(self, stage: int | None) -> None:
        self._eval_stage = None if stage is None else int(stage)

    def _resolve_stage(self) -> int:
        if self._eval_stage is not None:
            return self._eval_stage
        stages_root = self.root / "stages"
        stages = []
        if stages_root.is_dir():
            for path in stages_root.glob("stage-*"):
                try:
                    stages.append(int(path.name.removeprefix("stage-")))
                except ValueError:
                    continue
        return max(stages) if stages else 0

    def _stage_dir(self, stage: int) -> Path:
        return self.root / "stages" / f"stage-{int(stage):02d}"

    @staticmethod
    def _read_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise EvidenceError(f"unreadable evidence file {path}: {exc}") from exc
        except ValueError as exc:
            raise EvidenceError(f"malformed JSON in {path}: {exc}") from exc

    def validate_stage(self, stage: int) -> Path:
        stage = int(stage)
        stage_dir = self._stage_dir(stage)
        if stage in self._validated:
            return stage_dir
        if not stage_dir.is_dir():
            raise EvidenceError(f"no frozen evidence for stage {stage} at {stage_dir}")
        manifest_path = stage_dir / "manifest.json"
        if not manifest_path.is_file():
            raise EvidenceError(f"stage {stage} has no manifest at {manifest_path}")
        manifest = self._read_json(manifest_path)
        if not isinstance(manifest, dict):
            raise EvidenceError(f"stage {stage} manifest is not an object")
        if manifest.get("schema_version") != 1 or manifest.get("kind") != "stage":
            raise EvidenceError(f"stage {stage} manifest type mismatch")
        try:
            declared_stage = int(manifest.get("virtual_stage", -1))
        except (TypeError, ValueError) as exc:
            raise EvidenceError(f"stage {stage} manifest has invalid virtual_stage") from exc
        if declared_stage != stage:
            raise EvidenceError(f"stage {stage} manifest number mismatch: {declared_stage}")
        hashes = manifest.get("hashes")
        if not isinstance(hashes, dict) or not hashes:
            raise EvidenceError(f"stage {stage} manifest has no hashes")
        missing = [name for name in REQUIRED_FILES if name not in hashes]
        if missing:
            raise EvidenceError(f"stage {stage} missing required files: {missing}")
        actual_paths = {
            str(path.relative_to(stage_dir)): path
            for path in stage_dir.rglob("*")
            if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
        }
        if set(actual_paths) != set(hashes):
            raise EvidenceError(
                f"stage {stage} manifest/disk mismatch: "
                f"undeclared={sorted(set(actual_paths) - set(hashes))[:5]} "
                f"missing={sorted(set(hashes) - set(actual_paths))[:5]}"
            )
        for relative, expected in hashes.items():
            target = actual_paths.get(relative)
            if target is None or not isinstance(expected, str):
                raise EvidenceError(f"stage {stage} invalid hash entry: {relative}")
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                raise EvidenceError(f"stage {stage} file {relative} hash mismatch")
        self._validated.add(stage)
        return stage_dir

    def _load(self, stage: int, filename: str) -> Any:
        key = (int(stage), filename)
        if key in self._cache:
            return self._cache[key]
        stage_dir = self.validate_stage(int(stage))
        path = stage_dir / filename
        value = path.read_text(encoding="utf-8") if filename.endswith(".txt") else self._read_json(path)
        self._cache[key] = value
        return value

    def snapshot(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "snapshot.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} snapshot is not an object")
        if "error" in value and not any(key != "error" for key in value):
            raise EvidenceError(f"stage {stage} snapshot is a captured error: {value['error']!r}")
        return value

    def trace(self, stage: int) -> list[dict[str, Any]]:
        value = self._load(stage, "trace.json")
        if not isinstance(value, list):
            raise EvidenceError(f"stage {stage} trace is not a list")
        return value

    def response(self, stage: int) -> str:
        value = self._load(stage, "response.txt")
        return value if isinstance(value, str) else str(value)

    def trajectory(self, stage: int) -> dict[str, Any]:
        value = self._load(stage, "trajectory.json")
        if not isinstance(value, dict):
            raise EvidenceError(f"stage {stage} trajectory is not an object")
        return value

    def published_stages(self) -> list[int]:
        stages_root = self.root / "stages"
        if not stages_root.is_dir():
            return []
        found = []
        for path in sorted(stages_root.glob("stage-*")):
            try:
                found.append(int(path.name.removeprefix("stage-")))
            except ValueError:
                continue
        return found

    def _current_snapshot(self) -> dict[str, Any]:
        return self.snapshot(self._resolve_stage())

    @staticmethod
    def _walk(value: Any):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from HarborEvidence._walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from HarborEvidence._walk(child)

    def backend_read(self, server: str, tool: str, **kwargs: Any) -> Any:
        """Serve a captured backend projection for the currently bound stage."""
        snapshot = self._current_snapshot()
        section = snapshot.get(server)
        if not isinstance(section, dict):
            raise EvidenceError(f"stage {self._resolve_stage()} has no {server} snapshot")
        aliases = {
            ("ecommerce", "get_product"): "product",
            ("ecommerce", "get_cart"): "cart",
            ("delivery_logistics", "list_shipments"): "shipments",
            ("credit_card", "get_card"): "card",
            ("credit_card", "get_statement"): "statement",
            ("credit_card", "list_unbilled"): "unbilled",
            ("credit_card", "list_disputes"): "disputes",
            ("listing_platform", "search_listings"): "listings",
            ("calendar", "list_calendars"): "calendars",
            ("calendar", "list_events"): "events",
            ("notification_hub", "list_subscriptions"): "subscriptions",
            ("notification_hub", "list_notifications"): "notifications",
            ("weather", "get_alerts"): "alerts",
            ("weather", "get_forecast_daily"): "forecast",
            ("weather", "get_aqi"): "aqi",
        }
        key = aliases.get((server, tool), tool)
        if server == "ecommerce" and tool == "get_order":
            key = "resale_order" if kwargs.get("order_id") == "ord_rstent_0002" else "order"
        if server == "ecommerce" and tool == "list_orders":
            key = "orders"
        if server == "delivery_logistics" and tool == "get_shipment":
            key = "resale" if kwargs.get("shipment_id") == "shp_rstent_0002" else "primary"
        if server == "listing_platform" and tool == "get_listing_detail":
            listing_id = str(kwargs.get("listing_id") or "")
            key = "listing" if listing_id == "lst_rstent_0001" else "listings"
        if server == "notification_hub" and tool == "get_notification":
            rows = section.get("notifications", [])
            for row in self._walk(rows):
                if str(row.get("notification_id")) == str(kwargs.get("notification_id")):
                    if self._contains_error_envelope(row):
                        raise EvidenceError(
                            f"stage {self._resolve_stage()} notification contains an error projection"
                        )
                    return row
            return {}
        if server == "email" and tool in {"search_emails", "get_emails"}:
            folder = str(kwargs.get("folder", "INBOX")).lower()
            key = "sent" if folder == "sent" else "inbox"
            data = section.get(key, {})
            if isinstance(data, dict) and "listing" in data:
                listing = data["listing"]
                if self._contains_error_envelope(data):
                    raise EvidenceError(
                        f"stage {self._resolve_stage()} email.{tool} contains an error projection"
                    )
                if tool == "search_emails":
                    query = str(kwargs.get("query") or "").lower()
                    rows = listing.get("emails") if isinstance(listing, dict) else None
                    details = data.get("details") or []
                    detail_by_id = {
                        str(row.get("email_id")): row
                        for row in details
                        if isinstance(row, dict) and row.get("email_id") is not None
                    }
                    filtered = []
                    for row in rows or []:
                        if not isinstance(row, dict):
                            continue
                        detail = detail_by_id.get(str(row.get("email_id")), {})
                        haystack = " ".join(
                            str(row.get(field) or "")
                            for field in ("subject", "from_addr", "body_text")
                        )
                        haystack += " " + " ".join(
                            str(detail.get(field) or "")
                            for field in ("subject", "from_addr", "body_text")
                        )
                        if query in haystack.lower():
                            merged = dict(row)
                            if isinstance(detail, dict):
                                for field in ("body_text", "body_html", "in_reply_to", "references"):
                                    if detail.get(field) is not None:
                                        merged[field] = detail[field]
                            filtered.append(merged)
                    page = int(kwargs.get("page") or 1)
                    page_size = int(kwargs.get("page_size") or 20)
                    start = max(0, (page - 1) * page_size)
                    page_rows = filtered[start:start + page_size]
                    result = dict(listing) if isinstance(listing, dict) else {}
                    result.update({
                        "query": kwargs.get("query") or "",
                        "folder": "INBOX" if folder != "sent" else "Sent",
                        "emails": page_rows,
                        "total_results": len(filtered),
                        "current_page": page,
                        "page_size": page_size,
                    })
                    result["total_pages"] = max(1, (len(filtered) + page_size - 1) // page_size)
                    return result
                return listing
        value = section.get(key)
        if server == "listing_platform" and tool == "get_listing_detail" and isinstance(value, list):
            listing_id = str(kwargs.get("listing_id") or "")
            for row in self._walk(value):
                if str(row.get("listing_id")) == listing_id:
                    if self._contains_error_envelope(row):
                        raise EvidenceError(
                            f"stage {self._resolve_stage()} listing contains an error projection"
                        )
                    return row
            return {}
        if self._contains_error_envelope(value):
            raise EvidenceError(
                f"stage {self._resolve_stage()} {server}.{tool} contains an error projection"
            )
        return value

    @classmethod
    def _contains_error_envelope(cls, value: Any) -> bool:
        if isinstance(value, dict):
            if value.get("error") and set(value) <= {"error", "code", "message"}:
                return True
            return any(cls._contains_error_envelope(child) for child in value.values())
        if isinstance(value, list):
            return any(cls._contains_error_envelope(child) for child in value)
        return False

    def workspace_file(self, path: str) -> str:
        workspace = self._current_snapshot().get("workspace")
        if not isinstance(workspace, dict):
            return ""
        basename = str(path).rstrip("/").rsplit("/", 1)[-1]
        for key, value in workspace.items():
            if str(key).rstrip("/").rsplit("/", 1)[-1] == basename:
                return value if isinstance(value, str) else str(value)
        return ""


def snapshot(env, stage: int) -> dict[str, Any]:
    return env.snapshot(stage)


def trace(env, stage: int) -> list[dict[str, Any]]:
    return env.trace(stage)


def response(env, stage: int) -> str:
    return env.response(stage)
