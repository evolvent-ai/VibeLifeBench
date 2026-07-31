# health_tracker_mock — Specification

Status: v1 (implementer-facing)
Scope: implementation spec for the `health-tracker-mock` MCP server.

## 1. Purpose

`health_tracker_mock` is a self-contained, fully-offline mock of a personal
health-tracking backend — body metrics, workouts, goals, and nutrition. It
exists so benchmark tasks can exercise an agent's ability to log readings,
query trends and summaries, track goal progress, and surface descriptive
out-of-range flags, then react to deterministic state changes injected by the
task orchestrator via out-of-band SQL mutations.

The server makes **no** network calls and ships **no** bundled seed data —
state enters only through the env-directory `init.sql` script.

### Safety (binding)

Tools **only record or query** data. They MUST NOT produce a medical
diagnosis, risk/severity grade, or any medication / diet / treatment advice.
`list_health_alerts` flags readings outside a *typical reference range* using
neutral wording (`above_typical_range` / `below_typical_range`) plus the
reference bounds, and explicitly labels output as informational, not a
diagnosis. The reference ranges are descriptive only and never drive a
prescriptive recommendation.

Non-goals:

- No diagnosis, scoring, or advice (see Safety).
- No authentication. Identity is whatever the caller passes as `user_id`.
- No real device sync; all data is caller-supplied.
- No i18n; free-text fields pass through verbatim (`ensure_ascii=False`).

## 2. Stack

- Python ≥ 3.12, stdlib `sqlite3`, `fastmcp ≥ 2.10.5`, `mcp[cli] ≥ 1.11.0`.
- No network libraries in the package.
- Transport: **streamable-HTTP only** at path `/mcp`. No stdio.

## 3. Tools

All tools are `async def`, return `json.dumps(result, ensure_ascii=False)`,
and surface errors as `{"error": "...", "code": "..."}` rather than raising
across the MCP boundary. Dates are ISO `YYYY-MM-DD`; timestamps ISO-8601 with
timezone. IDs are domain-prefixed strings.

Units by metric type: `weight`=grams, `steps`=count, `heart_rate`=bpm,
`sleep_minutes`=minutes, `blood_pressure`= numeric `value` is systolic mmHg
(human form in `value_text` as `"sys/dia"`), `body_fat`=percent.

### 3.1 `log_metric(user_id, type, value, recorded_at, unit?, value_text?) -> str`

`type` ∈ {`weight`,`steps`,`heart_rate`,`sleep_minutes`,`blood_pressure`,`body_fat`}.
`value` numeric; `unit` defaults per type. For composite readings put the
human form in `value_text` (e.g. `"120/80"`) and the orderable number in `value`.

```json
{"metric_id": "met_00000200", "user_id": "usr_li_wei", "type": "weight",
 "value": 75600.0, "value_text": null, "unit": "g",
 "recorded_at": "2026-05-18T07:10:00+08:00"}
```

### 3.2 `get_metrics(user_id, type, since?, until?, limit=100) -> str`

Newest-first list of one metric type. Date window inclusive (`YYYY-MM-DD`).
`limit` default 100, clamped to 1000.

### 3.3 `get_latest_metric(user_id, type) -> str`

The single most recent reading. `METRIC_NOT_FOUND` if none exist.

### 3.4 `get_metric_summary(user_id, type, period) -> str`

`period` ∈ {`week` (7d), `month` (30d)}. Window ends at the user's latest
reading for that type (the server has no clock).

```json
{"user_id": "usr_li_wei", "type": "weight", "period": "week",
 "window_start": "2026-05-11", "window_end": "2026-05-17", "unit": "g",
 "count": 7, "min": 75450.0, "max": 76010.0, "avg": 75740.0,
 "first": 76010.0, "last": 75710.0, "delta": -300.0, "trend": "down"}
```

`trend` ∈ {`up`,`down`,`flat`} from `last - first`. If no readings exist,
`count` is 0 and the stats are `null`.

### 3.5 `log_workout(user_id, type, duration_min, started_at, calories?, distance_m?) -> str`

`type` free-form (`run`,`gym`,`cycling`,`swim`,`yoga`,…). `duration_min`
positive int. `calories` kcal, `distance_m` meters (both optional, ≥ 0).

```json
{"workout_id": "wkt_000025", "user_id": "usr_li_wei", "type": "run",
 "duration_min": 35, "calories": 360, "distance_m": 6000,
 "started_at": "2026-05-18T07:40:00+08:00"}
```

### 3.6 `list_workouts(user_id, since?, until?, limit=100) -> str`

Newest-first. Date window inclusive. `limit` default 100, clamped to 500.

### 3.7 `get_workout(workout_id) -> str`

One workout by id. `WORKOUT_NOT_FOUND` if unknown.

### 3.8 `get_activity_summary(user_id, date) -> str`

One calendar day. `steps` = latest steps reading that day; plus
`workout_count`, `active_minutes`, `workout_calories`, `distance_m`, and the
day's `workouts` list.

```json
{"user_id": "usr_li_wei", "date": "2026-05-16", "steps": 11560,
 "workout_count": 1, "active_minutes": 58, "workout_calories": 620,
 "distance_m": 9600, "workouts": [ ... ]}
```

### 3.9 `set_goal(user_id, type, target, period, unit?, direction?, start_date?) -> str`

`period` ∈ {`day`,`week`,`month`,`once`}. `direction` ∈ {`at_least` (more is
better), `at_most` (less is better)}; default `at_least`. Returns the goal
with `status: "active"`.

### 3.10 `get_goals(user_id, status?) -> str`

`status` ∈ {`active`,`achieved`,`abandoned`}.

### 3.11 `get_goal_progress(user_id, goal_id) -> str`

Descriptive progress over the goal's current period window (window end = the
user's latest data point). Measurement strategy by goal `type`:

- contains `distance` / `run` → sum of workout `distance_m` in window.
- `steps` → sum of daily-latest steps readings in window.
- `weight`/`body_fat`/`heart_rate`/`blood_pressure`/`sleep_minutes` → latest reading ≤ window end.
- otherwise → workout count in window.

```json
{"goal_id": "goal_seed_000002", "user_id": "usr_li_wei", "type": "run_distance",
 "direction": "at_least", "period": "week", "target": 18000.0, "unit": "m",
 "current": 14600.0, "window_start": "2026-05-10", "window_end": "2026-05-16",
 "percent_of_target": 81.1, "on_track": false, "status": "active"}
```

`on_track` is a boolean comparison only — no advice. `GOAL_NOT_FOUND` if the
id is unknown or belongs to a different user.

### 3.12 `log_nutrition(user_id, meal, calories, logged_at, description?, protein_g?, carbs_g?, fat_g?) -> str`

`meal` ∈ {`breakfast`,`lunch`,`dinner`,`snack`}. `calories` kcal (≥ 0).
macros in grams (optional).

### 3.13 `get_nutrition_summary(user_id, date) -> str`

Per-day totals (`total_calories`, `total_protein_g`, `total_carbs_g`,
`total_fat_g`) plus the `meals` list. Totals only — no dietary advice.

### 3.14 `list_health_alerts(user_id, limit=50) -> str`

Descriptive out-of-typical-range flags, newest first. See §Safety.

```json
[{"metric_id": "met_seed_...", "type": "blood_pressure", "value": 146.0,
  "value_text": "146/94", "unit": "mmHg", "recorded_at": "2026-04-19T07:08:00+08:00",
  "typical_low": 90.0, "typical_high": 140.0, "flag": "above_typical_range",
  "note": "... is above typical range (90.0-140.0 mmHg). Informational only; not a diagnosis."}]
```

Typical ranges (descriptive, adult resting): heart_rate 50–100 bpm,
blood_pressure systolic 90–140 mmHg, body_fat 8–30 %. weight/steps/sleep are
not range-checked. `limit` default 50, clamped to 200.

## 4. Storage

SQLite, one file per server. `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL`.

| table            | purpose                                                          |
| ---------------- | ---------------------------------------------------------------- |
| `metrics`        | individual readings; numeric `value` + optional `value_text`     |
| `workouts`       | logged sessions with duration / optional calories+distance       |
| `goals`          | per-user targets with period + direction + status                |
| `nutrition_logs` | logged meals with calories + optional macros                     |
| `_counters`      | atomic seq counters used to mint stable ids                      |

Indices: `(user_id, type, recorded_at)` on `metrics`; `(user_id, started_at)`
on `workouts`; `(user_id, status)` on `goals`; `(user_id, logged_at)` on
`nutrition_logs`.

## 5. State injection

No JSON seed. The server takes `--env <dir>` and on cold start:

1. Unlinks `<env>/runtime.db` (and WAL sidecars).
2. Creates the schema.
3. `executescript`s `<env>/init.sql` if present.
4. Opens streamable-HTTP on `<host>:<port>/mcp`.

The minimal stateless env is `envs/health_tracker/empty/` (empty `init.sql`).

## 6. State evolution across stages

The task orchestrator drives state changes through `mutation` events. A
mutation is one or more SQL statements against this server's runtime DB; the
dispatch path is identical to a caller running raw SQL. This server has no
management CLI, no sweep loop, and no runtime clock.

## 7. Logging & ops

- `logging.getLogger(__name__)` everywhere; handler attached to stderr only.
- No `print()` in the package.

## 8. Appendix — error codes

| code                 | meaning                                                     |
| -------------------- | ----------------------------------------------------------- |
| `BAD_TYPE`           | metric `type` not in the allowed set                        |
| `BAD_PERIOD`         | `period` not in the allowed set for the tool                |
| `BAD_DATE`           | non-ISO date / timestamp string                             |
| `BAD_VALUE`          | non-numeric / out-of-domain value or missing required field |
| `METRIC_NOT_FOUND`   | no reading of the requested type for the user               |
| `WORKOUT_NOT_FOUND`  | `workout_id` does not exist                                 |
| `GOAL_NOT_FOUND`     | `goal_id` unknown or owned by a different user              |
| `BAD_ARG`            | catch-all for malformed inputs                              |

## 9. Out of scope

- No diagnosis / scoring / advice of any kind (see §Safety).
- No pagination cursors (`limit` only).
- No batch / bulk endpoints.
- No real auth, no cross-user permission model beyond owner match on goals.
