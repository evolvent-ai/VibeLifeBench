# weather-mock — SPEC

Local mock of a weather/AQI/typhoon service. All state lives in a single
SQLite file under the env directory; the server has no notion of "today"
beyond the host wall-clock in each location's local timezone.

## 1. Boot contract

```bash
weather-mock --host 0.0.0.0 --port 8000 --env <abs path to env dir>
```

On cold start: delete `<env>/runtime.db` (and sidecars), recreate schema,
execute `<env>/init.sql` if present, open streamable-HTTP on `/mcp`.

## 2. Agent-facing tools

| tool                  | summary                                          |
| --------------------- | ------------------------------------------------ |
| `get_current_weather` | current observation (rounded-down hour)          |
| `get_forecast_hourly` | hourly forecast starting next whole hour         |
| `get_forecast_daily`  | daily forecast starting today                    |
| `get_aqi`             | current AQI                                      |
| `get_alerts`          | active alerts overlapping a geo                  |
| `subscribe_alerts`    | open a sink subscription                         |
| `get_typhoon_track`   | best-track for a storm id                        |

There are no admin tools. There is no clock-advancement surface.
Stage-to-stage world changes come from orchestrator-applied mutations
against `runtime.db`.

## 3. Determinism

* No `random.Random`.
* No forecast generator: weather rows are pre-baked in `init.sql`. The
  server is a literal read-through.
* AQI: `daily_aqi` row for (geo_key, today) > climate-profile baseline
  fallback.

## 4. Schema

```sql
climate_profiles(profile_id PK, seasonal_temp_means_json,
                 precip_freq_json, wind_baseline_kmh,
                 humidity_baseline_pct, aqi_baseline_json, notes);
locations(geo_key PK, city, country, lat, lng, timezone,
          climate_profile_id, kind);
daily_weather(geo_key, date, tmin, tmax, condition, precip_mm,
              precip_prob, wind_kmh, PK (geo_key, date));
hourly_weather(geo_key, datetime, temp_c, humidity, condition,
               precip_mm, wind_kmh, PK (geo_key, datetime));
alerts(alert_id PK, kind, severity, start_dt, end_dt, areas_json,
       description, active, created_at, source_event);
alert_subscriptions(sub_id PK, geo_key, sink, created_at, active);
notifications(id PK autoinc, created_at, channel, sub_id, alert_id,
              payload_json, delivered);
typhoon_tracks(storm_id, dt, lat, lng, intensity,
               PK (storm_id, dt));
daily_aqi(geo_key, date, aqi, category, dominant_pollutant,
          observed_at, PK (geo_key, date));
_counters(name PK, value);
```

The `active` column on `alerts` is honored as a literal boolean — task
authors flip it via stage `mutation` events when an alert should fire or
expire.

## 5. Error codes (subset)

| code                   | thrown when                                         |
| ---------------------- | --------------------------------------------------- |
| `no_nearby_location`   | geo string / lat-lng doesn't resolve                |
| `observation missing`  | `get_current` finds no hourly row for current hour  |
| `unknown_storm`        | `get_typhoon_track` called with unseeded storm_id   |
| `invalid_geo`          | geo dict missing lat/lng                            |
| `sink_outside_workspace` | file:// sink path escapes the workspace            |
