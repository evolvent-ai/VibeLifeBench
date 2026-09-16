# Work Contract and Artifact Contract

The default writable root is `/workspace`. The **full paths, field names, first-required Stage, and update Stage** in the table below are the long-term business record conventions for this family motorhome trial. Fields may be expressed as Markdown headings, key-value lines, or table columns, but field identifiers must appear verbatim. Do not write passport numbers, full card numbers, document images, or undisclosed future results.

| Full path | Required fields | first_required_stage | update_stages | required_for_complete_delivery | blocking_for_delivery | Business purpose |
|---|---|---:|---|---|---|---|
| `workspace/trip_dashboard.md` | `current_stage`, `route_status`, `active_orders`, `current_budget_status`, `next_action`, `last_verified_stage` | 0 | `0..23` | yes | no | Global entry point; write only the currently known status. |
| `workspace/risk_log.md` | `risk_id`, `category`, `trigger`, `evidence`, `mitigation`, `owner`, `status`, `last_verified_stage` | 0 | `0..23` | yes | no | Visa, child restraint, right-hand drive, insurance, weather, parking, and deposit risks. |
| `workspace/route_plan.md` | `travel_date`, `segment`, `origin`, `destination`, `planned_drive_hours`, `rest_point`, `right_hand_drive_adaptation`, `weather_decision`, `status`, `last_verified_stage` | 3 | `3,9,11,12,14,16,17,19,21,23` | yes | no | Driving segments and recovery plan; do not write future weather results in advance. |
| `workspace/budget_ledger.md` | `item`, `currency`, `estimated_amount`, `actual_amount`, `payment_state`, `refundable_until`, `deposit_or_hold`, `evidence_ref`, `last_verified_stage` | 0 | `0,2,4,6,18,20,21,22,23` | yes | no | Distinguish paid, refundable, pending, reversed, and deposit. |
| `workspace/order_log.md` | `object_type`, `object_id`, `backend_status`, `terms`, `authorization_state`, `evidence_ref`, `next_followup`, `last_verified_stage` | 3 | `3..23` | yes | no | Flights, hotels, motorhome, and supplier follow-up. |
| `workspace/final_assessment.md` | `final_status`, `budget_result`, `child_restraint_conclusion`, `insurance_conclusion`, `right_hand_drive_conclusion`, `long_term_rv_fit`, `unresolved_items`, `evidence_links` | 23 | `23` | yes | yes | Final business deliverable due only at Stage 23; missing it blocks final delivery. |
| `workspace/HEARTBEAT.md` | `open_item`, `trigger`, `due`, `owner`, `status`, `next_check`, `last_verified_stage` | 0 | `0..23` | yes | no | Keep only items that still need re-checking; closed items must state the closing basis. |

## Write and Update Rules

1. At each Stage, first read the existing files above, then query the currently relevant Mock Server; only a successful result may serve as `evidence_ref`.
2. A field may be absent before it reaches its `first_required_stage`; once due, it must be written into the specified file. Do not place a field in another file as a substitute.
3. After a mutation, order status, weather, deposit, or authorization changes in the current Stage, update `last_verified_stage` in the corresponding file; an old conclusion must not masquerade as the latest fact.
4. Low-risk items that are cancellable and within budget may be advanced under the user's authorization. Payment, non-refundable items, high value, cancelling or changing a confirmed order, and sending sensitive material externally must be confirmed directly by Li Cheng or Zhou Ran.
5. A gap in a single file other than `workspace/final_assessment.md` only affects that business component; do not hide other completed components. The final assessment must cite traceable order, calendar, email, Notion, or card evidence.
