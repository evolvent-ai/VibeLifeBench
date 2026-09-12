# bali_22d_jun

Maps / places / transit snapshot for the Bali 22-day (Jun-Jul 2026)
benchmark task.

## What this env represents

- **Scenario**: POIs, roads, and scripted road events across Bali
  (Seminyak, Ubud, Kintamani, Nusa Dua, Sanur, Uluwatu) + Shanghai
  origin for Chen Yu's 22-day trip.
- **Reference date**: 2026-05-28 (day 0).
- **Note**: Bali has no rail system. All transit is by car/taxi (Grab/Gojek).

## Key entities seeded

- **places**: ~60 POIs -- temples, beaches, rice terraces, hospitals,
  restaurants, markets, airports. Includes critical medical POIs
  (BIMC Kuta, Siloam Bali) needed for pregnancy emergency flow.
- **roads**: ~10 key routes with distance and typical duration.
- **road_events**: Pre-seeded inactive events:
  - Ubud road flooding Jun 20-22 (activated by storm)
  - Kintamani road closure (activated by volcano Level 3)

## Key places referenced by task

| place_id | Name | Task relevance |
|----------|------|---------------|
| pl_bimc_kuta | BIMC Hospital Kuta | Pregnancy emergency (stage 20) |
| pl_siloam_bali | Siloam Hospitals Bali | Alternative hospital |
| pl_tegallalang | Tegallalang Rice Terrace | 200+ stairs -- not for mother |
| pl_ceking_terrace | Ceking Rice Terrace | Flat accessible alternative |
| pl_kintamani_view | Kintamani Viewpoint | Closed when volcano Level 3 |
| pl_uluwatu | Uluwatu Temple | Cliff stairs -- not for mother |

## How to load

```bash
maps-mock \
  --env ../../envs/maps/bali_22d_jun \
  --host 0.0.0.0 --port 8000
```
