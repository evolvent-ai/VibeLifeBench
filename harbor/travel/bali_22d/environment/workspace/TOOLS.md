# Tool Usage -- Bali 22-Day Trip Cheat Sheet

9 services available:
- `flight_booking`, `hotel_booking`, `weather`, `maps`,
  `visa_and_advisory` (travel mocks)
- `emails`, `calendar`, `filesystem`, `notion` (reused)

No local reminder helper; persist follow-ups in Notion/calendar/workspace.

---

## 1. `flight_booking` -- core booking

**When to use**
- Searching PVG<->DPS fares for couple (stage 0-9) and mother's
  solo segment PVG->DPS on 6/22.
- Reseating after D2 equipment swap (A330 -> B738).
- Checking flight status on departure (stage 13) and return (stage 22-23).
- Online check-in (stage 12 outbound, stage 22 return).

**Important**
- Couple segment: 2 pax (chen_yu + wang_meilin), both ADT.
- Mother segment: 1 pax (liu_fang), ADT, separate booking.
- **Aisle seat for pregnant wife** (easier bathroom access).
- **Do not book mother's segment** until passport issue resolved.
- On equipment swap: use `get_seat_map` -> `change_booking`.
- Pregnant traveler: request bulkhead/extra legroom if available.
- On return delay (stage 23): pull status + comp (meal voucher + lounge).

---

## 2. `hotel_booking` -- lodging

**When to use**
- Booking Seminyak (days 1-5), Ubud (days 6-12), and coastal
  (days 13-22) stays.
- On D14 mold issue: request room change or property relocation.

**Important**
- **AC + good ventilation mandatory** (mold risk for pregnant woman,
  humidity worsens mother's RA).
- **Ground floor or elevator access** for mother (no steep stairs).
- **Within 30 min of BIMC Kuta or Siloam Bali** for pregnancy emergency.
- Pricing in IDR; convert at **1 CNY = 2,200 IDR**.
- Prefer **flex rate** until D-7; prepaid only if confirmed + savings justify.
- On mold issue: accept upgrade/relocation, log in journal + calendar.

---

## 3. `weather` -- advisory + forecast + volcanic monitoring

**When to use**
- Daily pre-trip check (stages 8-12): Bali forecast.
- Volcanic monitoring: `get_alerts` for Agung status.
- Storm tracking (stages 17-18): heavy rain impact on Ubud.
- Ash drift monitoring pre-return (stage 22).

**Decision logic**
- **Volcano Level 2 (Waspada)**: acknowledge, monitor. Do NOT cancel
  northern leg yet.
- **Volcano Level 3 (Siaga)**: Kintamani closed. Propose alt (Ubud
  activities, south coast). DPS airport -- monitor ash drift.
- **Heavy rain**: swap outdoor for indoor activities; check road closures.

---

## 4. `maps` -- navigation + POI

**When to use**
- Activity planning: cluster sites by region.
- Check distances (mother's 3 km/day limit).
- Hospital search: BIMC Kuta, Siloam Bali for OB/GYN.
- Alternative routes during flooding/road closures.

**Important**
- Tegallalang: 200+ steep stairs -- NOT suitable for mother.
  Use Ceking Rice Terrace (flat access) instead.
- Distance matrix for daily walking budget.
- Local transit: Grab/Gojek car preferred over walking for mother.

---

## 5. `visa_and_advisory` -- compliance

**When to use**
- Check entry requirements for all 3 travelers.
- Flag mother's passport validity issue.
- Monitor Zika advisory status.
- VOA fee tracking (IDR 500,000/person).

**Important**
- Indonesia VOA: 30 days, IDR 500,000/person.
- Passport must have >= 6 months validity from entry.
- Mother's passport fails this check -- must be surfaced immediately.
- Zika advisory: present facts to user, do NOT make go/no-go decision.

---

## 6. `emails` -- communication

**When to use**
- Read confirmations (stage 11).
- Send consolidated briefs on departure eve (stage 12) and return (stage 22).

**Important**
- Never embed passport/ID numbers in email body.
- Subject: `[Bali 2026] <topic>`.

---

## 7. `calendar` -- trip schedule

**When to use**
- After every confirmed booking.
- On every disruption (mold, volcano, storm, delay).
- Pre-trip placeholder at stage 0.

---

## 8. `notion` -- journal + checklists

**When to use**
- Trip journal: entry per stage.
- Packing checklist (by D-7).
- Expense reconciliation (stage 23).

---

## 9. `filesystem` -- workspace files

**When to use**
- Read persona files at stage 0.
- Write receipts, reports, artifacts.
- Maintain HEARTBEAT.md.

---

## Quick index

| Situation | First tool | Follow-up |
|---|---|---|
| Budget question | notion (expense log) | summarize |
| Passport validity | visa_and_advisory.check_entry_requirements | notion + alert user |
| Equipment swap | flight_booking.get_seat_map | change_booking |
| Zika advisory | visa_and_advisory + WHO info | surface to user |
| Volcano watch | weather.get_alerts | HEARTBEAT follow-up |
| Volcano warning | weather + maps | propose alt itinerary |
| Hotel mold | hotel_booking.get_reservation | request change + journal |
| Heavy rain/flood | weather + maps | indoor alternatives |
| Pregnancy concern | maps.search_places (hospital) | surface info only |
| Flight delay | flight_booking.get_flight_status | lounge + meal voucher |
| Mother arrives | flight_booking + maps (airport pickup) | brief + journal |
