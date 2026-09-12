# japan_20d_may

Maps / places / transit snapshot for the Japan 20-day (May 2026)
benchmark task.

## What this env represents

- **Scenario**: POIs, transit network, and scripted road / transit
  incidents across Tokyo, Kyoto, Osaka, Hakone, Nara (+ Shanghai
  origin) for Li Wei's 20-day Japan trip 2026-04-28 to 2026-05-22.
- **Reference date**: 2026-04-17 (day 0). Date windows are baked into
  `init.sql`; the server has no runtime clock.

## Key entities seeded

- **places**: 90 POIs — temples, shrines, parks, museums, attractions,
  stations, shopping streets, restaurants (including pharmacy /
  medical POIs needed by stage-17 Kyoto "nearest clinic" flow).
  Covers ~60 Tokyo / Kyoto / Osaka / Hakone / Nara entries plus a few
  Shanghai origin places.
- **transit_lines**: 19 lines covering JR Yamanote, Tokyo Metro
  Ginza / Marunouchi / Hibiya, JR Tokaido / Sanyo Shinkansen, Hankyu,
  Hakone Tozan railway, Kyoto subway, Osaka Loop, etc.
- **transit_stops**: 145 stops across the seeded lines, with geo
  coordinates and parent-station hierarchy.
- **transit_schedule**: 7,480 rows — typical-weekday HH:MM departures
  per line / direction.
- **roads**: 11 named roads — major highways and avenues used for
  scripted road events (e.g. Hakone Turnpike, Gion Matsuri closure
  street, Tomei Expressway alias).
- **road_events / transit_events**: 3 + 3 inactive rows. `active=0` on
  insert; explicit `event.yaml` mutations flip them when scripted stages
  open (e.g. Gion Matsuri closure on day 15, Kyoto Station incident on
  day 15).

No user-driven directions / geocoding history is seeded — agent drives
those.

## How to load

```bash
# direct, from servers/maps_mock/
maps-mock \
  --env ../../envs/maps/japan_20d_may \
  --host 0.0.0.0 --port 8000
```

```bash
# docker, from repo root after building vibe-agent-benchmark/maps_mock:latest
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/maps/japan_20d_may:/env-seed:ro" \
  vibe-agent-benchmark/maps_mock:latest
```

The Docker entrypoint copies `/env-seed` to `/env`; the server creates
`/env/runtime.db` and applies `/env/init.sql` on cold start.
