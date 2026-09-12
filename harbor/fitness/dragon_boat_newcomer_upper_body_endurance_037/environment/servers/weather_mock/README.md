# weather-mock

Local FastMCP mock of a weather service (OpenWeather / AccuWeather / JMA
analog). Streamable-HTTP transport, SQLite state under the env directory,
no external traffic.

See [SPEC.md](./SPEC.md) for the schema and tool surface.

## Install

```bash
uv sync
```

Python ≥ 3.12.

## Run

```bash
uv run weather-mock \
    --env ../../envs/weather/japan_20d_may \
    --host 0.0.0.0 --port 8000
```

The server listens at `http://<host>:<port>/mcp` (streamable-HTTP).

### CLI flags

| flag       | default     | meaning                                                          |
| ---------- | ----------- | ---------------------------------------------------------------- |
| `--env`    | (required)  | Path to an env directory. The dir's `init.sql` is loaded on boot. |
| `--host`   | `0.0.0.0`   | HTTP bind host                                                   |
| `--port`   | recommended `8000` for Docker/Terrarium parity | HTTP bind port             |
| `--debug`  | `False`     | Enable debug logging                                             |

On cold start the server deletes `<env>/runtime.db` (and sidecars),
recreates the schema, executes `<env>/init.sql` if present, then opens
streamable-HTTP. Every boot is a fresh DB. Weather rows (`daily_weather`,
`hourly_weather`, `alerts`, `typhoon_tracks`, `daily_aqi`) are read
literally from the table — the server does not generate or drift values.

"Now" for `get_current_weather`, `get_forecast_daily`, and `get_aqi` is
the real wall-clock time in the location's local timezone; missing rows
yield empty lists (forecasts) or `WeatherNotFound` errors (current).
Task authors must seed the env's init.sql so its date range covers the
test horizon.

## Empty env

`envs/weather/empty/init.sql` is an empty file; the smallest env that
boots the server with no data.

## Smoke test

```bash
uv run python scripts/smoke_http.py
```

Boots the server pointed at the japan_20d_may env and exercises
`get_forecast_daily`, `get_aqi`, `get_typhoon_track` (unknown id →
error). Prints `SMOKE PASS` on success.

## Agent-facing tools

| tool                  | purpose                                          |
| --------------------- | ------------------------------------------------ |
| `get_current_weather` | current observation (rounded-down hour)          |
| `get_forecast_hourly` | hourly forecast starting next whole hour         |
| `get_forecast_daily`  | daily forecast starting today                    |
| `get_aqi`             | current AQI                                      |
| `get_alerts`          | active alerts overlapping a geo                  |
| `subscribe_alerts`    | open a sink subscription                         |
| `get_typhoon_track`   | best-track for a storm id                        |

## Layout

```
src/weather_mock/
  server.py     # FastMCP wiring, streamable-HTTP transport
  tools/        # register_*_tools entry points
  services/     # business logic (read-through only)
  models/       # dataclasses
  backends/     # SQLite repo + notification sink
  utils/        # geo_resolver, time, units, exceptions
```
