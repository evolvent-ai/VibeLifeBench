# Tool Usage — Japan 20-Day Trip Cheat Sheet

This is the "when do I reach for which tool on THIS task" guide.
Full parameter reference lives in each server's `SPEC.md`; this
file is the task-shaped shortlist.

9 services are available (5 travel-specific mocks + 4 reused
toolathlon servers):

- `flight_booking`, `hotel_booking`, `weather`, `maps`,
  `visa_and_advisory` (task-new)
- `emails`, `calendar`, `filesystem`, `notion` (reused)

There is no local reminder helper in this Terrarium formulation; persist
follow-ups in Notion, calendar, or workspace files.

---

## 1. `flight_booking` — core booking

**When to use**

- Searching PVG↔NRT / PVG↔KIX fares for the 3-pax party on the
  pre-trip stages (ideally locked by stage 9, per D9 user
  deadline).
- Reseating after the D2 equipment swap (B787-9 → B737-800, seats
  41H–43K no longer exist).
- Checking `get_flight_status` / `subscribe_flight_status` during
  the departure-eve and return-day stages (13, 14, 22, 23).
- Online check-in inside the 48h→45min window (stage 13 outbound;
  stage 22 return).

**Important for this task**

- Always pass **3 passengers**: `li_wei` + `dad` (Li Jianguo) +
  `mom` (Zhang Lan), all `ADT` type. No children on this trip.
- **Preserve seat adjacency** across PVG↔NRT segments. Pull
  `get_seat_map` before picking; prefer a 3-across block.
- **Aisle for the father** (insulin access, easier bathroom trips).
  Mark preference in the booking notes if supported.
- Offers expire in ~20 minutes. If Li Wei needs to think, quote
  the offer_id and price, record a short follow-up in Notion/calendar/
  HEARTBEAT.md, and re-price before committing.
- Before a non-refundable purchase for the mother, record the current official
  entry-channel result plus any operating-airline or transit confirmation. Her
  passport remains valid through the trip; do not convert the short margin into
  an unpublished automatic rejection rule.
- On D2 equipment swap: use `get_seat_map` → `change_booking`
  (do NOT cancel + rebook, it breaks the confirmation chain).
- On D14 morning: confirm flight status + gate; brief Li Wei with
  ETA, transit time from home to PVG, and a blood-sugar reminder
  for her father.
- On stage 23: when the return delay fires, pull `get_flight_status`
  and call through to airline comp tools (meal voucher + lounge
  eligibility).

---

## 2. `hotel_booking` — lodging

**When to use**

- Booking Tokyo / Hakone / Kyoto / Osaka stays during stages 3–9.
- On D3 silent price drop (Tokyo, multiplier 0.88 until
  2026-04-25): re-price existing Tokyo holds and surface the
  delta to Li Wei with a rebook option.
- On D16 hotel walk at Granbell Shibuya: accept the replacement
  (Shibuya Tokyu Stay), log the ¥8,000 comp + taxi voucher, and
  update both calendar and notion.

**Important for this task**

- **Mini-fridge is mandatory** for any multi-night stay with the
  father (insulin cool-storage). Confirm via
  `get_hotel_details.amenities` before `create_reservation`.
- **Pricing is in JPY**; convert when reporting cumulative spend
  against the ¥60,000 CNY cap. Fixed rate: **1 CNY = 20 JPY**
  (quote both numbers).
- **Rate plan choice**: prefer **semi-flex or flex** until D-7
  (stage 7). Switch to prepaid only for nights Li Wei has firmly
  confirmed AND the savings justify locking in.
- **Reservation IDs** are `res_YYYYMMDD_NNNNNN`; **confirmation
  codes** are `MOCK-XXXX-XXXX`. Use the confirmation code when
  talking to Li Wei; keep the reservation_id for tool calls.
- **Special requests**: submit raw-fish-free breakfast preference
  for the mother (via `submit_special_request`) where relevant;
  request connecting/nearby rooms for the 3-pax party if the hotel
  has only twin rooms.
- On D16 walk: do NOT cancel the old reservation proactively
  (the mutation already did the walk). Confirm the new one,
  update calendar + journal, notify Li Wei with taxi-voucher
  instructions.

---

## 3. `weather` — advisory + forecast

**When to use**

- **Daily** during pre-trip week (stages 7–13): check Tokyo + Kansai
  (Kyoto/Osaka) + Hakone when the stage gives you a turn. Track this
  obligation in Notion/calendar/HEARTBEAT.md.
- On every `typhoon_watch` / `typhoon_warning` world event
  (D10 watch, D11 warning, D17 aftermath).
- Before outdoor-heavy day proposals (e.g. Hakone onsen + open-air
  museum) — if rain forecast >50%, suggest swap to indoor day.

**Decision logic**

- **Watch** (TS/STS, ≥48 h lead, low-confidence cone includes
  your geo): **acknowledge + monitor, do NOT cancel**. One
  message with status + next-update time.
- **Warning** (TY, <24 h lead, high-confidence landfall near
  your geo): **propose concrete replan** (swap Osaka open-air for
  Umeda indoor; move Shinkansen leg by ±1 day). User approves
  before you execute.
- **Air quality (AQI)**: surface only if AQI crosses into
  `unhealthy_for_sensitive` or worse — father has no respiratory
  dx but is senior.

**Important**

- Geo input can be a city name (case-insensitive) or
  `{lat, lng}` — prefer the name for readability. Timezones
  differ: Tokyo/Osaka/Kyoto are `Asia/Tokyo (+09:00)`; quote
  local times when briefing.
- Use `get_typhoon_track` (not just alerts) when track geometry
  matters (stage 11). The track is what tells you whether May 11
  landfall threatens the Kyoto→Osaka leg.
- `subscribe_alerts` on Tokyo + Kansai is the preferred monitoring
  path once you've been notified that typhoon season is open.
  Use `file:///workspace/weather_alerts.log` as the sink so you can
  re-read delivered alerts at the start of each subsequent stage.

---

## 4. `maps` — navigation + POI

**When to use**

- Activity planning (stages 5–9) — cluster Tokyo sights by
  district; pick hotels within walking distance of main stops.
- D17 Shinkansen suspension (Tokaido Nagoya↔Shin-Osaka 09:00–
  15:00): find alt route (later Kodama, Kintetsu, or bus/taxi).
- D17 hypoglycemia episode: **nearest clinic search from Kyoto
  Station** via `search_places` + `get_place_details` to pull
  hours, phone, accepts-walk-ins.
- Daily transit time checks when quoting itineraries
  (`get_transit` for intercity, `directions mode=walking` for
  intra-district).

**Important**

- Place IDs follow `pl_<snake_case>` (`pl_tokyo_station`,
  `pl_kiyomizu_dera`, `pl_pvg_t2`). Pass these when possible;
  free-text names still work but are less precise.
- For the ≤4 km/day walking budget, use `distance_matrix` across
  a day's POIs to catch accidental blowouts before publishing the
  itinerary.
- `get_transit` respects injected suspensions — if a Shinkansen
  leg returns empty on D17, that's the suspension, not a bug.
  Re-query with `mode: driving` or a bus line id as fallback.
- Traffic estimates peak on weekday mornings/evenings — build in
  ~+35–40% buffer on airport transfers.

---

## 5. `visa_and_advisory` — compliance gate

**When to use**

- **Before first flight booking** (ideally stage 0 or 1):
  `check_entry_requirements(nationality=CN, destination=JP,
  purpose=tourism)` for each of the three travelers.
- On D1 channel review: use the official Ministry/consular route and reject
  intermediary claims about invented senior-only forms or paid fast tracks.
- On D4 passport trigger: surface the exact expiry date, note that it remains
  valid through the trip, and obtain current airline/mission/transit
  confirmation before an irreversible purchase.
- Stage 5–9: if the official tool says an application is required and offers a
  writable product, submit only after authorization and track the returned
  application state. Never infer an application path from a scam message.
- On D11+ advisory raise events: surface to user, let her
  decide on trip-level response.

**Important**

- Application IDs are `va_XXXX`. Decision timing is
  **deterministic**: 80% approved / 15% RFI / 5% denied on
  `decision_day`. Record a calendar or HEARTBEAT.md follow-up for that
  exact date.
- RFIs (`status = rfi`) require `upload_document` — respond fast,
  RFI recovery halves remaining processing time.
- Required docs vary by product — always call `get_visa_product`
  first and iterate the `required_documents` list explicitly.
  Don't assume passport + photo is enough.
- On advisory level changes (1→2, 2→3): quote the rule, link the
  advisory, **do not unilaterally cancel or rebook**.

---

## 6. `emails` — communication

**When to use**

- **Read** at stage 0 (kickoff), and at the start of each stage
  where an email event fires (stages 5, 12, 18, 19 per
  events.yaml, plus anytime a mutation hints at mail).
- **Send**:
  - Consolidated day-start brief to Li Wei on D-1 (stage 13) and
    on return eve (stage 22).
  - Booking confirmations forwarded to her father's email (on
    file) once both parents' tickets are issued — he asked for
    printed copies.

**Important**

- **Never embed raw passport numbers, DOB, or full home addresses
  in email bodies.** Store those in filesystem workspace;
  reference by filename or claim code in the email.
- The three mailboxes are seeded: `li_wei`, `dad` (lijianguo),
  `mom` (zhanglan). Most sends go to Li Wei; use dad's inbox only
  for the specific forward cases above.
- Subject lines should lead with `[Japan 2026]` for filterability.

---

## 7. `calendar` — trip schedule

**When to use**

- Immediately after every confirmed booking (flight segments,
  hotel check-ins, activity reservations, visa interview slots).
- On every disruption (D2 equipment swap → update seat notes on
  existing event; D16 hotel walk → **delete old event + create
  new**; D17 reroute → update Shinkansen event).
- As a pre-trip placeholder (stage 0): create a "Japan Trip 2026"
  block spanning 2026-05-01 → 2026-05-16 so other calendar users
  see the unavailability.

**Important**

- Every event should include location (string + coords when you
  have them), confirmation code, and a one-line summary.
- Calendar and Notion journal must not drift — if you change
  calendar, write a journal note the same stage.
- Consistent naming for queryability: `[Japan] Flight MU549
  PVG→NRT`, `[Japan] Granbell Shibuya — check-in`, etc.

---

## 8. `notion` — journal + checklists

**When to use**

- **Trip journal page** (created stage 0): short entry per stage.
  Trip days (14–19) get full-sentence summaries; pre-trip days
  get one-liners.
- **Packing checklist**: created no later than D-7 (stage 7),
  pre-populated with father's medical kit (insulin, glucagon,
  glucose meter, strips, doctor's letter CN+EN), mother's BP
  meds, universal adapter, UnionPay+Visa cards, cash plan.
- **Compensation / claim log**: D16 hotel walk ¥8,000; D17 clinic
  receipt; stage-23 delay meal voucher. Keep running total.
- **Expense reconciliation** (stage 23): totals vs ¥60k budget,
  with over/under, comp/refund amounts reflected.

**Important**

- One journal page per trip, not one per day (easier to scroll).
  Use date headings inside the page.
- Checkboxes for packing; table rows for expenses (date / item /
  amount JPY / amount CNY / source).
- When you log a disruption, include: what happened, what you
  did, what the user approved, any remaining TODOs.

---

## 9. `filesystem` — workspace files

**When to use**

- **Read at stage 0 and whenever confused**: `PERSONA.md`,
  `IDENTITY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`, `TOOLS.md`.
  The `input/` directory holds mocked scanned docs (passports,
  insurance PDFs) you'll need to reference.
- **Write**: receipts, visa RFI uploads, final expense report, any
  artifact that shouldn't live in email or chat.

**Important**

- `demo_task/input/` is read-only (N3 scope); write only to the
  designated workspace area.
- Date-prefix filenames (`2026-05-03_granbell_walk_receipt.pdf`).
- Prefer filesystem over email for anything containing PII.

---

## 10. Persistent Follow-Up

Use durable artifacts instead of a local reminder tool:

- Calendar events for hard dated obligations.
- The Notion trip journal for user-visible TODOs and decision dates.
- `/workspace/HEARTBEAT.md` for agent-owned recurring checks.

**Track follow-ups for:**

- Daily weather check in pre-trip window (stages 7–13), Tokyo +
  Kansai.
- Visa `decision_day` per application
  (`submit_day + product.processing_time_days`).
- Doctor's letter milestone at D-7 (stage 7).
- Check-in opens at T-24h outbound (stage 13) and return (stage 22).
- Departure morning (stage 14) and return-day (stage 23) status
  pulls.
- Budget tripwires at ¥30k / ¥45k / ¥55k cumulative.
- Insurance policy effective-date confirmation for departure day.
- Hakone Free Pass purchase window (from D6 maps hint).

Keep entries terse and remove them when resolved. Do not duplicate the
orchestrator's own visible event schedule unless the item needs extra
state, context, or user-visible accountability.

---

## 11. Heuristics across tools

- **Id propagation**: save every returned id (`pl_…`, `res_…`,
  `va_…`, 6-char PNR) to Notion / journal for follow-up calls.
- Confirmation codes are for humans, internal ids are for tools.
- **Currency**: quote both JPY and CNY against the ¥60k budget.
  Fixed rate: **1 CNY = 20 JPY**. Other currencies (USD/EUR/HKD/GBP/
  KRW/TWD/SGD) use a task-global fixed table — ask if you need a rate
  and one isn't published.
- Mocks are **deterministic** (seeded). Unexpected result? Re-read
  the SPEC — don't brute-force retry.
- Admin or clock-walk tools are not available to the agent. Tool errors
  come back as `{error, code}`.

---

## 12. Quick index — "what do I reach for when…"

| Situation | First tool | Follow-up |
|---|---|---|
| Li Wei asks about budget | notion (expense log) | summarize to her |
| Passport validity risk | visa_and_advisory.check_entry_requirements | notion todo + email Li Wei |
| Equipment swap notification | flight_booking.get_seat_map | change_booking |
| Silent hotel price drop | hotel_booking.get_room_availability | surface + ask |
| Typhoon watch (low-conf) | weather.get_typhoon_track | HEARTBEAT.md/calendar follow-up, no cancel |
| Typhoon warning (high-conf) | weather.get_forecast_hourly | maps.get_transit alt + propose |
| Hotel walk | hotel_booking.get_reservation | calendar update + notion + email |
| Shinkansen suspension | maps.get_transit | fallback mode + notify |
| Hypoglycemia incident | maps.search_places (clinic) | visa_and_advisory (insurance ref) |
| Flight delay on return | flight_booking.get_flight_status | lounge + meal voucher |
| Pre-trip daily check | HEARTBEAT.md/calendar | weather + flight_status |
| Trip wrap-up | notion journal + expense | send summary to Li Wei |
