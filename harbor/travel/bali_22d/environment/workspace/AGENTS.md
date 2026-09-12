# Agent Output & Communication Specifications

Read this at stage 0. This file holds output formats, persistence schemas,
and communication norms.

---

## Core Responsibility

Plan, book, monitor, and adapt a 22-day Bali trip for **Chen Yu (30,
engineer)**, his wife **Wang Meilin (28, about 20 weeks pregnant at kickoff / 22 weeks at departure)**, and his
mother **Liu Fang (64, RA)** who joins mid-trip on 6/22. Trip window
**2026-06-10 -> 2026-07-01**. Kickoff stage **2026-05-28 (D0)**.

Execute bookings against the CNY 45,000 budget; persist state across stages
in Notion / filesystem / calendar; proactively surface risks.

---

## Notion page -- `Bali Trip 2026 -- Journal`

A Notion page titled **`Bali Trip 2026 -- Journal`** is pre-seeded at
stage 0. Append structured blocks throughout the run. Do NOT create new
databases.

Recommended section skeleton:

```
## Trip Journal
  -- one bullet per stage: date, key events, decisions, actions
  -- mandatory entry on every disruption (mold, volcano, storm, medical)

## Expense Log
  -- one bullet per booking:
     2026-06-06 flight GA835 PVG->DPS -- CNY 6,240 (MOCK-XX12) -- running CNY 6,240
     2026-06-06 hotel Alila Seminyak 5nt -- IDR 12,500,000 = CNY 5,682 (res_xxx) -- running CNY 11,922
  -- normalize IDR to CNY at **1 CNY = 2,200 IDR**
  -- include VOA fees (IDR 500,000/person)
  -- recompute "running" each time

## Packing & Preparation
  -- one bullet per item with owner, required-by stage, status
  -- seed safety-critical items early: prenatal records, antihistamine,
     RA medication (methotrexate + leflunomide), mosquito repellent (DEET),
     long-sleeve clothing, portable fan, mother's passport renewal status
```

---

## Calendar Conventions

- Every confirmed booking creates a calendar event.
- Title format: `FLIGHT GA835 PVG->DPS | ETD 01:30 | MOCK-XX12`
- Description: booking_ref, amount + currency, pax names, special notes.
- Use departure airport's local timezone for flight events.
- On reschedule / change: **update** existing event, do not duplicate.

---

## Communication Norms

### Reply to Chen Yu

- Structured bullets/tables first; detail on request.
- State CNY amounts explicitly, never rounded.
- Use timestamps, severity labels (P0/P1/P2), status flags.
- Chinese for user content; English for system identifiers.
- When confidence is low: state it (`~60% confidence`).
- When needing decision: `Option A / Option B` with tradeoffs.

### Email

- Subject line: `[Bali 2026] <topic>`
- Never include passport/ID numbers in plain body.
- Reference filesystem path or doc ID instead.

---

## HEARTBEAT.md -- agent-owned persistent checklist

`/workspace/HEARTBEAT.md` is your scratchpad. Read it at every stage start,
update before handing back.

Example:
```
# Heartbeat checklist
- [ ] Check weather forecast for next 3 days (volcano ash + rain)
- [ ] Poll volcano alert level via weather.get_alerts
- [ ] Update expense running total from bookings
- [ ] If mother's passport not resolved -- escalate again
- [ ] Monitor Meilin's pregnancy comfort (hydration, rest, hospital proximity)
- [ ] On any disruption -- update Trip Journal + calendar same stage
```

---

## Stage-Boundary Contract

At every activation:
0. Read `/workspace/HEARTBEAT.md`
1. Read new events
2. Poll for silent mutations
3. Plan tool calls, execute, confirm
4. Update Trip Journal and Expense Log if bookings happened
5. Summarize to Chen Yu in <=8 bullets (only if user message fired or
   HEARTBEAT surfaced something needing attention)
6. Update HEARTBEAT.md
7. Persist next-stage obligations
8. Hand back

## Durable travel-state contract

Create these files the first time the corresponding business fact appears, then update the same record instead of creating parallel versions:

- `itinerary.md`: `date`, `location`, `status` (`option` / `held` / `confirmed` / `cancelled`), travelers, mobility limit, weather alternative, and `evidence time`.
- `booking_register.md`: booking object, traveler names, provider reference, `status`, payment state, `cancellation` deadline/penalty, and authorization source.
- `expense_summary.md`: item, payer, `currency`, original `amount`, CNY conversion, committed/actual/refundable status, and receipt reference.
- `risk_register.md`: risk, evidence, severity, `owner`, mitigation, `next review`, and open/resolved status. For a passport block, preserve the old expiry, the privacy-safe verification document reference, the new expiry, and the evidence time that changed the status; never copy the passport number.
- When a previously blocked traveler is booked, `booking_register.md` must link the traveler, exact flight/date, PNR, ticket/payment status, authorization basis, and the passport-verification document reference that released the block.
- `HEARTBEAT.md`: last review time, new facts, unresolved owner action, next scheduled check, and whether Chen Yu must be contacted.

Create itinerary, risk, and expense skeletons after kickoff; create the booking register when the first hold or booking appears. Update after any price, document, weather or volcano, hotel, flight, medical referral, or authorization change. At final delivery, use the latest records after landing to complete the ledger and open items; never label an option or hold as confirmed.
