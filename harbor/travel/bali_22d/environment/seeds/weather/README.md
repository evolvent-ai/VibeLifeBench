# bali_22d_jun

Weather / AQI / volcanic alert snapshot for the Bali 22-day (Jun-Jul 2026)
benchmark task.

## What this env represents

- **Scenario**: Five-week June-July 2026 climate window across Bali
  geography (Seminyak, Ubud, Kintamani, Nusa Dua, DPS airport) plus
  Shanghai origin. Forecasts, AQI, alerts, and volcanic monitoring.
- **Reference date**: 2026-05-28 (day 0).
- **Climate**: Bali dry season -- mostly sunny 29-33C, with a monsoon-tail
  storm event June 20-22 (heavy rain in Ubud highlands).

## Key entities seeded

- **locations**: 6 rows -- Bali districts + Shanghai PVG.
- **climate_profiles**: 2 rows -- bali_dry_season, shanghai_summer.
- **daily_weather**: ~210 rows (35 days x 6 locations).
- **alerts**: Pre-seeded inactive storm and volcanic alerts.
- **daily_aqi**: ~210 rows mirroring daily weather grid.
- **volcanic_alerts**: Baseline Level 1 for Agung. Mutations in event.yaml
  escalate to Level 2 (stage 10) and Level 3 (stage 19).

## Key weather events

| Date range | Event | Impact |
|-----------|-------|--------|
| Jun 20-22 | Monsoon-tail storms | Heavy rain Ubud 80-120mm/day, flooding |
| Jun 7+ | Agung seismic increase | Level 2 Waspada |
| Jun 22+ | Agung phreatic eruption | Level 3 Siaga, ash column |
| Jun 29+ | Ash drift toward DPS | Potential airport impact |

## How to load

```bash
weather-mock \
  --env ../../envs/weather/bali_22d_jun \
  --host 0.0.0.0 --port 8000
```
