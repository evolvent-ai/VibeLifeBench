# San Francisco Summit Durable Artifact Contract

The three paths below are the authoritative persistent records. Paths and field labels are case-sensitive and must remain under `/workspace`.

| path | required fields / sections | first_required_stage | update_stages | required_for_complete_delivery | blocking_for_delivery | business reason |
|---|---|---:|---|---|---|---|
| `/workspace/trip_plan.md` | `trip_status`, `outbound_option_or_booking`, `return_option_or_booking`, `hotel_status`, `entry_document_status`, `calendar_commitments`, `disruption_updates`, `source_or_object_refs`, `last_verified_at` | 0 | 6, 8, 10, 13, 17, 19, 23, 24, 25 | yes | yes | Single operational itinerary and readiness handoff. |
| `/workspace/budget_tracker.md` | `policy_budget_cny`, `approval_threshold_cny`, `internal_fx_rate`, `flight_items`, `hotel_items`, `ground_and_meal_items`, `committed_total_cny`, `projected_total_cny`, `remaining_cny`, `source_or_transaction_refs`, `last_updated_at` | 3 | 4, 7, 12, 13, 20, 22, 25 | yes | no | Company-budget and reimbursement pre-review. |
| `/workspace/decision_log.md` | `decision_at`, `decision`, `reason`, `evidence_ref`, `authorization_status`, `owner`, `follow_up`, `status` | 1 | every Stage with a decision, conflict, rejection, or approval dependency | yes | no | Explains why options changed and what still needs authorization. |

## Lifecycle rules

- Before `first_required_stage`, a missing file is acceptable; once due, create it and update in place.
- Use the internal finance rate supplied by the company only for pre-review. Label it as an internal planning rate rather than a guaranteed market or reimbursement rate.
- An EVUS draft, reminder, or reply-only statement is not a completed enrollment. Record the formal tool result and current status separately from the B1/B2 visa.
- If no compliant booking can be completed, persist the failed precondition, closest viable option, owner, and next action instead of inventing a confirmation number.
