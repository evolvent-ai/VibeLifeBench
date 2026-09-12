# flight_booking_mock — east_asia_group_trip_24d

## Key IDs

| Item | flight_id | flight_no |    | departure   (UTC) |
|------|-----------|-----------|------|---------------|
| **S10     ** | `flt_mu501_0605` | **MU501** | PVG→NRT | 2026-06-04T23:30Z |
| S10     A | `flt_nh912_0605` | NH912 | PVG→NRT | 2026-06-05T04:00Z |
| S10     B(  ) | `flt_ca836_0605`+`flt_ca183_0605` | CA836+CA183 | PVG→PEK→NRT | 06-05 |
| S10      | `flt_mu507_0606` | MU507 | PVG→NRT | 2026-06-05T23:30Z |
| **S14 check-in  ** | `flt_oz102_0608` | **OZ102** | NRT→ICN | 2026-06-08T01:00Z (**JST 10:00**) |
| Zhao Min     | `flt_mu504_0608` | MU504 | NRT→PVG | 2026-06-07T23:00Z |
|      | `flt_ke892_0610` | KE892 | ICN→PVG | 2026-06-10T00:30Z |

## S10 Mutation   

```sql
UPDATE flights SET status='cancelled'
WHERE flight_no='MU501' AND date='2026-06-05';
```

   ，agent    `get_flight_status('MU501','2026-06-05')`  return `status='cancelled'`，      booking status    。

## S14 Check-in     

OZ102    2026-06-08T01:00Z（JST 10:00）：
- check_in   : **2026-06-06T01:00Z**（T-48h）
- check_in deadline: **2026-06-08T00:15Z**（T-45min）
- S14       : 2026-06-06（UTC），      ✓

##     

|    |    |
|------|------|
| Shanghai(PVG) | CST = UTC+8 |
| Tokyo(NRT) | JST = UTC+9 |
| Seoul(ICN) | KST = UTC+9 |

## Schema（  ）

```sql
flights(flight_id, flight_no, airline, carrier_code, origin, destination,
        date, departure_time, arrival_time, duration_min, cabin, fare_class,
        price_minor, currency, available_seats, status, aircraft_type, codeshare)
bookings(pnr, flight_id, user_id, email, status, passengers, contact,
         seat_selections, created_at)
```

status  : `scheduled` / `cancelled` / `delayed`
