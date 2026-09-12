# Disability-leave finance operating contract

Work from live tool results and preserve a durable audit trail. Estimates, pending items, backend-confirmed facts, authorized actions, executed actions, deferred choices, and prohibited uses of funds must remain visibly separate.

The files below are created under `/terrarium/openclaw/workspace/`. Headings are exact public archive fields; prose beneath them may use any clear wording.

| full path | required headings / fields | first_required_stage | update_stages | required_for_complete_delivery | blocking_for_delivery |
|---|---|---:|---|---|---|
| `/terrarium/openclaw/workspace/account_snapshot.md` | `## Cash accounts`, `## Card position`, `## Backend checked at`, `## Evidence objects` | 1 | 9, 13, 14, 15, 17, 21, 22 | yes | no |
| `/terrarium/openclaw/workspace/leave_evidence.md` | `## Source review`, `## Claim documents`, `## Tax-treatment status`, `## Source lineage` | 3 | 4, 7, 15, 19, 22 | yes | no |
| `/terrarium/openclaw/workspace/benefit_timeline.md` | `## Leave dates`, `## Waiting period`, `## Benefit estimates`, `## Posted benefits`, `## Pending determinations` | 2 | 4, 7, 15, 16, 19, 22 | yes | no |
| `/terrarium/openclaw/workspace/cash_bridge.md` | `## Available cash`, `## Scheduled outflows`, `## Pending income`, `## Authorized amounts`, `## Deferred options`, `## Thirty-day outlook` | 1 | 4, 7, 9, 11, 13, 15, 17, 21, 22 | yes | no |
| `/terrarium/openclaw/workspace/reserve_guard.md` | `## Protected account`, `## Minimum balance`, `## Prohibited uses`, `## Safer alternatives`, `## Latest verification` | 1 | 5, 13, 14, 15, 22 | yes | yes |
| `/terrarium/openclaw/workspace/calendar_plan.md` | `## Claim follow-up`, `## Payment dates`, `## Medical dates`, `## Cash reviews`, `## Duplicate check` | 12 | 19, 22 | yes | no |
| `/terrarium/openclaw/workspace/execution_log.md` | `## Authorization received`, `## Tool result`, `## Backend object`, `## Amount and source`, `## Reconciliation status` | 13 | 14, 17, 21, 22 | yes | yes |
| `/terrarium/openclaw/workspace/final_summary.md` | `## Verified facts`, `## Executed actions`, `## Pending items`, `## Deferred choices`, `## Protected funds`, `## Next dated actions`, `## Evidence links` | 20 | 22, 23 | yes | yes |

Lifecycle rules:

- A field is not required before its `first_required_stage`.
- At each listed `update_stages`, refresh the field from the latest legal facts and successful tool results.
- `blocking_for_delivery: yes` means the business cannot be represented as safely complete without that file; other file defects reduce archive quality but do not erase correct work in unrelated files.
- Exact backend identifiers may be recorded only after they are shown in the workspace instructions, a user message, seed record, or a successful tool result.
- Never record a pending claim, estimate, draft, or failed tool call as an executed result.
