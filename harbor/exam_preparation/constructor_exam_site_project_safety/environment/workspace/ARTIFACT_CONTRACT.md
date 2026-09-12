# Persistent Asset Contract

All paths are relative to `/workspace`. Use the field names exactly as shown in the table below; for files that have not yet reached the first required Stage, an empty skeleton may be kept, and after reaching that Stage, write only facts verified through official sources or tools.

| Full path | First required Stage | Field |
|---|---:|---|
| `/workspace/prep_plan.md` | 0 | `stage`、`exam_window`、`study_block`、`protected_project_block`、`mock_exam`、`next_review` |
| `/workspace/source_evidence.md` | 0 | `source_type`、`source_id`、`title`、`published_at`、`effective_at`、`retrieved_at`、`applicability`、`status` |
| `/workspace/project_conflict_matrix.md` | 2 | `project_event`、`project_window`、`exam_or_study_event`、`conflict`、`priority_reason`、`resolution`、`verified_at` |
| `/workspace/ce_integrity_log.md` | 3 | `course`、`required_hours`、`verified_hours`、`gap_hours`、`evidence`、`status`、`next_action` |
| `/workspace/auth_log.md` | 4 | `action`、`scope`、`reversible`、`status`、`requested_at`、`confirmed_at`、`evidence` |
| `/workspace/safety_privacy_log.md` | 5 | `record_type`、`sensitivity`、`recipient_or_channel`、`minimum_disclosure`、`status`、`mitigation` |
| `/workspace/material_log.md` | 6 | `item`、`version`、`authorization_source`、`order_status`、`shipment_status`、`return_status`、`cost_minor`、`last_verified_at` |
| `/workspace/budget_reimbursement.md` | 7 | `category`、`amount_minor`、`budget_minor`、`invoice_status`、`reimbursement_status`、`authorization_status`、`evidence` |
| `/workspace/travel_matrix.md` | 15 | `exam_site`、`exam_date`、`route`、`arrival_buffer`、`hotel`、`refund_policy`、`total_minor`、`authorization_status`、`last_verified_at` |
| `/workspace/final_review.md` | 23 | `registration_status`、`ce_status`、`material_status`、`project_handover`、`travel_status`、`privacy_status`、`budget_status`、`open_items` |

## Fixed Semantics

- The First-Class Constructor Examination dates are recorded as September 12 to 13, 2026; classroom, seat, and entry information remain subject to the admission ticket and subsequent official notices.
- Project site safety responsibilities take priority over ordinary study arrangements; when changing study blocks, retain project events and the reasons for conflicts.
- Continuing education records only real courses, attendance, and completion status; do not fabricate training hours.
- Payments, ticket purchases, non-refundable hotels, high-cost courses, changes, and reimbursement submissions must have an explicit status in `/workspace/auth_log.md`.
- Project drawings, accident photos, contract amount pages, personnel lists, and sensitive originals must not go into ordinary email or public content platforms.
