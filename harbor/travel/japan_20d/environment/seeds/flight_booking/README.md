# japan_20d_may

Flight inventory snapshot for the Japan 20-day (May 2026) benchmark task.

## What this env represents

- **Scenario**: Round-trip flight inventory between Shanghai and Japan
  covering Li Wei's 20-day Japan trip (depart 2026-04-28, return 2026-05-22).
- **Reference date**: 2026-04-17 (day 0). Date-keyed rows are baked
  into `init.sql`; the server has no runtime clock.
- **Currency**: CNY throughout (`flights.currency = 'CNY'`).

## Key entities seeded

- **flights**: 1,349 seed rows plus the MU549 2026-05-01 baseline row
  published in release-000. Together they cover 54 unique flight numbers x
  25 daily departures across PVG/SHA/HGH and NRT/HND/KIX. Carriers include
  MU, CA, CZ, HU, JL, NH, MM, IJ, GK.
- **fare_buckets**: 4,050 rows (3 cabins x flights x dates).
  Cabins: ECONOMY, PREMIUM_ECONOMY, BUSINESS. Seats_remaining is
  cabin-tier-typical (e.g. 90 / 30 / 12 for narrowbody).
- **flight_status**: 1,350 rows (one per flight-date) all in `SCHEDULED`
  with `delay_min=0`, ready for explicit `event.yaml` mutations to inject
  delays / cancellations.

No bookings, offers, seat_assignments, or notifications are seeded —
agent drives those flows.

## How to load

```bash
# direct, from servers/flight_booking_mock/
flight-booking-mock \
  --env ../../envs/flight_booking/japan_20d_may \
  --host 0.0.0.0 --port 8000
```

```bash
# docker, from repo root after building vibe-agent-benchmark/flight_booking_mock:latest
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/flight_booking/japan_20d_may:/env-seed:ro" \
  vibe-agent-benchmark/flight_booking_mock:latest
```

The Docker entrypoint copies `/env-seed` to `/env`; the server creates
`/env/runtime.db` and applies `/env/init.sql` on cold start.
