# Working Rules

Work in `/workspace` or `/terrarium/openclaw/workspace`.

Maintain these durable files as the task evolves:

- `planning_ledger.md`: current objective, attendance count, source checks, next actions.
- `budget_register.md`: line items split by budget category and approval status.
- `book_procurement.md`: book candidates, stock, cart status, coupon status, and learning-budget evidence.
- `group_roster.md`: mixed discussion groups and department balance; do not expose dietary details broadly.
- `guest_coordination.md`: guest availability, approved internal-use bio handling, and calendar status.
- `venue_catering_log.md`: venue and dinner candidates, capacity, invoice, allergy, vegetarian, and reservation status.
- `feedback_archive.md`: private aggregate feedback summary and internal follow-up items.
- `privacy_log.md`: authorization checks and public-sharing decisions.
- `final_handoff.md`: final operational handoff for Ella.
- `audit_journal.md`: stage-by-stage source checks and decisions.

At the end of each stage, update the relevant files with source names and dates.
Do not include guessed internal IDs or evaluation notes in the workspace.

## Persistent file contract

Use the exact paths below. Each file must retain `Last verified`, `Sources checked`, `Current status`, `Open blockers`, and `Next action`.

| File | First required stage | Required fields |
|---|---:|---|
| `planning_ledger.md` | 0 | objective; latest attendance; event date/time; source status; next actions |
| `budget_register.md` | 0 | category; item; quantity; unit/subtotal/net cost; approval; payment state |
| `book_procurement.md` | 1 | title/SKU; attendee copies; facilitator copies; stock; coupon; cart quantity; net learning cost |
| `group_roster.md` | 2 | final attendance; group; department mix; facilitator; private dietary handling |
| `guest_coordination.md` | 5 | guest time window; calendar status; bio-use scope; Q&A notes visibility; source date |
| `venue_catering_log.md` | 1 | vendor; capacity; accessibility; equipment; invoice; dietary/allergy handling; hold/reservation state |
| `feedback_archive.md` | 20 | aggregate themes; raw-comment storage boundary; access; follow-up owner; publication status |
| `privacy_log.md` | 5 | guest bio; roster/dietary data; raw feedback; photo/public-use authorization; decision source |
| `final_handoff.md` | 24 | attendance; groups; guest time; venue; dinner; book cart; budget split; unpaid/unsigned items; archive plan |
| `audit_journal.md` | 0 | stage/date; tools and records checked; changed facts; decision; files updated |
