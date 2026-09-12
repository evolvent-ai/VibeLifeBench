# hotel-booking-mock — SPEC

Local mock of a hotel booking aggregator. All state lives in a single
SQLite file under the env directory; the server has no notion of "today"
— refundable windows compare against the wall-clock UTC date.

## 1. Boot contract

```bash
hotel-booking-mock --host 0.0.0.0 --port 8000 --env <abs path to env dir>
```

On cold start: delete `<env>/runtime.db` (and sidecars), recreate schema,
execute `<env>/init.sql` if present, open streamable-HTTP on `/mcp`.

## 2. Agent-facing tools

| tool                         | summary                                            |
| ---------------------------- | -------------------------------------------------- |
| `search_hotels`              | hotels in a city / geo for a stay window           |
| `get_hotel_details`          | full hotel profile                                 |
| `get_room_availability`      | per-room-type rate plans for the stay              |
| `create_reservation`         | book a rate_plan_id                                |
| `get_reservation`            | fetch a reservation                                |
| `list_reservations`          | list by user_id                                    |
| `modify_reservation`         | shift dates / change room type                     |
| `cancel_reservation`         | refund + penalty per fare flavor                   |
| `request_late_checkout`      | auto-approved if hotel below 85% occupancy         |
| `submit_special_request`     | open a request ticket                              |
| `get_user_bookings_summary`  | aggregate user stats                               |

There are no admin tools. There is no clock-advancement surface.
Stage-to-stage world changes (price shocks, walks, …) come from
orchestrator-applied mutations against `runtime.db`.

## 3. Determinism

* No `random.Random`.
* `reservation_id` = `res_<YYYYMMDD>_<NNNNNN>` where NNNNNN is bumped
  from the `_counters.reservation_seq` row.
* `confirmation_code` = `MOCK-AAAA-BBBB` derived from the first 8
  hex chars of `sha256(reservation_id)`.
* `ticket_id` = `tkt_<NNNNNN>` from `_counters.ticket_seq`.

## 4. Schema

```sql
hotels(hotel_id PK, name, city, district, geo_lat, geo_lng,
       star_rating, user_rating, user_rating_count,
       amenities_json, address_json, policies_json, description,
       capacity_estimate);
rate_plans(rate_plan_row_id PK autoinc, hotel_id, date, room_type,
           flavor, nightly_price, currency, inventory_remaining,
           inventory_capacity, cancellation_policy, refundable_until,
           breakfast_included, max_occupancy,
           UNIQUE (hotel_id, date, room_type, flavor));
reservations(reservation_id PK, confirmation_code UNIQUE, user_id,
             hotel_id, check_in, check_out, room_type, flavor, status,
             total_charged, currency, refundable, refundable_until,
             created_at, updated_at, guest_profile_json,
             payment_method_id, special_requests_json);
reservation_nights(id PK autoinc, reservation_id, date, rate_plan_row_id,
                   nightly_price);
special_requests(ticket_id PK, reservation_id, text, status,
                 created_at, updated_at);
notifications(id PK autoinc, created_at, channel, payload_json);
_counters(name PK, value);
```

## 5. Error codes (subset)

| code                          | thrown when                                        |
| ----------------------------- | -------------------------------------------------- |
| `HotelNotFoundError`          | unknown hotel_id                                   |
| `RatePlanNotFoundError`       | invalid / missing rate_plan_id                     |
| `ReservationNotFoundError`    | unknown reservation_id                             |
| `BadDateRangeError`           | invalid check_in/check_out                         |
| `SoldOutError`                | inventory_remaining <= 0 for some night            |
| `ModifyNoAvailabilityError`   | modify-target dates don't cover all nights         |
| `AlreadyCancelledError`       | cancel against already-cancelled reservation       |
| `UncancellableError`          | cancel against `checked_out` / `walked` state      |
| `BadArgError`                 | required fields missing on guest_profile etc.      |
