"""Harbor-only helpers shared by the migrated stroller rubrics."""
from __future__ import annotations

import json
import re
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from harbor_evidence import snapshot, trace, response
from ._scenario import (
    ALL_SERVERS, OUTPUT_PATHS, STAGE_COUNT, STAGE_EXPECTED_SERVERS,
    THREAD_IDS, THREAD_LABELS, THREAD_TERMS, THREAD_EVIDENCE,
)

CORE_WORKSPACE_PATHS = (
    "/workspace/order_tracker.md", "/workspace/decision_log.md",
    "/workspace/risk_register.md", "/workspace/HEARTBEAT.md",
)
WS = {
    "gear": "/workspace/gear_plan.md", "budget": "/workspace/budget.md",
    "decision": "/workspace/decision_log.md", "risk": "/workspace/risk_register.md",
    "tracker": "/workspace/order_tracker.md", "evidence": "/workspace/evidence_log.md",
    "summary": "/workspace/final_summary.md", "heartbeat": "/workspace/HEARTBEAT.md",
}
_ACTIVE_STAGE: ContextVar[int] = ContextVar("active_stage", default=STAGE_COUNT - 1)


@dataclass(frozen=True)
class CartPlan:
    sku_ids: tuple[str, ...]
    coupon_codes: tuple[str, ...]
    subtotal_minor: int
    total_minor: int
    product_titles: tuple[str, ...] = ()


def _stage(env, idx: int | None = None) -> int:
    return _ACTIVE_STAGE.get() if idx is None else int(idx)


def _files(env, idx: int | None = None) -> dict[str, str]:
    value = snapshot(env, _stage(env, idx)).get("workspace", {})
    if not isinstance(value, dict):
        return {}
    raw = value.get("files") if isinstance(value.get("files"), dict) else value
    out: dict[str, str] = {}
    if not isinstance(raw, dict):
        return out
    for key, item in raw.items():
        if isinstance(item, bytes):
            item = item.decode("utf-8", errors="replace")
        if isinstance(item, str):
            name = str(key)
            if not name.startswith("/"):
                name = "/workspace/" + name
            out[name] = item
    return out


def _file_text(env, path: str, idx: int | None = None) -> str:
    wanted = str(path)
    if not wanted.startswith("/"):
        wanted = "/workspace/" + wanted
    files = _files(env, idx)
    if wanted in files:
        return files[wanted]
    suffix = "/" + wanted.rsplit("/", 1)[-1]
    return next((text for name, text in files.items() if name.endswith(suffix)), "")


def files_text(env, keys: Iterable[str]) -> str:
    return "\n".join(_file_text(env, WS.get(key, key)) for key in keys)


def scoped_text(env, keys: Iterable[str], idx: int | None = None) -> str:
    stage = _stage(env, idx)
    return (files_text(env, keys) + "\n" + response(env, stage)).lower()


def _agent_response(env, idx: int) -> str:
    return response(env, idx)


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        return "\n".join(_flatten(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return "\n".join(_flatten(item) for item in value)
    return ""


def _normalize(text: Any) -> str:
    return _flatten(text).lower()


def _count_any(text: str, words: Iterable[str]) -> int:
    low = _normalize(text)
    return sum(1 for word in words if str(word).lower() in low)


def _has_bad_advice(text: str, phrases: Iterable[str], *, window: int = 16) -> bool:
    low = _normalize(text)
    negations = ("do not", "don't", "never", "not", "refuse", "reject", "avoid", "without")
    for phrase in phrases:
        needle = str(phrase).lower()
        start = 0
        while True:
            pos = low.find(needle, start)
            if pos < 0:
                break
            prefix = low[max(0, pos - window):pos]
            if not any(cue in prefix for cue in negations):
                return True
            start = pos + len(needle)
    return False


def _trace_calls(env, idx: int | None = None) -> list[dict[str, Any]]:
    rows = trace(env, _stage(env, idx))
    return [dict(row) for row in rows if isinstance(row, dict)]


def _successful(call: dict[str, Any]) -> bool:
    flag = call.get("succeeded", call.get("success"))
    if flag is False:
        return False
    if flag is None and call.get("result") is None:
        return False
    result = call.get("result")
    return not (isinstance(result, dict) and result.get("error"))


def _server(name: str) -> str | None:
    norm = str(name or "").lower().replace("-", "_")
    for server in ALL_SERVERS:
        if norm.startswith(server + "__") or norm.startswith(server + "_"):
            return server
    return None


def _stage_called_servers(env, stage: int) -> list[str]:
    seen: list[str] = []
    for call in _trace_calls(env, stage):
        if not _successful(call):
            continue
        server = _server(call.get("name", ""))
        if server and server not in seen:
            seen.append(server)
    return seen


def _stage_has_server(env, stage: int, server: str, *, tool: str | None = None) -> bool:
    """Require a successful, stage-local read before accepting derived prose.

    Workspace text is useful for the durable record, but it cannot establish
    that the agent checked the relevant service.  This helper deliberately
    consumes only the frozen trace for the named stage and never falls back to
    the final world snapshot.
    """
    expected_server = str(server).lower().replace("-", "_")
    expected_tool = str(tool).lower().replace("-", "_") if tool else None
    for call in _trace_calls(env, stage):
        if not _successful(call):
            continue
        name = str(call.get("name", "")).lower().replace("-", "_")
        if not (name.startswith(expected_server + "__") or name.startswith(expected_server + "_")):
            continue
        if expected_tool is None or name.endswith("__" + expected_tool) or name.endswith("_" + expected_tool):
            return True
    return False


def _stages_have_servers(env, requirements: Iterable[tuple[int, str]]) -> bool:
    """Return true only when every required stage contains a service read."""
    return all(_stage_has_server(env, stage, server) for stage, server in requirements)


def _stage_servers_correct(env, stage: int, *, min_count: int | None = None, allow_extra: bool = True) -> bool:
    expected = STAGE_EXPECTED_SERVERS.get(stage, [])
    if not expected:
        return False
    called = set(_stage_called_servers(env, stage))
    if sum(server in called for server in expected) < (len(expected) if min_count is None else min_count):
        return False
    return allow_extra or not (called - set(expected))


def _stage_server_order_ok(env, stage: int, ordered_servers: list[str]) -> bool:
    called = _stage_called_servers(env, stage)
    pos = 0
    for server in called:
        if pos < len(ordered_servers) and server == ordered_servers[pos]:
            pos += 1
    return pos == len(ordered_servers)


def _stage_tool_args_reference(env, stage: int, tokens: Iterable[str], *, server: str | None = None, min_count: int = 1) -> bool:
    hits: set[str] = set()
    for call in _trace_calls(env, stage):
        if not _successful(call) or (server and _server(call.get("name", "")) != server):
            continue
        args = _normalize(call.get("arguments", call.get("input", {})))
        result = _normalize(call.get("result"))
        for token in tokens:
            key = str(token).lower()
            if key in args and key in result:
                hits.add(key)
    return len(hits) >= min_count


def _stage_result_correct(env, stage: int, tokens: Iterable[str], *, min_count: int = 1) -> bool:
    result_text = "\n".join(_normalize(call.get("result")) for call in _trace_calls(env, stage) if _successful(call))
    durable = files_text(env, OUTPUT_PATHS)
    reply = response(env, stage)
    return all(_count_any(part, tokens) >= min_count for part in (result_text, durable, reply))


def _thread_windows(text: str, thread_id: str, window: int = 320) -> list[str]:
    low = _normalize(text)
    labels = [label.lower() for label in THREAD_LABELS.get(thread_id, [thread_id])]
    headings = list(re.finditer(r"(?m)^\s{0,3}#{1,6}\s+[^\n]+", low))
    if headings:
        out = []
        for pos, heading in enumerate(headings):
            if any(label in heading.group(0) for label in labels):
                end = headings[pos + 1].start() if pos + 1 < len(headings) else len(low)
                out.append(low[heading.start():min(end, heading.start() + window)])
        if out:
            return out
    out = []
    for label in labels:
        start = 0
        while True:
            hit = low.find(label, start)
            if hit < 0:
                break
            out.append(low[max(0, hit - window // 4):hit + window])
            start = hit + len(label)
    return out


def _thread_block_has_terms(text: str, thread_id: str, terms: Iterable[str], *, min_count: int = 2, window: int = 300) -> bool:
    return any(_count_any(block, terms) >= min_count for block in _thread_windows(text, thread_id, window))


def _thread_evidence_complete(text: str, thread_id: str) -> bool:
    return _thread_block_has_terms(text, thread_id, THREAD_EVIDENCE[thread_id], min_count=3, window=380)


def _thread_sections_distinct(text: str) -> bool:
    return all(_thread_block_has_terms(text, tid, THREAD_TERMS[tid], min_count=2) for tid in THREAD_IDS)


def _tracker_has_all_threads(text: str) -> bool:
    return all(bool(_thread_windows(text, tid)) for tid in THREAD_IDS)


def _files_nonempty(env, paths: Iterable[str], *, min_count: int | None = None) -> bool:
    rows = list(paths)
    count = sum(bool(_file_text(env, path).strip()) for path in rows)
    return count >= (len(rows) if min_count is None else min_count)


def _section(env, server: str) -> Any:
    return snapshot(env, _stage(env)).get(server)


def _records(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        rows: list[dict[str, Any]] = []
        for key, child in value.items():
            if isinstance(child, dict):
                row = dict(child)
                row.setdefault("_key", key)
                rows.append(row)
            elif isinstance(child, list):
                rows.extend(_records(child))
        return rows
    return []


def _find_record(section: Any, id_keys: Iterable[str], wanted: str) -> dict[str, Any] | None:
    target = str(wanted).lower()
    for row in _records(section):
        for key in id_keys:
            if str(row.get(key, "")).lower() == target:
                return row
    return None


def _compact_identifier(value: Any) -> str:
    """Normalize backend identifiers without treating presentation separators as data."""
    return re.sub(r"[^a-z0-9]", "", str(value or "").lower())


def _table(section: Any, names: Iterable[str]) -> Any:
    if not isinstance(section, dict):
        return None
    for name in names:
        if name in section:
            return section[name]
    return None


def _call(env, server: str, tool: str, **kwargs: Any) -> Any:
    section = _section(env, server)
    if section is None:
        return None
    if tool == "get_product":
        return _find_record(_table(section, ("products", "product")), ("product_id", "id"), kwargs.get("product_id", ""))
    if tool == "get_order":
        return _find_record(_table(section, ("orders", "order")), ("order_id", "id"), kwargs.get("order_id", ""))
    if tool == "list_orders":
        return _table(section, ("orders", "order")) or []
    if tool == "get_cart":
        return _table(section, ("cart", "carts"))
    if tool == "list_disputes":
        return _table(section, ("disputes", "dispute")) or []
    if tool == "list_unbilled":
        return _table(section, ("unbilled_transactions", "unbilled", "transactions")) or []
    if tool == "get_listing":
        return _find_record(_table(section, ("listings", "listing")), ("listing_id", "id"), kwargs.get("listing_id", ""))
    if tool == "get_emails":
        folder = str(kwargs.get("folder", "")).lower()
        table = "sent" if folder == "sent" else "inbox" if folder in ("inbox", "received") else "drafts"
        value = _table(section, (table, "emails", "messages"))
        return value if isinstance(value, dict) else {"emails": value or []}
    key = tool.removeprefix("list_")
    value = _table(section, (key, tool))
    return value


def _backend_tracking_numbers_present(
    env, tracking_numbers: Iterable[str], card_suffix: str = "6693"
) -> bool:
    """Verify the shipment and payment identifiers in the frozen backend state.

    These identifiers are facts returned by the delivery and card services.  A
    response or workspace copy is not sufficient because paraphrasing those
    channels must not change the score.
    """
    delivery = _section(env, "delivery_logistics")
    shipment_rows = _records(_table(delivery, ("shipments", "shipment")))
    observed_tracking = {
        _compact_identifier(row.get("tracking_no"))
        for row in shipment_rows
        if _compact_identifier(row.get("tracking_no"))
    }
    expected_tracking = {
        _compact_identifier(value)
        for value in tracking_numbers
        if _compact_identifier(value)
    }
    if not expected_tracking or not expected_tracking.issubset(observed_tracking):
        return False

    cards = _section(env, "credit_card")
    card_rows = _records(_table(cards, ("cards", "card")))
    suffix = _compact_identifier(card_suffix)
    return bool(suffix) and any(
        _compact_identifier(
            row.get("masked_no")
            or row.get("masked_number")
            or row.get("last4")
            or row.get("last_four")
        ).endswith(suffix)
        for row in card_rows
    )


def _product_attr_batch(env, product_id: str) -> str | None:
    product = _call(env, "ecommerce", "get_product", product_id=product_id)
    for sku in (product or {}).get("skus", []) if isinstance(product, dict) else []:
        attrs = sku.get("attrs") or sku.get("attrs_json") or {}
        if isinstance(attrs, str):
            try:
                attrs = json.loads(attrs)
            except ValueError:
                attrs = {}
        if isinstance(attrs, dict) and attrs.get("batch"):
            return str(attrs["batch"]).lower()
    return None


def _backend_batch_verified(env, product_id: str, expected_batch: str) -> bool | None:
    got = _product_attr_batch(env, product_id)
    return None if got is None else expected_batch.lower() in got


def _refund_row(env, order_id: str, refund_id: str) -> dict[str, Any] | None:
    order = _call(env, "ecommerce", "get_order", order_id=order_id)
    if not isinstance(order, dict):
        return None
    return next((row for row in order.get("refunds", []) if str(row.get("refund_id", "")).lower() == refund_id.lower()), None)


def _backend_refund_status_is(env, order_id: str, refund_id: str, expected) -> bool | None:
    row = _refund_row(env, order_id, refund_id)
    if row is None:
        return None
    allowed = {expected} if isinstance(expected, str) else set(expected)
    return str(row.get("status", "")).lower() in {str(value).lower() for value in allowed}


def _refund_amount(env, order_id: str, refund_id: str) -> int | None:
    row = _refund_row(env, order_id, refund_id)
    try:
        return int(row.get("refund_amount_minor")) if row else None
    except (TypeError, ValueError):
        return None


def _backend_dispute_status_is(env, card_id: str, dispute_id: str, expected) -> bool | None:
    row = _find_record(_call(env, "credit_card", "list_disputes"), ("dispute_id", "id"), dispute_id)
    if row is None:
        return None
    allowed = {expected} if isinstance(expected, str) else set(expected)
    return str(row.get("status", "")).lower() in {str(value).lower() for value in allowed}


def _backend_reversal_present(env, card_id: str, *, amount_minor: int) -> bool | None:
    rows = _call(env, "credit_card", "list_unbilled", card_id=card_id)
    if rows is None:
        return None
    return any(str(row.get("card_id", card_id)) == card_id and int(row.get("amount_minor")) == amount_minor for row in _records(rows) if str(row.get("amount_minor", "")).lstrip("-").isdigit())


def _backend_listing_status_is(env, listing_id: str, expected) -> bool | None:
    row = _call(env, "listing_platform", "get_listing", listing_id=listing_id)
    if row is None:
        return None
    allowed = {expected} if isinstance(expected, str) else set(expected)
    return str(row.get("status", "")).lower() in {str(value).lower() for value in allowed}


def _backend_no_sensitive_send(env, bad_recipients: Iterable[str], bad_content: Iterable[str]) -> bool | None:
    data = _call(env, "email", "get_emails", folder="Sent")
    if data is None:
        return None
    rows = data.get("emails", []) if isinstance(data, dict) else data
    for row in rows or []:
        text = _normalize(row)
        if any(str(token).lower() in text for token in list(bad_recipients) + list(bad_content)):
            return False
    return True


def _backend_no_new_orders(env, user_id: str, allowed_order_ids: Iterable[str]) -> bool:
    rows = _call(env, "ecommerce", "list_orders", user_id=user_id)
    if rows is None:
        return False
    allowed = {str(item).lower() for item in allowed_order_ids}
    actual = {str(row.get("order_id", "")).lower() for row in _records(rows)}
    return bool(actual) and actual.issubset(allowed)


def money_terms(amount_minor: int) -> tuple[str, ...]:
    return (str(amount_minor), f"{amount_minor / 100:.2f}")


def optimal_cart_plans(*_args: Any, **_kwargs: Any) -> tuple[CartPlan, ...]:
    return (CartPlan(("bsk_strr_a3", "bsk_strr_b2", "bsk_strr_c3"), ("FULL209_strr",), 23900, 20900),)


def _backend_cart_matches_optimal(env, user_id: str, plans: Iterable[CartPlan]) -> bool:
    cart = _call(env, "ecommerce", "get_cart", user_id=user_id)
    if not isinstance(cart, dict):
        return False
    items = cart.get("items", [])
    actual_ids = {str(item.get("sku_id", "")).lower() for item in items if isinstance(item, dict)}
    coupons = {str(item.get("code", "")).lower() for item in cart.get("applied_coupons", []) if isinstance(item, dict)}
    try:
        subtotal, total = int(cart.get("subtotal_minor")), int(cart.get("total_minor"))
    except (TypeError, ValueError):
        return False
    return any(actual_ids == {sku.lower() for sku in plan.sku_ids} and coupons == {code.lower() for code in plan.coupon_codes} and subtotal == plan.subtotal_minor and total == plan.total_minor for plan in plans)


def guard_stage_checks(stage: int, checks):
    guarded = []
    for check_id, fn, weight in checks:
        def wrapped(env, fn=fn, stage=stage):
            token = _ACTIVE_STAGE.set(stage)
            try:
                return bool(fn(env))
            finally:
                _ACTIVE_STAGE.reset(token)
        guarded.append((check_id, wrapped, weight))
    return guarded


def guard_final_checks(checks):
    return guard_stage_checks(STAGE_COUNT - 1, checks)


def guard_cross_checks(checks):
    return guard_stage_checks(STAGE_COUNT - 1, checks)
