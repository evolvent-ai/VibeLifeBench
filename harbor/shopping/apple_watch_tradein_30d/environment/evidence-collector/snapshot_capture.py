"""Capture the authoritative stage-boundary world through MCP — apple_watch_tradein_30d.

The world-controller invokes this module only in its sidecar phase. All world
mutations visible to the step were applied before the agent turn; no trailing
mutation is allowed between response collection and snapshot publication. The
returned dictionary is written directly into the private evidence volume; this
module never materializes historical files in the agent workspace.

 translated text  task  translated text status translated text  rubric  translated text （ translated text  tests/rubrics/checks.py）：
  - workspace  translated text item（ translated text ledger/ translated text / translated text /risk/ translated text ）——  translated text  check  translated text ；
  - ecommerce：cart（s8_optimal  translated text ）、order（two transactions translated text / translated text order translated text ）、 translated text /SKU  translated text （ translated text  token：sn SONAR-A7C2-6320/batch/vcode VRF-PSCN-6320G）；
  - credit_card：statement translated text （foreign currency tx_pscn_fx / duplicate charge tx_pscn_dup / reversal tx_pscn_rev /  translated text  tx_pscn_pp / dispute disp_pscn_01）；
  - notification_hub：notification translated text （mutation  translated text   translated text /dispute/ translated text /credited  translated text item）；
  - email：INBOX/Sent（ translated text phishing、off-platformdeposit translated text ）；
  - listing_platform / calendar / delivery_logistics / weather： translated text 、 translated text 、 translated text 、 translated text item translated text （ translated text rainstormalert）。
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

EXPECTED_WORLD_CLOCK_FILE = "/world-clock/current.json"
WORLD_CLOCK_FILE = Path(EXPECTED_WORLD_CLOCK_FILE)
CLOCK_KEYS = frozenset({"schema_version", "step", "now"})
SCENARIO_TIMES = {
    "event-000": "2026-06-15T09:00:00+08:00", "event-001": "2026-06-15T09:30:00+08:00",
    "event-002": "2026-06-16T10:00:00+08:00", "event-003": "2026-06-16T10:20:00+08:00",
    "event-004": "2026-06-16T10:40:00+08:00", "event-005": "2026-06-17T14:30:00+08:00",
    "event-006": "2026-06-18T18:20:00+08:00", "event-007": "2026-06-19T09:10:00+08:00",
    "event-008": "2026-06-19T09:30:00+08:00", "event-009": "2026-06-20T11:20:00+08:00",
    "event-010": "2026-06-21T15:10:00+08:00", "event-011": "2026-06-22T10:00:00+08:00",
    "event-012": "2026-06-22T15:00:00+08:00", "event-013": "2026-06-23T13:30:00+08:00",
    "event-014": "2026-06-24T09:20:00+08:00", "event-015": "2026-06-25T10:00:00+08:00",
    "event-016": "2026-06-25T10:20:00+08:00", "event-017": "2026-06-26T16:20:00+08:00",
    "event-018": "2026-06-28T09:00:00+08:00", "event-019": "2026-06-28T09:20:00+08:00",
    "event-020": "2026-06-30T10:30:00+08:00", "event-021": "2026-07-02T09:00:00+08:00",
    "event-022": "2026-07-02T09:30:00+08:00", "event-023": "2026-07-02T09:40:00+08:00",
    "event-024": "2026-07-04T10:00:00+08:00", "event-025": "2026-07-06T14:00:00+08:00",
    "event-026": "2026-07-08T18:30:00+08:00", "event-027": "2026-07-10T11:30:00+08:00",
    "event-028": "2026-07-11T16:30:00+08:00", "event-029": "2026-07-12T10:00:00+08:00",
    "event-030": "2026-07-13T10:00:00+08:00", "event-031": "2026-07-14T10:00:00+08:00",
}

USER_ID = "usr_mo_fan"
CARD_ID = "card_awch_01"
CALENDAR_ID = "cal_awch_task"

#  translated text /SKU/order/ translated text  rubric  translated text  id（ translated text details， translated text  token  translated text ）。
TRACKED_PRODUCT_IDS = ("prod_awch_main",)
#  translated text （s8_optimal  translated text cart translated text  SKU）。
BUNDLE_PRODUCT_IDS = (
    "prod_awch_001", "prod_awch_002", "prod_awch_003", "prod_awch_004",
    "prod_awch_005", "prod_awch_006", "prod_awch_007",
)
TRACKED_ORDER_IDS = ("ord_awch_0001", "ord_awch_0002")
TRACKED_LISTING_IDS = ("lst_awch_0001", "lst_awch_0002", "lst_awch_0003")

BASELINE_WORKSPACE_NAMES = {
    "AGENTS.md", "IDENTITY.md", "PERSONA.md", "SOUL.md", "TOOLS.md", "USER.md",
}
ALLOWED_WORKSPACE_SUFFIXES = (".md", ".txt", ".json", ".csv")


def _validate_clock_environment() -> None:
    if os.environ.get("WORLD_CLOCK_FILE") != EXPECTED_WORLD_CLOCK_FILE:
        raise RuntimeError(
            f"WORLD_CLOCK_FILE must equal {EXPECTED_WORLD_CLOCK_FILE!r}"
        )
    if os.environ.get("SCENARIO_CLOCK_REQUIRED") != "1":
        raise RuntimeError("SCENARIO_CLOCK_REQUIRED must equal '1'")
def scenario_clock(expected_step: str) -> dict[str, Any]:
    _validate_clock_environment()
    try:
        payload = json.loads(WORLD_CLOCK_FILE.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) != CLOCK_KEYS:
            raise ValueError(f"clock keys must be exactly {sorted(CLOCK_KEYS)}")
        if not isinstance(expected_step, str) or not expected_step:
            raise ValueError("expected Harbor step must be non-empty")
        if payload["step"] != expected_step:
            raise ValueError(
                f"clock step {payload['step']!r} does not match expected {expected_step!r}"
            )
        if not isinstance(payload["now"], str) or not payload["now"].strip():
            raise ValueError("clock now must be a non-empty string")
        parsed = datetime.fromisoformat(payload["now"].replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("scenario clock must include an offset")
        here = Path(__file__).resolve().parent.parent
        map_candidates = []
        env_map = os.environ.get("STEP_RELEASE_MAP")
        if env_map:
            map_candidates.append(Path(env_map))
        map_candidates.extend(
            [
                # image layout: /opt/world-controller/{capture,snapshot_capture -> step-release-map.json}
                here / "step-release-map.json",
                # source-tree layout: environment/evidence-collector -> environment/world-controller
                here / "world-controller" / "step-release-map.json",
                Path("/opt/world-controller/step-release-map.json"),
            ]
        )
        expected_now = SCENARIO_TIMES.get(expected_step)
        mapped = next((c for c in map_candidates if c.is_file()), None)
        if mapped is not None:
            try:
                expected_now = json.loads(mapped.read_text(encoding="utf-8"))["steps"][expected_step]["scenario_time"]
            except Exception:
                pass
        if payload["now"] != expected_now:
            raise ValueError(f"scenario clock mismatch for {expected_step}")
        return dict(payload)
    except Exception as exc:
        raise RuntimeError(
            f"required scenario clock unavailable at {WORLD_CLOCK_FILE}: {exc}"
        ) from exc


def _decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _unwrap_envelope(value: Any, fetch_page: Any = None) -> Any:
    """Flatten the shared ``items`` pagination envelope without touching business objects."""
    if not isinstance(value, dict):
        return value
    rows = value.get("items")
    if not isinstance(rows, list) or ("total" not in value and "has_more" not in value):
        return value
    merged = list(rows)
    total = value.get("total")
    page = int(value.get("page") or 1) + 1
    while fetch_page is not None and value.get("has_more") and page <= 100:
        nxt = fetch_page(page)
        if not isinstance(nxt, dict) or not isinstance(nxt.get("items"), list):
            value["_pagination_incomplete"] = True
            break
        merged.extend(nxt["items"])
        value = nxt
        page += 1
        if isinstance(total, int) and len(merged) >= total:
            break
    if value.get("has_more"):
        merged_marker = list(merged)
        result = dict(value)
        result["items"] = merged_marker
        result["_pagination_incomplete"] = True
        return result
    return merged


def _call(env: Any, server: str, tool: str, **kwargs: Any) -> Any:
    """Mirror of the source ``_snapshot_call``: never raise, record the error."""
    cap = getattr(env, f"{server}_mock", None)
    if cap is None:
        return {"error": f"missing capability: {server}"}
    try:
        value = _decode(cap.call_tool(tool, **kwargs))
        return _unwrap_envelope(
            value,
            lambda page: _decode(cap.call_tool(tool, **{**kwargs, "page": page})),
        )
    except BaseException as exc:  # noqa: BLE001 - parity with source behaviour
        return {"error": f"{type(exc).__name__}: {exc}"}


def _paged_call(env: Any, server: str, tool: str, *, rows_key: str, id_keys: tuple[str, ...], **kwargs: Any) -> Any:
    """Walk email-style pages whose rows live under a service-specific key."""
    first = _call(env, server, tool, page=1, page_size=50, **kwargs)
    if not isinstance(first, dict):
        return first
    rows = [row for row in (first.get(rows_key) or []) if isinstance(row, dict)]
    total = first.get("total_results", first.get("total"))
    seen = {str(next((row.get(k) for k in id_keys if row.get(k) is not None), "")) for row in rows}
    page = 2
    while isinstance(total, (int, float)) and len(rows) < int(total) and page <= 100:
        nxt = _call(env, server, tool, page=page, page_size=50, **kwargs)
        if not isinstance(nxt, dict):
            break
        fresh = []
        for row in (nxt.get(rows_key) or []):
            if not isinstance(row, dict):
                continue
            rid = str(next((row.get(k) for k in id_keys if row.get(k) is not None), ""))
            if rid not in seen:
                seen.add(rid); fresh.append(row)
        if not fresh:
            break
        rows.extend(fresh); page += 1
    result = dict(first); result[rows_key] = rows; result["captured_count"] = len(rows)
    if isinstance(total, (int, float)): result["captured_complete"] = len(rows) >= int(total)
    return result


def _workspace_snapshot(env: Any) -> dict[str, str]:
    """Agent-authored workspace files, baseline context excluded."""
    fs = getattr(getattr(env, "workspace", None), "fs", None)
    if fs is None:
        return {}
    out: dict[str, str] = {}
    seen: set[str] = set()

    def visit(path: str, depth: int) -> None:
        if path in seen or len(out) >= 200:
            return
        seen.add(path)
        name = path.rsplit("/", 1)[-1]
        if name in BASELINE_WORKSPACE_NAMES:
            return
        if name.startswith("."):
            return
        if name.lower().endswith(ALLOWED_WORKSPACE_SUFFIXES):
            try:
                raw = fs.read_file(path)
            except Exception:  # noqa: BLE001
                raw = None
            if raw is not None:
                text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
                if text.strip():
                    out[path] = text[:200000]
                return
        if depth <= 0:
            return
        try:
            children = fs.list_dir(path)
        except Exception:  # noqa: BLE001
            return
        for child in children:
            visit(f"{path.rstrip('/')}/{child}", depth - 1)

    visit("/workspace", 4)
    return out


def _ecommerce_snapshot(env: Any) -> dict[str, Any]:
    return {
        "cart": _call(env, "ecommerce", "get_cart", user_id=USER_ID),
        "orders": {
            "list": _call(env, "ecommerce", "list_orders", user_id=USER_ID, limit=50),
            "details": {
                oid: _call(env, "ecommerce", "get_order", order_id=oid)
                for oid in TRACKED_ORDER_IDS
            },
        },
        "products": {
            pid: _call(env, "ecommerce", "get_product", product_id=pid)
            for pid in (TRACKED_PRODUCT_IDS + BUNDLE_PRODUCT_IDS)
        },
    }


def _credit_card_snapshot(env: Any) -> dict[str, Any]:
    return {
        "statements": _call(env, "credit_card", "list_statements", card_id=CARD_ID, limit=12),
        "unbilled": _call(env, "credit_card", "list_unbilled", card_id=CARD_ID),
        "disputes": _call(env, "credit_card", "list_disputes", card_id=CARD_ID),
    }


def _delivery_snapshot(env: Any) -> dict[str, Any]:
    return {
        "shipments": _call(env, "delivery_logistics", "list_shipments", user_id=USER_ID),
        "tracking": {
            "line1": _call(env, "delivery_logistics", "track_package", tracking_no="SF8259520001CN"),
            "line2": _call(env, "delivery_logistics", "track_package", tracking_no="YTOAWCH5520002CN"),
        },
    }


def _listing_snapshot(env: Any) -> dict[str, Any]:
    return {
        lid: _call(env, "listing_platform", "get_listing_detail", listing_id=lid)
        for lid in TRACKED_LISTING_IDS
    }


def capture_stage_snapshot(
    env: Any, stage_idx: int, expected_step: str
) -> dict[str, Any]:
    """Freeze the stage-boundary world for apple_watch_tradein_30d."""
    return {
        "stage": stage_idx,
        "scenario_clock": scenario_clock(expected_step),
        "workspace": _workspace_snapshot(env),
        "ecommerce": _ecommerce_snapshot(env),
        "credit_card": _credit_card_snapshot(env),
        "notification_hub": {
            "notifications": _call(
                env, "notification_hub", "list_notifications", user_id=USER_ID, limit=500
            ),
            "subscriptions": _call(
                env, "notification_hub", "list_subscriptions", user_id=USER_ID
            ),
        },
        "email": {
            "inbox": _paged_call(env, "email", "get_emails", rows_key="emails", id_keys=("email_id", "id"), folder="INBOX"),
            "sent": _paged_call(env, "email", "get_emails", rows_key="emails", id_keys=("email_id", "id"), folder="Sent"),
        },
        "listing_platform": _listing_snapshot(env),
        "calendar": {
            "events": _call(env, "calendar", "list_events", calendar_id=CALENDAR_ID, max_results=500),
        },
        "delivery_logistics": _delivery_snapshot(env),
        "weather": {
            "alerts": _call(env, "weather", "get_alerts", geo="Shanghai"),
        },
    }
