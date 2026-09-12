# Workspace Artifact Contract

This task has 22 stages (`0..21`). Read `IDENTITY.md`, `USER.md`, `PERSONA.md`, `SOUL.md`, `TOOLS.md`, `HEARTBEAT.md`, and existing canonical files at every stage. The writable root is `/workspace`. Exact fields may be Markdown headings, key/value labels, or table columns, but must appear in the specified file.

| Full path | Required fields | first_required_stage | update_stages | required_for_complete_delivery | blocking_for_delivery | Business purpose |
|---|---|---:|---|---|---|---|
| `workspace/audit_journal.md` | `stage`, `checked_at`, `tool_or_source`, `backend_object_id`, `result_status`, `decision`, `files_updated` | 0 | `0..21` | yes | no | Append material successful checks, decisions, boundaries, and writes. |
| `workspace/HEARTBEAT.md` | `open_item`, `trigger`, `owner`, `due`, `status`, `next_check`, `last_verified_stage` | 0 | `0..21` | yes | no | Only unresolved cross-stage work; close items with evidence. |
| `workspace/trip_evidence_log.md` | `evidence_id`, `service`, `backend_object_id`, `fact_summary`, `verified_at`, `verified_stage`, `source_lineage`, `freshness_status` | 1 | `1..21` | yes | no | Email, flight, hotel, rail, maps, weather, calendar, Notion, card, and restaurant facts. |
| `workspace/trip_risk_register.md` | `risk_id`, `category`, `trigger`, `impact`, `mitigation`, `owner`, `status`, `evidence_id`, `last_verified_stage` | 2 | `2..21` | yes | no | Allergy, refund, transport, weather, calendar, privacy and authorization risks. |
| `workspace/authorization_ledger.md` | `authorization_id`, `actor`, `scope`, `reversible_or_irreversible`, `decision`, `received_at`, `evidence_id`, `status` | 2 | `2,9,11,13,14,19,21` | yes | no | Direct Maya approvals and declined/deferred proxy requests. |
| `workspace/budget_and_booking_state.md` | `item_id`, `service`, `backend_object_id`, `currency`, `amount`, `budget_state`, `booking_state`, `refundability`, `refund_or_fee_state`, `last_verified_stage` | 2 | `2..21` | yes | no | EUR 4,800 cap, card-safe references, candidates, deadlines, and terminal states. |
| `workspace/final_travel_packet.md` | `final_status`, `flight_state`, `hotel_state`, `rail_state`, `restaurant_state`, `allergy_controls`, `authorization_history`, `wedding_buffer`, `open_risks`, `next_manual_actions`, `evidence_links` | 19 | `19,21` | yes | yes | Wedding-day and final handoff packet; absence blocks final delivery. |

## Operational rules

1. A field is not required before its `first_required_stage`. When a listed update stage changes relevant facts, refresh `last_verified_stage`/`verified_stage`; stale presence is not enough.
2. Put each field in its specified file. A same-named field in an ad hoc `notes.md`, `plan.md`, `todo.md`, or `summary.md` does not satisfy this business archive.
3. Direct Maya approval is required for irreversible or nonrefundable action. Luca, friends, vendors, and family members cannot proxy that authority.
4. Do not reserve a restaurant until current backend evidence addresses pine nut exposure and cross-contact controls. Ratings alone are insufficient.
5. Do not persist passport numbers, full card numbers, document identifiers, or other private values in outbound mail or final files.
6. A missing non-blocking file reduces only that component. `workspace/final_travel_packet.md` is the sole blocking file and becomes due at Stage 19.
