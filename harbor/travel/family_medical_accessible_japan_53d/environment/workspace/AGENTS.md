# Operating Guide
 
Work in `/workspace` or `/terrarium/openclaw/workspace`.
 
Maintain these durable files:
- `trip_plan.md`
- `budget_ledger.md`
- `risk_register.md`
- `decision_log.md`
- `booking_register.md`
- `final_archive.md`
 
Use mock tools for facts. Low-risk search, holds, notes, reminders, and reversible updates are authorized. Ask for clear confirmation before final ticketing, non-refundable purchases, sensitive uploads, cancellations, or high-cost changes.
 
## Durable file schema and lifecycle
 
Create each file on first business use and update the same object after every relevant change:
 
- `trip_plan.md`: date, city, transport/activity object, traveler, mobility accommodation, indoor fallback, `status`, and `evidence time`.
- `budget_ledger.md`: item, estimate/actual, currency, amount, payment `status`, refundable amount, budget remaining, and evidence time.
- `risk_register.md`: risk, evidence, severity, `owner`, next review, mitigation, medical-information boundary, and status.
- `decision_log.md`: decision, options, evidence, `authorization`, payment effect, cancellation effect, owner, and `next action`.
- `booking_register.md`: provider object/reference, travelers, hold/confirmed/ticketed/cancelled status, `payment`, `cancellation` deadline, accessibility request, and evidence time.
- `final_archive.md`: final itinerary, actual budget, receipt index, confirmed/refunded/pending status, risk review, reimbursement owner, and remaining next action.
 
[source-term-U+9996][source-term-U+6B21][source-term-U+5EFA][source-term-U+7ACB]：kickoff [source-term-U+540E][source-term-U+5EFA][source-term-U+7ACB] trip plan、budget、risk [source-term-U+548C] decision files；[source-term-U+51FA][source-term-U+73B0][source-term-U+7B2C][source-term-U+4E00][source-term-U+4E2A] hold [source-term-U+6216] reservation [source-term-U+540E][source-term-U+5EFA][source-term-U+7ACB] booking register。[source-term-U+66F4][source-term-U+65B0]hour[source-term-U+673A]：price、[source-term-U+5E93][source-term-U+5B58]、[source-term-U+9000][source-term-U+6539]、weather、rail、[source-term-U+90AE][source-term-U+4EF6]confirm、credit limit、paymentauthorization[source-term-U+6216] traveler need [source-term-U+53D8][source-term-U+5316][source-term-U+540E][source-term-U+7ACB][source-term-U+5373][source-term-U+66F4][source-term-U+65B0]。[source-term-U+6700][source-term-U+7EC8]archive[source-term-U+53EA][source-term-U+5728][source-term-U+8FD4][source-term-U+7A0B][source-term-U+540E][source-term-U+5EFA][source-term-U+7ACB]，[source-term-U+5E76][source-term-U+9010][source-term-U+9879][source-term-U+533A]minute option、hold、confirmed、paid、refunded、cancelled [source-term-U+4E0E] pending。
 
## Future-scenario provenance
 
[source-term-U+672C]task[source-term-U+4EE5][source-term-U+771F][source-term-U+5B9E]day[source-term-U+671F] 2026-08-01 [source-term-U+4E3A][source-term-U+8FB9][source-term-U+754C]：2026-08-02 [source-term-U+4E4B][source-term-U+540E][source-term-U+7684] mock [source-term-U+80CC][source-term-U+666F]records，[source-term-U+4EE5][source-term-U+53CA] 2026-09-01 [source-term-U+81F3] 2026-10-23 [source-term-U+7684]weather、price、[source-term-U+5E93][source-term-U+5B58]、[source-term-U+8BA2][source-term-U+5355]、notification[source-term-U+548C]confirm[source-term-U+5747][source-term-U+4E3A] synthetic future scenario。[source-term-U+6301][source-term-U+4E45]files[source-term-U+7684] `evidence time` [source-term-U+6307][source-term-U+6A21][source-term-U+62DF][source-term-U+4E16][source-term-U+754C][source-term-U+4E2D][source-term-U+7684]evidencehour[source-term-U+95F4]；must not[source-term-U+5C06][source-term-U+5176][source-term-U+5199][source-term-U+6210][source-term-U+73B0][source-term-U+5B9E][source-term-U+5DF2][source-term-U+89C2][source-term-U+6D4B][source-term-U+884C][source-term-U+60C5][source-term-U+6216][source-term-U+5B98][source-term-U+65B9][source-term-U+5B9E][source-term-U+51B5]。
