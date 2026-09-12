# Workspace Persistence Contract

This file exposes the complete paths and field locations for every fixed file. Field names are case-sensitive; amounts use integer minor units, and `Stage` uses integers. Arrays may be expressed as YAML lists or Markdown entries, but field labels must be retained. All files have `blocking_for_delivery: no`: insufficient quality in a single file must not erase business results already completed in other files.

## `/workspace/gear_plan.md`
- first_required_stage: 0; suggested update stages: 2, 7, 8, 16, 17, 22
- blocking_for_delivery: no
- required_fields: `template_state`, `scenario`, `current_option`, `alternatives`, `selection_basis`, `authorization_state`, `last_updated_stage`
- Each item in `alternatives` must contain `option`, `evidence`, `net_cost_minor`, `schedule_impact`.

## `/workspace/budget.md`
- first_required_stage: 0; suggested update stages: 6, 10, 13, 18, 20, 23
- blocking_for_delivery: no
- required_fields: `template_state`, `currency`, `ordered_minor`, `paid_minor`, `refund_pending_minor`, `refunded_minor`, `holdback_minor`, `resale_received_minor`, `net_outflow_minor`, `source_objects`, `as_of_stage`
- `currency` is fixed as `CNY`; `net_outflow_minor` must be recalculated based on funds actually disbursed; listed prices and pending refunds do not count as received funds.

## `/workspace/decision_log.md`
- first_required_stage: 2; update after each plan, authorization, or status change
- blocking_for_delivery: no
- Each entry's required_fields: `stage`, `decision`, `status`, `basis`, `authorization`, `supersedes`

## `/workspace/risk_register.md`
- first_required_stage: 0; update when a risk is added, resolved, or escalated
- blocking_for_delivery: no
- Each entry's required_fields: `risk`, `status`, `trigger`, `mitigation`, `owner`, `next_review_stage`

## `/workspace/order_tracker.md`
- first_required_stage: 0; update the three objects after each actual status change
- blocking_for_delivery: no
- Three fixed objects: `ord_qgrd_0001`, `ord_qgrd_0002`, `lst_qgrd_0001`
- Each segment's required_fields: `object_id`, `state`, `evidence`, `next_action`, `authorization_required`, `as_of_stage`

## `/workspace/evidence_log.md`
- first_required_stage: 2; update when verifiable tool results, attachments, notifications, or on-site records are obtained
- blocking_for_delivery: no
- Each entry's required_fields: `evidence_id`, `service`, `object_id`, `observed_at_stage`, `fact`, `limits`, `supports`
- `limits` must state what the evidence cannot prove on its own, to avoid treating a notification or weather as a ruling.

## `/workspace/final_summary.md`
- first_required_stage: 23; may be empty before then and must not fail prematurely
- blocking_for_delivery: no
- required_fields: `template_state`, `resolved`, `in_progress`, `pending_user`, `pending_funds`, `safety_boundaries`, `reusable_checklist`, `as_of_stage`
- The three business lines must each be closed out separately; pending items, pending authorization, or funds pending receipt must not be written into `resolved`.

## `/workspace/HEARTBEAT.md`
- first_required_stage: 0; append one line at each stage
- blocking_for_delivery: no
- Each line's required_fields: `stage`, `changed`, `source`, `next`

Valid updates must come from currently disclosed events, successful tool results, or the Agent's own persistent writes. Bank card numbers, contract verification codes, email short-link contents, or rulings about the future that have not occurred must not be recorded.
