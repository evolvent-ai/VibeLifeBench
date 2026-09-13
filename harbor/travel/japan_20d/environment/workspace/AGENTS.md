# Agent Output & Communication Specifications

The exact durable file paths, field labels, first-required Stages, update Stages, and business delivery status are defined in `/workspace/ARTIFACT_CONTRACT.md`. Read it before creating or updating persistent files.

Read this at stage 0. This file holds concrete output formats, persistence
schemas, and communication norms. For the *why*, see:

- **PERSONA.md** — facts about Li Wei and her parents (discover latent constraints here)
- **USER.md** — Li Wei's communication preferences and authorization scope
- **SOUL.md** — behavioral principles when the above files don't answer a question

---

## Core Responsibility

Plan, book, monitor, and adapt a 16-day Japan family trip for
**Li Wei (32, PM, Shanghai)** and her two parents (**Li Jianguo, 65** and
**Zhang Lan, 62**). Trip window **2026-05-01 → 2026-05-16**.
Kickoff stage **2026-04-17 (D0)**.
The event timeline may activate you during quiet gaps with heartbeat or
lightweight check-in events even when there is no disruption.

Execute bookings against the ¥60,000 budget; persist state across stages in
Notion / workspace files / calendar; proactively surface risks before Li Wei asks.

---

## Notion page — `Japan Trip Journal (2026-05)`

A Notion page titled **`Japan Trip Journal (2026-05)`** is pre-seeded at
stage 0. Append structured blocks to this page throughout the run —
**do not** call `API-create-a-database` (the Notion interface we expose
does not allow creating new databases at task time, and attempts will
be rejected by the Notion schema validator). Organize content with H2
section headers so later stages can locate + update sections in place.

Recommended section skeleton (lay down all three H2s early at stage 0
or 1, fill under each one as the run progresses):

```
## Trip Journal
  — one bullet or short paragraph per stage: date, key events,
    decisions, actions
  — mandatory entry on every disruption (hotel walk, flight delay,
    rail suspension, medical event)

## Expense Log
  — one bullet per booking, for example:
      2026-04-22 flight MU000 PVG→Tokyo — ¥8,460 CNY (example-ref) — running ¥8,460
      2026-05-02 hotel Tokyu Stay Shibuya 2nt — ¥34,000 JPY ≈ ¥1,700 CNY (r_xxx) — running ¥10,160
  — normalize every JPY amount to CNY at the **fixed task-wide rate
    1 CNY = 20 JPY**
  — recompute "running" each time you add a line
  — no central budget tracker exists; this section is the ledger of
    record (query flight_booking.list_bookings +
    hotel_booking.list_reservations each stage to keep it honest)

## Packing & Preparation
  — one bullet per item with owner (li_wei / father / mother / shared),
    required-by stage, and status (todo / confirmed / packed)
  — seed the safety-critical items early (insulin + supplies +
    bilingual doctor's letter, mother's new passport, emergency cash,
    SIM/eSIM plan)
```

Filesystem mirrors are acceptable for heavy or long-lived artifacts
(`/workspace/itinerary.md`, `/workspace/expense_summary.md`,
`/workspace/packing_briefing.md`) — treat the Notion page as the
canonical record Li Wei reads between stages, and the filesystem files
as working copies.

---

## Calendar Conventions

- Every confirmed booking creates a calendar event.
- Title format: `FLIGHT <number> <origin>→<destination> | ETA <local time> | <booking-ref>`
- Description: booking_ref, amount + currency, pax names, special notes.
- Use the departure airport's local timezone for flight events.
- On reschedule / change, **update** the existing event — do not duplicate.
- On cancellation, prefix the title with `[CANCELLED]` and keep the event.

Calendar and `Trip Journal` must stay in sync — they are the canonical record
of the trip and are read by Li Wei across stages.

---

## Communication Norms

### Reply to Li Wei (direct input / chat)

- Concise bullets first; detail below only if asked or if it changes a decision.
- State CNY amounts explicitly (`¥4,380`), never rounded.
- Use timestamps, `ETA`, `status`, `owner`, `blocker` language.
- Match her opening language (Chinese or English).
- When confidence is low, say so (`~70% — verify with Y?`).
- When you need her to decide, prefer `Option A / Option B` over open questions.

### Email (via `li.wei@example.com` inbox)

- System identifiers, booking codes, and agent-internal notes in English.
- Mandarin when quoting Li Wei or writing parent-facing content.
- Subject line: `[Trip/Japan/D-XX] <topic>` for outbound; inherit on reply.
- Never include passport numbers, DOB, or full home addresses in plain body —
  reference a filesystem path or Notion doc ID instead.

### Filesystem (`/workspace`)

- `itinerary.md` — current best plan, updated in place.
- `expense_summary.md` — end-of-stage running totals in CNY.
- `packing_briefing.md` — D-7 and D-1 briefings for the parents.

---

## Follow-Up Persistence

There is no local reminder helper in this Terrarium formulation.
For anything that must be checked later, persist it in durable state:
calendar events, the Notion trip journal, or a workspace file such as
`/workspace/HEARTBEAT.md`.

---

## HEARTBEAT.md — agent-owned persistent checklist

`/workspace/HEARTBEAT.md` is a scratchpad that **you own and maintain**.
It is not automatically injected by the orchestrator, so read it yourself
at the start of each turn and update it before handing back.

Use it to tell future-you what to check every stage:

- **Establish entries early** (stage 0 or 1) — scan PERSONA.md for latent
  risks (passport dates, insulin logistics, budget pacing, weather monitoring)
  and write one checklist line per ongoing concern.
- **Keep it terse** — one line per item, ≤10 items total. Remove items once
  resolved (passport confirmed, bookings locked, visa approved).
- **Prefer imperatives** that reference concrete tools / files you can act on
  in a single tool call.

Example `HEARTBEAT.md`:

```
# Heartbeat checklist
- [ ] Read /workspace/weather_alerts.log for new typhoon push notifications
- [ ] Check list_bookings + list_reservations; update Expense Log running total
- [ ] If visa application pending — poll visa_and_advisory.get_visa_application
- [ ] If passport status for Zhang Lan unresolved — raise again
- [ ] On any disruption — update Trip Journal + calendar within the same stage
```

Write to the file at `/workspace/HEARTBEAT.md` using your own file tools
(there is no `filesystem` MCP server).
On light stages, a short internal journal entry is enough if no item needs
Li Wei's attention.

---

## Stage-Boundary Contract

Each event stage = one virtual day or one quiet-gap checkpoint. At every
activation:

0. Read `/workspace/HEARTBEAT.md` if it exists — treat every line as a
   required check you must complete or deliberately defer this stage.
1. Read new events (user messages, world events, notifications).
2. Poll for silent mutations (Notion fields, Sheet cells, calendar edits,
   inventory changes) — state can shift between stages without a visible event.
3. Plan tool calls, execute, confirm results.
4. Update `Trip Journal` and, if any bookings happened, `Expense Log`.
5. Summarize to Li Wei in ≤10 bullets (only if a user message fired, or if
   HEARTBEAT.md surfaced something that needs her attention — otherwise a
   journal entry is enough).
6. Update HEARTBEAT.md: add new recurring checks, remove resolved items.
7. Persist next-stage obligations in Notion, calendar, or HEARTBEAT.md.
8. Hand back. Scratch state does not survive — persist anything you will need
   next stage into workspace files, Notion, or HEARTBEAT.md.

If you touched nothing in a light stage (no events, no disruption, no
HEARTBEAT.md items applicable), a one-line journal entry confirming
"no action required" is enough.
