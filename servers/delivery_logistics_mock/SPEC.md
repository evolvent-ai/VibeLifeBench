# delivery_logistics_mock — Specification

Status: v0.1 (implementer-facing)
Audience: agents and operators integrating with the mock express shipping server.
Scope: this document plus `README.md` is the only behavioural contract.

The mock simulates a Chinese express shipping aggregator (顺丰 / 京东物流 /
中通-style) over **streamable-HTTP only** with a local SQLite backend.
Money is **integer 分** (CNY minor units). All times are ISO 8601; all
dates are `YYYY-MM-DD`. All text is UTF-8; Chinese is preserved (no
`ensure_ascii`).

This server is fully offline. It never contacts any real carrier API.

## 1. Layout

```
delivery_logistics_mock/
├── pyproject.toml
├── README.md
├── SPEC.md                     # this document
├── Dockerfile
├── src/delivery_logistics_mock/
│   ├── __init__.py / __main__.py
│   ├── server.py                # FastMCP streamable-http, takes --env <path>
│   ├── models/                  # dataclasses
│   ├── backends/db.py           # schema (no bundled seed data)
│   ├── services/                # TrackingService, ShipmentService, …
│   ├── tools/                   # one register_* per group
│   └── utils/                   # ids, dates, exceptions
└── scripts/smoke_http.py
```

The package ships schema only. State enters via `<env>/init.sql` which
the server executes against a fresh `<env>/runtime.db` on every cold
start (v3 contract).

## 2. Transport and CLI

- `mcp.run(transport="streamable-http", host, port, path="/mcp")`. There
  is no stdio fallback, no `--transport` flag.
- Server CLI: `--host`, `--port`, `--env <dir>`, `--debug`.
  Pass `--port 8000` for Docker/Terrarium parity.
- No management CLI. Stage-driven mutations are pushed by the orchestrator's
  event-overlay channel against the server's runtime DB directly.

## 3. Data model (SQLite)

### shipments
`shipment_id` PK; `user_id`; `tracking_no` UNIQUE; `carrier`;
`service_level`; `status` ∈ `{label_created, picked_up, in_transit,
out_for_delivery, delivered, exception, returned, cancelled}`;
`sender_json`, `recipient_json` (address objects);
`weight_kg`; `dimensions_json`; `declared_value_minor`; `fee_minor`;
`created_at`; `eta_date`; `scheduled_pickup_at`; `updated_at`;
`cancel_reason`. Indexed on `(user_id)`, `(status)`, `(eta_date)`.

### shipment_events
`event_id` PK; `shipment_id` FK; `at` (ISO ts); `location`; `status_code`;
`description`. Index on `(shipment_id, at)` — events grow fast, this
index is load-bearing.

### pickups
`pickup_id` PK; `shipment_id` FK; `scheduled_at`; `completed_at`; `status`
∈ `{pending, completed, cancelled}`.

### issue_tickets
`ticket_id` PK; `shipment_id` FK; `issue_type` ∈ `{lost, damaged,
wrong_address, missing_item, delivery_failed}`; `description`; `status` ∈
`{open, in_review, resolved, closed}`; `opened_at`;
`expected_response_date`; `resolved_at`.

### status_subscriptions
`subscription_id` PK; `shipment_id` FK; `channel` ∈ `{email, sms,
webhook}`; `target`; `active` (1/0); `created_at`.

### notifications_outbox
`id` PK auto; `subscription_id` FK; `payload_json`; `queued_at`;
`sent_at`. Status transitions and reschedule / cancel / address-change
events all fanout one row per active subscription.

### address_book
`address_id` PK; `user_id`; `label`; `recipient`; `phone`; `province`;
`city`; `district`; `detail`; `postal_code`; `is_default`.

### _counters
Generic atomic counter table (shipment_seq, event_seq, pickup_seq,
ticket_seq, subscription_seq). The leading underscore signals "control
table, not part of the agent-visible domain".

The server does not carry a notion of "today"; date-coupled
validations fall back to the real UTC date. Date-keyed rows (ETAs,
scheduled pickups) are seeded by `init.sql` against literal dates.

## 4. Address shape

All address-valued tool inputs/outputs use the same dict shape:

```json
{
  "recipient": "李伟",
  "phone": "13800000001",
  "province": "上海",
  "city": "上海",
  "district": "徐汇区",
  "detail": "虹桥路1号 园景苑3号楼1801室",
  "postal_code": "200030"
}
```

`recipient`, `phone`, `province`, `city`, `district`, `detail` are
required. `postal_code` is optional. Validation failures raise
`BAD_ADDRESS`.

## 5. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`
strings, and translate `DeliveryMockError` subclasses to
`{"error": msg, "code": CODE}`. The full code list is in §Appendix A.

### track_package(tracking_no)
Returns `{tracking_no, carrier, status, latest_event, origin,
destination, eta_date, events}`. `latest_event` is `None` for label-only
shipments with no scans. `events` is ordered ascending by `at`.

### list_shipments(user_id, status_filter=None, limit=20)
Newest first by `created_at`. Each item is a compact summary; call
`get_shipment` for everything.

### get_shipment(shipment_id)
Full record: carrier, service_level, sender, recipient, weight_kg,
dimensions, declared_value_minor, fee_minor, tracking_no, status, events,
eta_date, subscriptions, cancel_reason.

### estimate_delivery(origin_addr, dest_addr, weight_kg, service_type)
`service_type` ∈ `{standard, express, same_day}`. Returns
`{service_type, weight_kg, origin, destination, offers: [{carrier,
service_level, eta_date, fee_minor}]}` with 2-3 offers. Carrier choice is
deterministic — the same `(service_type, origin, dest, weight)` hash
always produces the same ordered carrier list. No DB writes.

### request_pickup(user_id, pickup_addr, dest_addr, item_desc, weight_kg, service_type, scheduled_at)
Creates a shipment in `label_created` plus its initial scan event plus a
`pickups` row. Picks the first carrier offer that `estimate_delivery`
would return for the same inputs (so an agent's plan stays internally
consistent). Returns `{shipment_id, tracking_no, carrier, service_level,
fee_minor, eta_date, scheduled_pickup_at, confirmation_code}`.
`scheduled_at` accepts `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM[:SS]`; past
dates raise `BAD_DATE`.

### reschedule_delivery(tracking_no, new_date, time_window)
Allowed only when status ∈ `{in_transit, out_for_delivery, exception}`;
otherwise `INVALID_STATUS_FOR_OP`. `new_date` is ISO; must not be in the
past (else `BAD_DATE`). `time_window` ∈ `{morning, afternoon, evening,
anytime}` (else `BAD_ARG`). Inserts a `reschedule` event and fans out a
notification per active subscription.

### change_address(tracking_no, new_address)
Allowed only when status ∈ `{label_created, picked_up}`. If status is
`in_transit` or later → `IN_TRANSIT_LOCKED`. Other invalid statuses →
`INVALID_STATUS_FOR_OP`. Inserts an `address_changed` event and fans out
notifications. Returns the updated shipment record (same shape as
`get_shipment`).

### cancel_shipment(tracking_no, reason)
Allowed only when status ∈ `{label_created, picked_up}`. After that:
`CANCEL_TOO_LATE`. Any pending pickup is also moved to `cancelled`.
Fans out a `cancelled` notification.

### report_issue(tracking_no, issue_type, description)
`issue_type` ∈ `{lost, damaged, wrong_address, missing_item,
delivery_failed}`. Returns `{ticket_id, shipment_id, tracking_no,
issue_type, status: "open", opened_at, expected_response_date}`. SLA
defaults (days): `lost=3`, `damaged=2`, `missing_item=2`,
`wrong_address=1`, `delivery_failed=1`.

### list_issues(user_id, status_filter=None)
All tickets owned by `user_id` (matched via the underlying shipment),
newest first.

### subscribe_status(tracking_no, channel, target)
`channel` ∈ `{email, sms, webhook}`. `target` is the destination
(address / phone / URL). Returns
`{subscription_id, shipment_id, tracking_no, channel, target, active,
created_at}`.

### unsubscribe(subscription_id)
Idempotent. If the subscription doesn't exist → `SUBSCRIPTION_NOT_FOUND`.
If already inactive → returns `already_inactive: true` instead of
erroring.

## 6. Stage progression

There is no in-server clock walk. Shipment status, eta_date, and
shipment_events rows are pre-baked by `init.sql` for the env's reference
date frame. When a task wants a shipment to "progress" between stages,
the task writes a `mutation` event (`event.yaml`) that the orchestrator
applies as raw SQL against the server's `runtime.db`.

## 7. Quality contract

- All tools async; all return `json.dumps(...)` strings.
- Errors are never raised across the MCP boundary; they become
  `{"error": "...", "code": "..."}` JSON.
- No `print()` anywhere; logging only, to stderr.
- No network libraries imported (`requests`, `httpx`, `aiohttp`,
  `urllib3` are absent).
- Server starts cleanly against an empty env (returns empty lists).
- `shipment_events` is indexed on `(shipment_id, at)`.
- No `random.*` anywhere in `src/`.

## Appendix A — error codes

| code                    | meaning |
| ----------------------- | ------- |
| `BAD_ARG`               | malformed required argument (non-string, empty, wrong type, etc.) |
| `BAD_DATE`              | malformed date or date in the past |
| `BAD_ADDRESS`           | address object missing a required field |
| `BAD_SERVICE_TYPE`      | `service_type` not in `{standard, express, same_day}` |
| `SHIPMENT_NOT_FOUND`    | no shipment matches the given `shipment_id` / `tracking_no` |
| `INVALID_STATUS_FOR_OP` | operation not allowed in the current shipment status (generic) |
| `IN_TRANSIT_LOCKED`     | `change_address` attempted after the package left the origin hub |
| `CANCEL_TOO_LATE`       | `cancel_shipment` attempted after `in_transit` |
| `SUBSCRIPTION_NOT_FOUND`| `unsubscribe` called with an unknown subscription id |
