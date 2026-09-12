# Workspace renovation note

renovation note fixed renovation note of  full renovation note with  field renovation note。 field renovation note； amount renovation note，Stage renovation note。renovation note YAML renovation note or  Markdown renovation note，renovation note field  label renovation note must  retain 。renovation note `blocking_for_delivery: no`：renovation note already  complete  of renovation note result 。

## `/workspace/gear_plan.md`
- first_required_stage: 0；renovation note update  stage ：2、7、8、16、17、22
- blocking_for_delivery: no
- required_fields: `template_state`, `scenario`, `current_option`, `alternatives`, `selection_basis`, `authorization_state`, `last_updated_stage`
- `alternatives`  in renovation note `option`, `evidence`, `net_cost_minor`, `schedule_impact`。

## `/workspace/budget.md`
- first_required_stage: 0；renovation note update  stage ：6、10、13、18、20、23
- blocking_for_delivery: no
- required_fields: `template_state`, `currency`, `ordered_minor`, `paid_minor`, `refund_pending_minor`, `refunded_minor`, `holdback_minor`, `resale_received_minor`, `net_outflow_minor`, `source_objects`, `as_of_stage`
- `currency`  fixed renovation note `CNY`；`net_outflow_minor` renovation note has renovation note， listing renovation note and renovation note refund renovation note。

## `/workspace/decision_log.md`
- first_required_stage: 2；renovation note plan 、renovation note or  status renovation note after  update 
- blocking_for_delivery: no
-  each item  required_fields: `stage`, `decision`, `status`, `basis`, `authorization`, `supersedes`

## `/workspace/risk_register.md`
- first_required_stage: 0； risk renovation note、renovation note or renovation note update 
- blocking_for_delivery: no
-  each item  required_fields: `risk`, `status`, `trigger`, `mitigation`, `owner`, `next_review_stage`

## `/workspace/order_tracker.md`
- first_required_stage: 0；renovation note verified  status renovation note after  update 
- blocking_for_delivery: no
- renovation note fixed renovation note：`ord_qbed_0001`, `ord_qbed_0002`, `lst_qbed_0001`
- renovation note required_fields: `object_id`, `state`, `evidence`, `next_action`, `authorization_required`, `as_of_stage`

## `/workspace/evidence_log.md`
- first_required_stage: 2；renovation note review renovation note result 、renovation note、 notification  or  site  record renovation note update 
- blocking_for_delivery: no
-  each item  required_fields: `evidence_id`, `service`, `object_id`, `observed_at_stage`, `fact`, `limits`, `supports`
- `limits` renovation note must  explanation  evidence  cannot renovation note proof renovation note，renovation note notification  or  weather renovation note。

## `/workspace/final_summary.md`
- first_required_stage: 23；renovation note before renovation note empty renovation note must not renovation note before renovation note
- blocking_for_delivery: no
- required_fields: `template_state`, `resolved`, `in_progress`, `pending_user`, `pending_funds`, `safety_boundaries`, `reusable_checklist`, `as_of_stage`
- renovation note separately  finishing detail ； must not renovation note handle 、renovation note or renovation note write  `resolved`。

## `/workspace/HEARTBEAT.md`
- first_required_stage: 0；renovation note stage renovation note
- blocking_for_delivery: no
- renovation note required_fields: `stage`, `changed`, `source`, `next`

renovation note update renovation note must renovation note current  has renovation note event 、renovation note result  or  Agent renovation note of renovation note write 。 must not  record  bank card renovation note、 verification code 、 email  short link  content  or  not renovation note of  not renovation note。
