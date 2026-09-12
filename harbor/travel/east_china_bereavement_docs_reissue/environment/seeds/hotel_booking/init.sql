-- Reviewed Stage 0 lodging inventory: 20 properties and 50 rate-plan rows.
INSERT INTO hotels(hotel_id,name,city,district,geo_lat,geo_lng,star_rating,user_rating,user_rating_count,amenities_json,address_json,policies_json,description,capacity_estimate) VALUES
 ('hotel_suz_mourning_nearby','Suzhou Jing’an Residence','Suzhou','Wuzhong',31.260,120.630,4,8.8,220,'["wifi","breakfast","elevator","quiet_room"]','{"street":"Baodai West Road18scenario text"}','{"front_desk":"24h","deposit":"card","smoking":"designated_only"}','scenario textServicescenario text，scenario textelderscenario text。',50);

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<19)
INSERT INTO hotels(hotel_id,name,city,district,geo_lat,geo_lng,star_rating,user_rating,user_rating_count,amenities_json,address_json,policies_json,description,capacity_estimate)
SELECT printf('hotel_east_%02d',n),
       (CASE n%4 WHEN 0 THEN 'Beijingscenario text' WHEN 1 THEN 'Suzhouscenario text' WHEN 2 THEN 'Shanghaiscenario text' ELSE 'NingboHaishuscenario text' END)||printf('-%02d',n),
       CASE n%4 WHEN 0 THEN 'Beijing' WHEN 1 THEN 'Suzhou' WHEN 2 THEN 'Shanghai' ELSE 'Ningbo' END,
       CASE n%8 WHEN 0 THEN 'scenario text' WHEN 1 THEN 'Gusu' WHEN 2 THEN 'Jing’an' WHEN 3 THEN 'Haishu' WHEN 4 THEN 'Dongcheng' WHEN 5 THEN 'Wuzhong' WHEN 6 THEN 'Changning' ELSE 'Yinzhou' END,
       29.8+(n%8)*0.18,116.3+(n%9)*0.55,3+(n%3),7.6+(n%12)*0.1,80+n*13,
       CASE n%4 WHEN 0 THEN '["wifi","laundry","late_checkin"]' WHEN 1 THEN '["wifi","elevator","family_room"]' WHEN 2 THEN '["wifi","metro_access","luggage_storage"]' ELSE '["wifi","quiet_room","breakfast"]' END,
       printf('{"street":"%s%dscenario text"}',CASE n%4 WHEN 0 THEN 'Anzhen Road' WHEN 1 THEN 'Panmen Road' WHEN 2 THEN 'Wuding Road' ELSE 'Liuting Street' END,20+n),
       CASE n%3 WHEN 0 THEN '{"deposit":"cash_or_card","quiet_hours":"22:00-07:00"}' WHEN 1 THEN '{"deposit":"card","late_arrival":"call_front_desk"}' ELSE '{"deposit":"none","accessible_room":"on_request"}' END,
       CASE n%10 WHEN 0 THEN 'scenario text，scenario textroute。' WHEN 1 THEN 'scenario textelderscenario text，scenario text。' WHEN 2 THEN 'scenario text，scenario texttime。' WHEN 3 THEN 'scenario text，scenario text。' WHEN 4 THEN 'scenario text，scenario textservice windowscenario text。' WHEN 5 THEN 'familyscenario text，scenario text。' WHEN 6 THEN 'scenario text，scenario text。' WHEN 7 THEN 'scenario text，scenario text。' WHEN 8 THEN 'scenario text，scenario text。' ELSE 'scenario textplacesscenario text，scenario text。' END,
       30+n*2
FROM seq;

WITH dates(d) AS (VALUES('2026-04-05'),('2026-04-06'),('2026-04-07'),('2026-04-08')),
rooms(room_type,base_price) AS (VALUES('twin',730),('two_single',990),('quiet_double',690))
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT 'hotel_suz_mourning_nearby',d,room_type,'flex',base_price + CAST(substr(d,-2) AS INTEGER)*5,'CNY',4,8,'free_cancel_until_18_local',d||'T18:00:00+08:00',1,2
FROM dates CROSS JOIN rooms;

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<38)
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT printf('hotel_east_%02d',((n-1)%19)+1),
       CASE WHEN n<=19 THEN '2026-04-04' ELSE '2026-04-05' END,
       CASE n%4 WHEN 0 THEN 'twin' WHEN 1 THEN 'double' WHEN 2 THEN 'quiet_double' ELSE 'family' END,
       CASE n%3 WHEN 0 THEN 'semi' WHEN 1 THEN 'flex' ELSE 'prepaid' END,
       420+(n%13)*35,'CNY',2+(n%7),10,
       CASE n%3 WHEN 0 THEN 'one_night_fee_after_noon' WHEN 1 THEN 'free_cancel_until_18_local' ELSE 'nonrefundable_after_booking' END,
       CASE n%3 WHEN 2 THEN NULL ELSE (CASE WHEN n<=19 THEN '2026-04-04T18:00:00+08:00' ELSE '2026-04-05T18:00:00+08:00' END) END,
       CASE n%2 WHEN 0 THEN 1 ELSE 0 END,CASE n%4 WHEN 3 THEN 3 ELSE 2 END
FROM seq;

-- Shanghai window-day lodging (2026-04-09..2026-04-12).
-- The stage-7 world event tells the agent that refundable rooms near the
-- Shanghai ID window "scenario text", and the rubric requires an active
-- Shanghai reservation for the 04-11 appointment — but the inventory above
-- stops at 04-05, so no such room could ever be booked. These rows close that
-- gap for the Shanghai properties only; Suzhou/Beijing/Ningbo are untouched so
-- the elder-lodging price delta at 04-05..04-08 stays exactly as seeded.
WITH d(day) AS (VALUES('2026-04-09'),('2026-04-10'),('2026-04-11'),('2026-04-12')),
rooms(room_type,base_price) AS (VALUES('double',680),('quiet_double',720)),
sha(hotel_id) AS (SELECT hotel_id FROM hotels WHERE city = 'Shanghai')
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT sha.hotel_id, d.day, rooms.room_type, 'flex',
       rooms.base_price + CAST(substr(d.day,-2) AS INTEGER)*4, 'CNY',
       3, 10, 'free_cancel_until_18_local', d.day||'T18:00:00+08:00', 1, 2
FROM sha CROSS JOIN d CROSS JOIN rooms;

-- Ningbo arrival-day lodging (2026-04-16..2026-04-21).
-- The elder reaches Ningbo on D3135 at 19:46 on 04-16 and the return flight is
-- 04-21, and final_all_segments_closed requires an active Ningbo reservation,
-- but the seeded inventory stops at 04-05. Ningbo properties only.
WITH d(day) AS (VALUES('2026-04-16'),('2026-04-17'),('2026-04-18'),('2026-04-19'),('2026-04-20'),('2026-04-21')),
rooms(room_type,base_price) AS (VALUES('twin',560),('quiet_double',600)),
ngb(hotel_id) AS (SELECT hotel_id FROM hotels WHERE city = 'Ningbo')
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT ngb.hotel_id, d.day, rooms.room_type, 'flex',
       rooms.base_price + CAST(substr(d.day,-2) AS INTEGER)*3, 'CNY',
       3, 10, 'free_cancel_until_18_local', d.day||'T18:00:00+08:00', 1, 2
FROM ngb CROSS JOIN d CROSS JOIN rooms;
