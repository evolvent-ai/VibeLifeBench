# `weather/dragon_boat_newcomer_upper_body_endurance_037`

## Source description

This task-local `weather` environment belongs to `fitness/dragon_boat_newcomer_upper_body_endurance_037` (Dragon Boat Newcomer Upper-Body Endurance Preparation). It stores synthetic location weather, forecasts, alerts, and observations for the scenario. The scenario runs from `2026-07-06` through `2026-08-17` in `Asia/Shanghai`.

## English Summary

This is the task-local `weather` environment for `fitness/dragon_boat_newcomer_upper_body_endurance_037` (Dragon Boat Newcomer Upper-Body Endurance Preparation). It contains the offline synthetic business state available at scenario start. The environment name is `dragon_boat_newcomer_upper_body_endurance_037`, the scenario window is `2026-07-06` through `2026-08-17`, and the timezone is `Asia/Shanghai`.

## Associated Task

- **Task / task:** `fitness/dragon_boat_newcomer_upper_body_endurance_037`
- **zhong wen biao ti / Chinese title:** Dragon-Boat Newcomer Upper-Body Endurance Preparation
- **English title / English title:** Dragon Boat Newcomer Upper-Body Endurance Preparation
- **Service / service:** `weather`
- **Environment / environment name:** `dragon_boat_newcomer_upper_body_endurance_037`
- **Scenario window / scenario window:** `2026-07-06` → `2026-08-17`
- **Timezone / timezone:** `Asia/Shanghai`

## Scenario Role

Stores location weather, forecasts, alerts, and observations.

Stores location weather, forecasts, alerts, and observations.

## initial data / Seed Contents

The initial file is `init.sql`. The counts below come from loading the service SQLite schema and this file into a fresh in-memory database; empty tables are included to make the initial-state boundary explicit.

Initial files: `init.sql`. The row counts below come from a fresh in-memory load of the corresponding service SQLite schema plus `init.sql`; empty tables are included to make the initial-state boundary explicit.

| business table / Table | initial rows / Initial Rows |
|---|---:|
| `_counters` | 1 |
| `_sim_clock` | 0 |
| `alert_subscriptions` | 0 |
| `alerts` | 0 |
| `climate_profiles` | 1 |
| `daily_aqi` | 15 |
| `daily_weather` | 15 |
| `hourly_weather` | 210 |
| `locations` | 1 |
| `notifications` | 0 |
| `typhoon_tracks` | 0 |

## key entities / Key Entities

The following larger tables and primary-key fields are part of the initial snapshot. They are ordinary scenario entities and do not imply a predetermined outcome.

The following are the larger business tables in the initial snapshot and their primary-key fields. They are ordinary scenario entities and do not imply a predetermined outcome.

| business table / Table | initial rows / Initial Rows | primary-key field / Primary Key |
|---|---:|---|
| `hourly_weather` | 210 | `geo_key`, `datetime` |
| `daily_aqi` | 15 | `geo_key`, `date` |
| `daily_weather` | 15 | `geo_key`, `date` |
| `climate_profiles` | 1 | `profile_id` |
| `locations` | 1 | `geo_key` |

## initial state and dynamic changes / Initial State and Mutations

The `init.*` files describe only the state before timeline events are applied. Later changes must follow the Stage and timestamp order in `event.yaml`; they are not hidden in the initial seed.

The `init.*` files describe only the state before timeline events are applied. Later state changes must be applied in the Stage and timestamp order defined by `event.yaml`; they are not part of the initial seed.

Two events in `event.yaml` update this service:

| Stage | Time | Kind | Update method |
|---:|---|---|---|
| 9 | `2026-07-18T07:30:00+08:00` | `mutation` | SQL file `s09_weather_thunderstorm.sql` |
| 25 | `2026-08-15T08:00:00+08:00` | `mutation` | SQL file `s25_weather_race_heat.sql` |

## file information / Files

| File / file | Purpose / purpose | Size / size |
|---|---|---:|
| `init.sql` | SQLite initial seed | 176156 bytes |

## loading / Loading

At runtime, bind `weather` to environment `dragon_boat_newcomer_upper_body_endurance_037` and read `envs/weather/dragon_boat_newcomer_upper_body_endurance_037/` from the task directory. The external service implementation supplied `DDL`; after loading `init.sql`, SQLite `integrity_check` was `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files exist, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

A compatible runtime should bind `weather` to environment `dragon_boat_newcomer_upper_body_endurance_037` and read `envs/weather/dragon_boat_newcomer_upper_body_endurance_037/` from the task directory. For this data audit, the external service implementation supplied `DDL`, after which `init.sql` was loaded; SQLite `integrity_check` returned `ok` and the foreign-key check returned zero rows. If `init.json` or JSONL files are present, retain and load them according to the service data contract. This task-only release does not include service implementations or the execution framework.

## data and privacy statement / Data and Privacy

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.

All people, organizations, accounts, orders, messages, places, prices, policy summaries, and business records in this environment are offline synthetic data. The files contain no real personal data and require no internet access.
