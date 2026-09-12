# hotel_booking_mock — east_asia_group_trip_24d

## Key IDs

| Item | hotel_id | rate_plan_id | Notes |
|------|----------|-------------|-------|
| **S12     ** | `htl_shinjuku_grand` | `rp_sg_ref` | Superior Twin，refundable  |
| Tokyo   A | `htl_shibuya_excel` | `rp_sb_ref` |   ，Superior Twin |
| Tokyo   B | `htl_asakusa_view` | `rp_av_ref` |   ，    |
| Tokyo      | `htl_ikebukuro_sun` | `rp_ik_nonref` |  refundable |
| Seoul    | `htl_myeongdong_plaza` | `rp_mp_ref` | Myeongdong，refundable  |
| Seoul    | `htl_hongdae_stay` | `rp_hd_ref` |   ，refundable  |

## S12 Mutation   

```sql
--  Shinjuku hotel Superior Twin      
UPDATE room_inventory SET available_count=0
WHERE hotel_id='htl_shinjuku_grand'
  AND room_type_id='rt_sg_superior'
  AND date IN ('2026-06-05','2026-06-06','2026-06-07');
```

   ，agent    `get_room_availability('htl_shinjuku_grand','2026-06-05','2026-06-08',2)`   Superior Twin    。  
Agent      hotel（  /  ）     。

##     

- Shinjuku Superior Twin: 5 / （mutation    0）
-    Superior Twin: 6 / （mutation    ）
-    Superior Double: 4 / 
- Myeongdong Superior Twin（Seoul）: 5 / 

##     

|   | check-in | check-out |   hotel |
|----|------|------|---------|
| Tokyo  | 2026-06-05 | 2026-06-08 | htl_shinjuku_grand → S12     |
| Seoul  | 2026-06-08 | 2026-06-10 | htl_myeongdong_plaza |

## Schema（  ）

```sql
hotels(hotel_id, name, city, country_code, star_rating, rating, address,
       description, lat, lng, amenities, check_in_time, check_out_time)
room_types(room_type_id, hotel_id, name, max_guests, beds, area_sqm, amenities)
rate_plans(rate_plan_id, hotel_id, room_type_id, flavor, base_rate_minor,
           currency, meal_plan, refund_deadline_h, description)
room_inventory(id, hotel_id, room_type_id, date, available_count)
reservations(reservation_id, rate_plan_id, user_id, status, check_in, check_out,
             guests, guest_profile, special_requests, total_minor, created_at)
```

flavor: `refundable` / `non_refundable`
