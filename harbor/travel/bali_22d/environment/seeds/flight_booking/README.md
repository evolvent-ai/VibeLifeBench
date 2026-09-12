# bali_22d_jun

Flight inventory snapshot for the Bali 22-day (Jun-Jul 2026) benchmark task.

## What this env represents

- **Scenario**: Round-trip flight inventory between Shanghai and Bali
  covering Chen Yu's 22-day Bali trip (depart 2026-06-10, return 2026-07-01)
  plus mother Liu Fang joining 2026-06-22.
- **Reference date**: 2026-05-28 (day 0). Date-keyed rows are baked
  into `init.sql`; the server has no runtime clock.
- **Currency**: CNY throughout (`flights.currency = 'CNY'`).

## Key entities seeded

- **flights**: ~225 rows. 9 unique flight numbers x 25 daily departures
  covering both directions across PVG and DPS over the trip window.
  Carriers include GA (Garuda), MU (China Eastern), CZ (China Southern),
  SQ (Singapore Airlines), QZ (AirAsia Indonesia).
- **fare_buckets**: ~675 rows (3 cabins x flights).
  Cabins: ECONOMY, PREMIUM_ECONOMY, BUSINESS.
- **flight_status**: ~225 rows (one per flight-date) all in `SCHEDULED`
  with `delay_min=0`, ready for `event.yaml` mutations.

No bookings, offers, seat_assignments, or notifications are seeded --
agent drives those flows.

## Key flight numbers

| Flight | Route | Depart | Arrive | Equipment | Notes |
|--------|-------|--------|--------|-----------|-------|
| GA835 | PVG->DPS | 05:55+08 | 12:15+08 | A330 (mutated to B738) | Main outbound |
| GA836 | DPS->PVG | 14:05+08 | 20:25+08 | A330 | Main return |
| GA837 | PVG->DPS | 23:55+08 | 06:15+08 | A330 | Mother's segment option |
| MU5029 | PVG->DPS | 08:00+08 | 14:20+08 | 789 | Alternative |
| MU5030 | DPS->PVG | 15:30+08 | 21:50+08 | 789 | Alternative return |

## How to load

```bash
flight-booking-mock \
  --env ../../envs/flight_booking/bali_22d_jun \
  --host 0.0.0.0 --port 8000
```
