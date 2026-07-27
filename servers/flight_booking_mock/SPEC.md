# flight-booking-mock — SPEC

Local mock of an Amadeus-flavored flight booking service. All state lives
in a single SQLite file under the env directory; servers do not have a
"today" — date-keyed rows are queried by literal date supplied by the
agent.

## 1. Boot contract

```bash
flight-booking-mock --host 0.0.0.0 --port 8000 --env <abs path to env dir>
```

On cold start the server deletes `<env>/runtime.db` (and its sidecars),
recreates the schema, executes `<env>/init.sql` if present, then opens
streamable-HTTP on `/mcp`. Every start is a fresh DB.

## 2. Agent-facing tools

| tool                       | summary                                          |
| -------------------------- | ------------------------------------------------ |
| `search_flights`           | offers for a route on a date (or round-trip)     |
| `get_flight_offer`         | re-fetch an offer's full fare rules + segments   |
| `get_seat_map`             | seat map for an offer or booking segment         |
| `price_offer`              | re-price an offer against current bucket prices  |
| `create_booking`           | ticket / hold a PNR                              |
| `get_booking`              | fetch a PNR                                      |
| `list_bookings`            | list PNRs for a user/email                       |
| `cancel_booking`           | cancel a PNR                                     |
| `change_booking`           | exchange segments for a new offer                |
| `check_in`                 | online check-in                                  |
| `get_flight_status`        | live flight status                               |
| `subscribe_flight_status`  | push subscription (local notifications table)    |

There are no admin tools. There is no clock-advancement surface.
Stage-to-stage world changes are delivered by the task orchestrator writing
directly to `runtime.db` via `event.yaml` mutation events.

## 3. Determinism

* No `random.Random` anywhere — IDs come from a sequence counter
  (`_counters` table) plus content hashes.
* Same query → same result. There is no per-search variation.
* IDs:
  * PNR: 6 chars from `_PNR_ALPHABET` indexed by sha256 bytes seeded with
    `pnr_seq` counter + caller-supplied seed.
  * Offer: `ofr_<14 hex of sha256>`.
  * Subscription: `sub_<10 hex>`.
  * Boarding pass: `BP<8 hex upper>`.
  * Ticket number: `172-<9 digits derived from sha256>`.
  * Search id: `srch_<8 hex>`.

## 4. Schema

```sql
flights(flight_no, origin, dest, depart_dt, arrive_dt, equipment,
        base_price, currency, carrier, PK (flight_no, depart_dt));
fare_buckets(flight_no, date, cabin, price, seats_remaining,
             PK (flight_no, date, cabin));
offers(offer_id PK, created_at, expires_at, payload_json,
       priced_price, priced_at, price_guarantee_until);
bookings(pnr PK, user_id, offer_id, status, paid_amount, currency,
         created_at, segments_json, passengers_json, contact_json,
         history_json);
seat_assignments(pnr, segment_idx, pax_idx, seat, checked_in,
                 boarding_pass_id, PK (pnr, segment_idx, pax_idx));
flight_status(flight_no, date, status, actual_depart, actual_arrive,
              gate, terminal, delay_min, last_updated,
              PK (flight_no, date));
status_subscriptions(sub_id PK, flight_no, date, sink, webhook_url,
                     created_at);
notifications(id PK autoinc, created_at, channel, payload_json);
_counters(name PK, value);
```

`offers` has a TTL (20 min) and `expires_at`. The price-guarantee window
is 10 min after `price_offer` runs. These windows use real wall-clock
time; the orchestrator runs stages back-to-back so the windows never
fire in normal use.

## 5. Error codes (subset)

| code                        | thrown when                                         |
| --------------------------- | --------------------------------------------------- |
| `flight_not_found`          | unknown `flight_no` / no row for that date          |
| `offer_not_found`           | unknown `offer_id`                                  |
| `inventory_gone`            | seats_remaining < pax_count                         |
| `seat_unavailable`          | seat label not in layout / already taken            |
| `booking_not_found`         | unknown PNR                                         |
| `already_cancelled`         | re-cancelling a CANCELLED booking                   |
| `payment_declined_mock`     | `payment.card_last4 == "0000"` (rigged decline)     |
| `non_changeable_fare`       | old offer's `fare_rules.changeable` is false        |
| `flight_cancelled`          | check-in against a CANCELLED flight                 |
| `invalid_sink`              | `sink` not in `{stdout, email, webhook}`            |
