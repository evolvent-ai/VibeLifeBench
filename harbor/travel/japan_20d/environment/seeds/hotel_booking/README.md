# japan_20d_may

Hotel inventory + rate-plan snapshot for the Japan 20-day (May 2026)
benchmark task.

## What this env represents

- **Scenario**: 24 Japanese properties (Tokyo, Hakone, Kyoto, Osaka,
  Nara) for Li Wei's 20-day Japan trip 2026-04-28 to 2026-05-22.
- **Reference date**: 2026-04-17 (day 0). Rate plans cover the full
  booking window plus a buffer; the server has no runtime clock.
- **Currency**: JPY (`rate_plans.currency = 'JPY'`); fares stored in
  minor units (1 yen = 1 minor unit since JPY has no sub-unit).

## Key entities seeded

- **hotels**: 24 rows. 4-star properties in Tokyo (Shiodome / Shinjuku /
  Shibuya / Asakusa / Ginza / Roppongi), Hakone ryokans, Kyoto
  machiya-style properties, Osaka business hotels, Nara mid-range.
- **rate_plans**: 4,104 rows — one row per (hotel, date, room_type)
  across the trip window. Three plan flavors per night:
  - `flex` (~60%) — free cancellation until 7 days prior.
  - `semi` (~30%) — free cancellation until 2 days prior.
  - `rigid` (~10%) — non-refundable.
  Weekend nights and Golden Week dates (2026-05-03..05) carry a price
  premium reflected in `base_price`.
- **pending_events**: historical fixture rows are present, but the current
  Terrarium task uses explicit `event.yaml` mutations for staged changes.

No reservations, reservation_nights, special_requests, or notifications
are pre-seeded — agent drives those flows.

## How to load

```bash
# direct, from servers/hotel_booking_mock/
hotel-booking-mock \
  --env ../../envs/hotel_booking/japan_20d_may \
  --host 0.0.0.0 --port 8000
```

```bash
# docker, from repo root after building vibe-agent-benchmark/hotel_booking_mock:latest
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/hotel_booking/japan_20d_may:/env-seed:ro" \
  vibe-agent-benchmark/hotel_booking_mock:latest
```

The Docker entrypoint copies `/env-seed` to `/env`; the server creates
`/env/runtime.db` and applies `/env/init.sql` on cold start.
