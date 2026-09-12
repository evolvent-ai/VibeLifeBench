# Work Contract

The working directory is `/terrarium/openclaw/workspace`. Maintain the following fixed files after processing each event or performing a scheduled review; do not change the filenames:

- `stage_progress.md`: the source, queries, decisions, and next steps for each key stage.
- `service_consistency_matrix.md`: state propagation across calendar, health_tracker, weather, ecommerce, email, and notion.
- `risk_log.md`: dizziness, sleep, rainy weather, nighttime lighting, data quality, and safety alternatives.
- `calendar_change_log.md`: training, recovery, weather checks, equipment checks, and route adjustments.
- `auth_log.md`: authorization status for purchases, payments, email sending, meeting adjustments, and other actions.
- `equipment_budget.md`: candidate equipment, confirmed equipment, remaining budget, and unconfirmed items.
- `weather_route_log.md`: Route A/B/C, weather, roadworks, lighting, and the rationale for the final route.
- `final_review.md`: final review, conditions for the following month, and incomplete confirmations.

When processing each event, refresh the relevant service facts first, then update the persistent files. Background state may change; a scheduled check is an opportunity to query again.

## Standard Fields

Each record contains: `time`, `source`, `service`, `fact or status`, `action`, `authorization status`, `risk`, and `next step`. If the interface clearly displays a Stage number, `stage` may be used as an auxiliary index; it is not a required delivery field, and do not add internal labels such as `S00` or `stage0` merely for bookkeeping. Do not write weather, health, delivery, or authorization results before they have appeared.

| File | First required | When to update | Required contents |
|---|---:|---|---|
| `stage_progress.md` | Stage 0 | Every Stage with a visible event | Query sources, current status, decisions, actions, and next steps |
| `service_consistency_matrix.md` | Stage 1 | After changes occur to weather, health, calendar, equipment, email, or route | Cross-service facts, time, objects, and inconsistencies |
| `risk_log.md` | Stage 0 | After dizziness, insufficient sleep, rainy weather, bicycle commuting at night, roadworks, or a sync gap appears | Risks, triggering evidence, pause conditions, and alternatives |
| `calendar_change_log.md` | Stage 2 | After training/recovery/weather check/equipment check/route reminders change | Original arrangement, new arrangement, reasons, and final calendar status |
| `auth_log.md` | Stage 0 | When purchases, payments, email sending, or work arrangements are involved | Request, authorization status, actual actions, and unexecuted items |
| `equipment_budget.md` | Stage 0 | After changes to candidate, confirmation, delivery, or promotion status | Product, purpose, price, confirmation status, order status, and remaining budget |
| `weather_route_log.md` | Stage 1 | After changes to weather, roadworks, lighting, or route availability | Conditions, status, risks, and alternative rationale for Route A/B/C |
| `final_review.md` | Stage 27 | Final review | Verified facts, missing items, closed authorization loop, final route, and conditions for the next cycle |
