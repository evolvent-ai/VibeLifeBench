# japan_20d_may

Weather / AQI / typhoon snapshot for the Japan 20-day (May 2026)
benchmark task.

## What this env represents

- **Scenario**: Five-week May 2026 climate window across the Japan trip
  geography (Tokyo / Hakone / Kyoto / Osaka / Nara) plus the Shanghai
  origin city. Forecasts, AQI readings, alerts, and one typhoon track
  cover the trip dates 2026-04-28 to 2026-05-22.
- **Reference date**: 2026-04-17 (day 0). Weather rows are baked into
  `init.sql`; the server has no runtime clock or forecast drift.

## Key entities seeded

- **climate_profiles**: 5 rows — `kanto_may`, `kansai_may`, `hakone_may`,
  `shanghai_may`, `okinawa_may`.
- **locations**: 10 rows — city + airport geo_keys for Tokyo (city /
  HND / NRT), Osaka (city / KIX), Kyoto, Nara, Hakone, Shanghai (city
  / PVG). Each location is tied to a climate profile.
- **daily_weather**: 225 rows — 45 days x 5 representative geos
  (tmin, tmax, condition, precipitation probability, wind).
- **hourly_weather**: 1,080 rows — 24 h x select stage-critical days.
- **alerts**: no baseline alert rows; stage-specific alerts are released by
  the world-controller at their source events.
- **daily_aqi**: 225 rows mirroring the daily weather grid (AQI value,
  category, dominant pollutant).
- **typhoon_tracks**: no baseline track rows; the D10 release publishes only
  observations available by that stage and the service filters by world time.

No alert_subscriptions, notifications, or aqi_overrides are seeded —
agent drives those.

## How to load

```bash
# direct, from servers/weather_mock/
weather-mock \
  --env ../../envs/weather/japan_20d_may \
  --host 0.0.0.0 --port 8000
```

```bash
# docker, from repo root after building vibe-agent-benchmark/weather_mock:latest
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/weather/japan_20d_may:/env-seed:ro" \
  vibe-agent-benchmark/weather_mock:latest
```

The Docker entrypoint copies `/env-seed` to `/env`; the server creates
`/env/runtime.db` and applies `/env/init.sql` on cold start.
