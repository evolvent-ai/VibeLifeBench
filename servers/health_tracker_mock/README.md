# health-tracker-mock

A FastMCP-based, fully-offline mock of a personal health-tracking backend
(think Apple Health / a smart scale / a fitness app) — logging and querying
weight, steps, heart rate, sleep, blood pressure, body fat, workouts, goals,
and nutrition. Runs over **streamable-HTTP** (no stdio) with a local SQLite
database.

> **Safety:** every tool only *records or queries* personal health data. The
> server never produces a medical diagnosis, severity grade, or any
> medication / treatment advice. `list_health_alerts` may flag readings that
> fall outside a typical reference range, but only descriptively. See
> [SPEC.md](./SPEC.md) §Safety.

## Tools (agent-facing)

Metrics
- `log_metric(user_id, type, value, recorded_at, unit?, value_text?)` — type ∈ {weight, steps, heart_rate, sleep_minutes, blood_pressure, body_fat}.
- `get_metrics(user_id, type, since?, until?, limit?)` — newest first.
- `get_latest_metric(user_id, type)`
- `get_metric_summary(user_id, type, period)` — period ∈ {week, month}; min/max/avg/first/last/delta/trend.

Workouts
- `log_workout(user_id, type, duration_min, started_at, calories?, distance_m?)`
- `list_workouts(user_id, since?, until?, limit?)`
- `get_workout(workout_id)`
- `get_activity_summary(user_id, date)` — steps + workouts for one day.

Goals
- `set_goal(user_id, type, target, period, unit?, direction?, start_date?)` — period ∈ {day, week, month, once}; direction ∈ {at_least, at_most}.
- `get_goals(user_id, status?)`
- `get_goal_progress(user_id, goal_id)` — current vs target, percent, on_track (numbers only).

Nutrition
- `log_nutrition(user_id, meal, calories, logged_at, description?, protein_g?, carbs_g?, fat_g?)` — meal ∈ {breakfast, lunch, dinner, snack}.
- `get_nutrition_summary(user_id, date)`

Alerts
- `list_health_alerts(user_id, limit?)` — descriptive out-of-typical-range flags; never a diagnosis.

The server has no simulated clock and no management CLI. Stage-driven state
changes are applied as SQL mutations by the task orchestrator.

## Units

weight = grams, steps = count, heart_rate = bpm, sleep_minutes = minutes,
blood_pressure: numeric `value` = systolic mmHg with `value_text` = `"sys/dia"`,
body_fat = percent. Pass `unit` to `log_metric` to override the default.

## Quick start

```bash
# From this directory
pip install -e .

# Run with an env directory.
health-tracker-mock \
  --port 8020 \
  --env ../../envs/health_tracker/li_wei_fitness_2026
```

On startup the server unlinks any `<env>/runtime.db`, creates the schema,
executes `<env>/init.sql` if present, and binds streamable-HTTP at
`http://<host>:<port>/mcp`.

## CLI flags

- `--env PATH` — required; path to an `envs/<server>/<env_name>/` directory.
- `--host` (default `0.0.0.0`)
- `--port` (default `8020`; pass `8000` for Docker/Terrarium parity)
- `--debug` — verbose logging.

## Smoke test

```bash
python3 scripts/smoke_http.py
```

Spins up the server in a subprocess against
`envs/health_tracker/li_wei_fitness_2026` and round-trips `get_latest_metric`,
`get_metric_summary`, `log_metric`, `list_workouts`, `get_goal_progress`, and
`list_health_alerts`, plus an unknown-type call expecting `BAD_TYPE`. Prints
`PASS` or `FAIL`.

## Errors

Every tool returns valid JSON. Errors come back as
`{"error": "<msg>", "code": "<CODE>"}` — never as exceptions. Stable codes:

`BAD_TYPE`, `BAD_PERIOD`, `BAD_DATE`, `BAD_VALUE`, `METRIC_NOT_FOUND`,
`WORKOUT_NOT_FOUND`, `GOAL_NOT_FOUND`, `BAD_ARG`.
