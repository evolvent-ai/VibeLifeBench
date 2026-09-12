# bali_22d_jun

Hotel inventory + rate-plan snapshot for the Bali 22-day (Jun-Jul 2026)
benchmark task.

## What this env represents

- **Scenario**: 20 Bali properties (Seminyak, Kuta, Ubud, Nusa Dua,
  Sanur, Kintamani) for Chen Yu's 22-day Bali trip 2026-06-10 to 2026-07-01.
- **Reference date**: 2026-05-28 (day 0). Rate plans cover the full
  booking window plus buffer.
- **Currency**: IDR (`rate_plans.currency = 'IDR'`).
- **Exchange rate**: 1 CNY = 2,200 IDR (task-defined).

## Key entities seeded

- **hotels**: 20 rows. Properties across 6 Bali districts.
- **rate_plans**: ~5,400 rows -- one row per (hotel, date, room_type, flavor)
  across the trip window. Three flavors: flex, semi, prepaid.

No reservations or special_requests are pre-seeded -- agent drives those.

## Key hotels referenced by task

| hotel_id | Name | District | Stars | Task relevance |
|----------|------|----------|-------|---------------|
| htl_bal_seminyak_01 | Alila Seminyak | Seminyak | 4 | Mold issue stage 14 |
| htl_bal_seminyak_02 | W Bali Seminyak | Seminyak | 5 | Relocation option |
| htl_bal_ubud_01 | Alila Ubud | Ubud | 5 | Mid-trip base |
| htl_bal_kintamani_01 | Lakeview Hotel | Kintamani | 3 | Volcano proximity |

## Important amenities

- All hotels have AC (critical for pregnancy comfort + RA management)
- Most have minifridge (medication storage)
- Ground-floor / elevator access noted for mother's mobility

## How to load

```bash
hotel-booking-mock \
  --env ../../envs/hotel_booking/bali_22d_jun \
  --host 0.0.0.0 --port 8000
```
