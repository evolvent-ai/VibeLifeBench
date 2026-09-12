# family travel detail Artifact Contract

family travel detail `/workspace`。family travel detail**family travel detail、family travel detail、family travel detail Stage family travel detail Stage**family travel detailfamilymotorhomefamily travel detail。family travel detail Markdown family travel detail、family travel detail，family travel detailmustfamily travel detail。family travel detailpassportfamily travel detail、family travel detail、family travel detail。

| family travel detail | family travel detail | first_required_stage | update_stages | required_for_complete_delivery | blocking_for_delivery | family travel detail |
|---|---|---:|---|---|---|---|
| `workspace/trip_dashboard.md` | `current_stage`, `route_status`, `active_orders`, `current_budget_status`, `next_action`, `last_verified_stage` | 0 | `0..23` | yes | no | family travel detail，family travel detailstatus。 |
| `workspace/risk_log.md` | `risk_id`, `category`, `trigger`, `evidence`, `mitigation`, `owner`, `status`, `last_verified_stage` | 0 | `0..23` | yes | no | family travel detail、childrestraint、family travel detail、insurance、family travel detail、family travel detail、depositfamily travel detail。 |
| `workspace/route_plan.md` | `travel_date`, `segment`, `origin`, `destination`, `planned_drive_hours`, `rest_point`, `right_hand_drive_adaptation`, `weather_decision`, `status`, `last_verified_stage` | 3 | `3,9,11,12,14,16,17,19,21,23` | yes | no | family travel detail；must notfamily travel detail。 |
| `workspace/budget_ledger.md` | `item`, `currency`, `estimated_amount`, `actual_amount`, `payment_state`, `refundable_until`, `deposit_or_hold`, `evidence_ref`, `last_verified_stage` | 0 | `0,2,4,6,18,20,21,22,23` | yes | no | family travel detail paid、refundable、pending、reversed、deposit。 |
| `workspace/order_log.md` | `object_type`, `object_id`, `backend_status`, `terms`, `authorization_state`, `evidence_ref`, `next_followup`, `last_verified_stage` | 3 | `3..23` | yes | no | family travel detail、hotel、motorhomefamily travel detail。 |
| `workspace/final_assessment.md` | `final_status`, `budget_result`, `child_restraint_conclusion`, `insurance_conclusion`, `right_hand_drive_conclusion`, `long_term_rv_fit`, `unresolved_items`, `evidence_links` | 23 | `23` | yes | yes | Stage 23 family travel detail；family travel detail。 |
| `workspace/HEARTBEAT.md` | `open_item`, `trigger`, `due`, `owner`, `status`, `next_check`, `last_verified_stage` | 0 | `0..23` | yes | no | family travel detailretainfamily travel detail，family travel detail。 |

## family travel detail

1. family travel detail Stage family travel detail，family travel detailqueryfamily travel detail Mock Server；family travel detail `evidence_ref`。
2. family travel detail `first_required_stage` family travel detail；family travel detail，mustfamily travel detail。must notfamily travel detail。
3. family travel detail Stage family travel detail mutation、family travel detailstatus、family travel detail、depositfamily travel detail，family travel detail `last_verified_stage`；family travel detailmust notfamily travel detail。
4. family travel detailcancelledfamily travel detailbudgetfamily travel detailuserfamily travel detail。payment、non-refundable、high value、cancelled/family travel detail、sending sensitive materialmustfamily travel detailLi Chengfamily travel detailZhou Ranfamily travel detail。
5. `workspace/final_assessment.md` family travel detail；must notfamily travel detail。family travel detailmustfamily travel detail、calendar、family travel detail、Notion family travel detail。
