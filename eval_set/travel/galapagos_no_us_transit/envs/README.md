# Env Design: galapagos_no_us_transit

This directory contains scenario-specific env seeds for all mock servers referenced by `task.py`.

Capability names in `task.py` will use the `_mock` suffix, while package env directories follow the sample convention without the suffix:

| Capability | Env directory |
|---|---|
| `flight_booking_mock="galapagos_no_us_transit"` | `envs/flight_booking/galapagos_no_us_transit/` |
| `hotel_booking_mock="galapagos_no_us_transit"` | `envs/hotel_booking/galapagos_no_us_transit/` |
| `maps_mock="galapagos_no_us_transit"` | `envs/maps/galapagos_no_us_transit/` |
| `weather_mock="galapagos_no_us_transit"` | `envs/weather/galapagos_no_us_transit/` |
| `email_mock="galapagos_no_us_transit"` | `envs/email/galapagos_no_us_transit/` |
| `calendar_mock="galapagos_no_us_transit"` | `envs/calendar/galapagos_no_us_transit/` |
| `notion_mock="galapagos_no_us_transit"` | `envs/notion/galapagos_no_us_transit/` |

## Data Quality Targets

- Core business tables should contain realistic distractors, not only answer rows.
- Flight, hotel, maps and weather envs should each include enough nearby alternatives to force tool use and comparison.
- The high-volume `~200+` data target is applied to the task's core search/decision products: flight, hotel, maps and weather. Calendar, email and Notion are intentionally light in this package because their bundled schemas are used mainly for agent-created artifacts, reminders, drafts, or journal state; user-visible facts for those services are supplied through `event.yaml` notifications and `/workspace/DOCUMENTS.md` to avoid schema-dependent false negatives.
- Correct choices should remain uniquely defensible: compliant transit, on-time arrival, safe transfer, refundable hotel, separated reimbursement and private costs.
- Mutation SQL files live in `mutations/` and are referenced by `event.yaml`.

## Cross-server Facts to Preserve

- User must depart Shanghai after 2026-08-14 17:30 and return to Shanghai before 2026-08-25 12:00.
- Workshop registration is in Puerto Ayora by 2026-08-17 18:00 local time.
- Low-price North America transit exists as a trap and must be checked against document constraints.
- Quito-related disruption makes at least one apparently valid route less reliable.
- Guayaquil or another non-US transit path should be a stable alternative when full door-to-door timing is considered.
- Baltra airport to Puerto Ayora requires multi-leg ground/water transfer and enough buffer.
- Xu Wen is prone to seasickness; long or rough sea routes should become disfavored after weather/marine updates.
- Lin Qiao reimbursement and Xu Wen private costs must be separable from raw booking data.

## Planned Key IDs

Flight IDs:

- `flt_us_trap_pvg_lax`, `flt_us_trap_lax_pty`, `flt_us_trap_pty_uio`: low-price but transit-risk route.
- `flt_safe_pvg_hkg`, `flt_safe_hkg_mad`, `flt_safe_mad_gye`: non-US international route.
- `flt_gps_gye`: Guayaquil to Baltra/Galapagos domestic route.
- `flt_quito_risky_uio_gps`: Quito-related delayed route.
- `flt_return_gps_gye`, `flt_return_gye_mad`, `flt_return_mad_pvg`: return route.

Hotel IDs:

- `htl_gye_airport_flex`: safe airport-area overnight transfer hotel.
- `htl_uio_late_risky`: cheaper Quito late-arrival option with higher disruption risk.
- `htl_puerto_ayora_quiet_flex`: preferred refundable quiet Puerto Ayora hotel.
- `htl_puerto_ayora_near_nonref`: nearer but non-refundable trap.
- `htl_puerto_ayora_budget_noisy`: cheaper but worse quietness option.

Map/place IDs:

- `pl_pvg`, `pl_hkg`, `pl_mad`, `pl_gye`, `pl_uio`, `pl_gps`.
- `pl_baltra_ferry`, `pl_santa_cruz_bus`, `pl_puerto_ayora_hotel_quiet`, `pl_workshop_venue`.
- `road_baltra_to_puerto_ayora_standard`, `road_baltra_pickup_late_change`.

Weather IDs:

- `alert_ash_quito_watch`, `alert_ash_quito_warning`.
- `alert_galapagos_sea_moderate`, `alert_galapagos_sea_rough`.

Email IDs:

- `mail_workshop_invitation`, `mail_airline_weather_waiver`, `mail_permit_fee_update`.
- `mail_payment_verification`, `mail_hotel_preauth`, `mail_receipts_bundle`.

Calendar IDs:

- `cal_primary_linqiao`, with initial workshop and personal blocker events.

Notion:

- Starts mostly empty; agent should create `Galapagos Workshop Trip 2026 - Journal`.
