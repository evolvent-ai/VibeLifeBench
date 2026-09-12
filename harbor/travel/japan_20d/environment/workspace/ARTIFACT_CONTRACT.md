# Japan Trip Durable Artifact Contract

This is the authoritative file-and-field map for persistent trip records. Paths and field labels are case-sensitive. Keep the files in `/workspace`; do not create alternate names.

| path | required fields / sections | first_required_stage | update_stages | required_for_complete_delivery | blocking_for_delivery | business reason |
|---|---|---:|---|---|---|---|
| `/workspace/HEARTBEAT.md` | `open_item`, `reason`, `next_check_at`, `source_or_object_ref`, `owner`, `status` | 0 | every Stage with a new unresolved fact | yes | no | Carries monitoring obligations across quiet gaps. |
| `/workspace/itinerary.md` | `segment_date`, `city_or_route`, `status`, `booking_or_source_ref`, `transfer_and_walking_load`, `meal_or_medical_pacing`, `contingency`, `last_verified_at` | 0 | 2, 8, 11, 14, 16, 17, 22, 23 | yes | yes | Final day-by-day movement plan and disruption handoff. |
| `/workspace/expense_summary.md` | `currency`, `committed_items`, `pending_items`, `refunds_or_compensation`, `committed_total_cny`, `projected_total_cny`, `remaining_to_60000_cny`, `source_or_booking_refs`, `last_updated_at` | 3 | 5, 8, 9, 16, 17, 23 | yes | no | Running budget and final reconciliation. |
| `/workspace/packing_briefing.md` | `traveler`, `carry_on_medication`, `prescription_or_import_documents`, `insulin_storage`, `meal_gap_plan`, `departure_checklist`, `return_checklist`, `source_refs`, `last_updated_at` | 7 | 8, 13, 14, 17, 21 | yes | yes | Safety-critical medication and parent handoff. |

`/workspace/weather_alerts.log` is a system-owned notification sink. Read and cite it when present, but do not fabricate entries or replace it with an Agent-authored file.

## Lifecycle rules

- Before a file's `first_required_stage`, its absence is acceptable.
- On an `update_stages` Stage, update only with facts visible by that Stage and preserve earlier valid entries.
- `status` values for open items are `open`, `monitoring`, `blocked_pending_authorization`, or `closed`.
- A source reference may be a successful tool-return object ID, email message ID, booking reference, calendar event ID, or the dated notification that released the fact.
- Missing non-blocking records require an explicit gap, impact, owner, and recovery step in the final handoff; do not invent data.
