-- Reviewed neutral hotel inventory: 25 properties and 75 rate-plan rows.
INSERT INTO hotels(hotel_id,name,city,district,geo_lat,geo_lng,star_rating,user_rating,user_rating_count,amenities_json,address_json,policies_json,description,capacity_estimate) VALUES
 ('hotel_guayaquil_aero','Terminal Garden Guayaquil','Guayaquil','Airport',-2.155,-79.884,4,8.6,760,'["airport_shuttle","quiet_rooms","24h_front_desk"]','{"street":"Avenida de las Americas 410"}','{"cancellation_default":"listed_by_rate","night_transfer":"covered_walkway"}','Flexible airport hotel with staffed overnight access and a short terminal transfer.',120),
 ('hotel_quito_terminal','Quito Terminal Courtyard','Quito','Airport',-0.129,-78.357,4,8.4,620,'["airport_shuttle","24h_front_desk","late_meals"]','{"street":"Conector Alpachaca 82"}','{"cancellation_default":"listed_by_rate","weather_rebooking":"supported"}','Airport property with dependable disruption handling and pre-arranged pickup.',100),
 ('hotel_jardin_tranquilo','Jardin Tranquilo','Puerto Ayora','Workshop West',-0.744,-90.315,4,9.0,350,'["quiet_rooms","laundry","garden","walkable"]','{"street":"Calle Petrel 17"}','{"distance_to_workshop_km":1.1,"deposit_usd":180}','Quiet garden-side rooms within walking distance of the workshop venue.',35),
 ('hotel_malecon_central','Malecon Central Rooms','Puerto Ayora','Pier',-0.742,-90.311,4,8.3,290,'["restaurant","luggage_storage","pier_access"]','{"street":"Avenida Charles Darwin 51"}','{"distance_to_workshop_km":0.4,"night_activity":"moderate"}','Very close to the venue, but pier activity continues late and prepaid rates are strict.',28),
 ('hotel_cerro_verde','Cerro Verde Eco Lodge','Puerto Ayora','Highlands',-0.683,-90.340,3,8.7,120,'["quiet_rooms","nature","limited_shuttle"]','{"street":"Via Bellavista km 8"}','{"distance_to_workshop_km":12.5,"shuttle":"limited_schedule"}','Calm highland lodging that depends on scheduled transfers for workshop mornings.',22);

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<20)
INSERT INTO hotels(hotel_id,name,city,district,geo_lat,geo_lng,star_rating,user_rating,user_rating_count,amenities_json,address_json,policies_json,description,capacity_estimate)
SELECT printf('hotel_ec_%02d',n),
       CASE n WHEN 1 THEN 'Rio Guayas Business Hotel' WHEN 2 THEN 'Kennedy Norte Suites' WHEN 3 THEN 'Quito Airport Rest House' WHEN 4 THEN 'Tababela Morning Inn' WHEN 5 THEN 'Santa Cruz Bay Rooms' WHEN 6 THEN 'Pelican Walk Hotel' WHEN 7 THEN 'Darwin Avenue Guesthouse' WHEN 8 THEN 'Bellavista Family Lodge' WHEN 9 THEN 'Baltra Transit Rooms' WHEN 10 THEN 'Guayaquil Riverside Stay' WHEN 11 THEN 'Quito Historic Patio' WHEN 12 THEN 'Puerto Ayora Library Hotel' WHEN 13 THEN 'Tortuga Bay Approach Inn' WHEN 14 THEN 'Academy Bay Courtyard' WHEN 15 THEN 'Isabela Connector Lodge' WHEN 16 THEN 'San Cristobal Port Rooms' WHEN 17 THEN 'Guayaquil Early Flight Hotel' WHEN 18 THEN 'Quito Highland Transfer Inn' WHEN 19 THEN 'Santa Cruz Quiet House' ELSE 'Puerto Ayora Market Rooms' END,
       CASE WHEN n IN (1,2,10,17) THEN 'Guayaquil' WHEN n IN (3,4,11,18) THEN 'Quito' WHEN n=9 THEN 'Baltra' WHEN n=15 THEN 'Isabela' WHEN n=16 THEN 'San Cristobal' ELSE 'Puerto Ayora' END,
       CASE n%7 WHEN 0 THEN 'Waterfront' WHEN 1 THEN 'Airport' WHEN 2 THEN 'Centro' WHEN 3 THEN 'Residential' WHEN 4 THEN 'Highlands' WHEN 5 THEN 'Market' ELSE 'Workshop East' END,
       -2.20+n*0.08,-79.95-n*0.41,3+(n%3),7.7+(n%12)*0.1,90+n*17,
       CASE n%4 WHEN 0 THEN '["wifi","breakfast","laundry"]' WHEN 1 THEN '["wifi","airport_shuttle","late_checkin"]' WHEN 2 THEN '["wifi","quiet_rooms","luggage_storage"]' ELSE '["wifi","family_room","garden"]' END,
       printf('{"street":"Ecuador service road %d"}',100+n),
       CASE n%3 WHEN 0 THEN '{"deposit":"cash_or_card","arrival":"call_ahead"}' WHEN 1 THEN '{"deposit":"card","quiet_hours":"22:00-07:00"}' ELSE '{"deposit":"none","stairs":"check_before_booking"}' END,
       CASE n%10 WHEN 0 THEN 'Near a mainland airport with a staffed desk for late international arrivals.' WHEN 1 THEN 'Residential setting with low night traffic and limited nearby dining.' WHEN 2 THEN 'Convenient for the venue, though ground-floor rooms should be requested early.' WHEN 3 THEN 'Reliable luggage storage and clear taxi pickup instructions at reception.' WHEN 4 THEN 'Breakfast starts early enough for the first domestic flight bank.' WHEN 5 THEN 'Shared courtyard is quiet, while upper floors require stair access.' WHEN 6 THEN 'Close to shops and pharmacies but exposed to daytime street activity.' WHEN 7 THEN 'Transfer-dependent option with a fixed morning shuttle timetable.' WHEN 8 THEN 'Flexible arrival desk and written cancellation confirmation on request.' ELSE 'Simple rooms suited to short stays, with deposits settled at check-out.' END,
       24+n*3
FROM seq;

WITH RECURSIVE days(n) AS (SELECT 0 UNION ALL SELECT n+1 FROM days WHERE n<3),
hotels(hotel_id,base) AS (VALUES('hotel_guayaquil_aero',175),('hotel_quito_terminal',205))
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT hotel_id,strftime('%Y-%m-%d','2026-08-14','+'||n||' days'),'double_or_twin','flex',base+n*7,'USD',4+(n%3),8,'Free cancellation until 18:00 local on the listed date',strftime('%Y-%m-%dT18:00:00-05:00','2026-08-14','+'||n||' days'),1,2
FROM days CROSS JOIN hotels;

WITH RECURSIVE days(n) AS (SELECT 0 UNION ALL SELECT n+1 FROM days WHERE n<7),
hotels(hotel_id,flavor,base,breakfast) AS (VALUES('hotel_jardin_tranquilo','flex',225,0),('hotel_cerro_verde','flex',185,1),('hotel_malecon_central','prepaid',205,1))
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT hotel_id,strftime('%Y-%m-%d','2026-08-16','+'||n||' days'),'garden_double',flavor,base+(n%3)*8,'USD',CASE hotel_id WHEN 'hotel_jardin_tranquilo' THEN 7 WHEN 'hotel_cerro_verde' THEN 4 ELSE 3 END,9,
       CASE flavor WHEN 'flex' THEN 'Free cancellation until 18:00 local two days before arrival' ELSE 'Non-refundable after booking confirmation' END,
       CASE flavor WHEN 'flex' THEN strftime('%Y-%m-%dT18:00:00-06:00','2026-08-14','+'||n||' days') ELSE NULL END,breakfast,2
FROM days CROSS JOIN hotels;

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<40)
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy)
SELECT printf('hotel_ec_%02d',((n-1)%20)+1),CASE WHEN n<=20 THEN '2026-08-15' ELSE '2026-08-16' END,
       CASE n%4 WHEN 0 THEN 'twin' WHEN 1 THEN 'double' WHEN 2 THEN 'family' ELSE 'single' END,
       CASE n%3 WHEN 0 THEN 'semi' WHEN 1 THEN 'flex' ELSE 'prepaid' END,95+(n%14)*13,'USD',2+(n%6),8,
       CASE n%3 WHEN 0 THEN 'One-night fee after noon on arrival eve' WHEN 1 THEN 'Free cancellation through the stated local deadline' ELSE 'Non-refundable after booking confirmation' END,
       CASE n%3 WHEN 2 THEN NULL ELSE (CASE WHEN n<=20 THEN '2026-08-14T18:00:00-05:00' ELSE '2026-08-15T18:00:00-06:00' END) END,
       n%2,CASE n%4 WHEN 2 THEN 3 ELSE 2 END
FROM seq;
INSERT INTO rate_plans(hotel_id,date,room_type,flavor,nightly_price,currency,inventory_remaining,inventory_capacity,cancellation_policy,refundable_until,breakfast_included,max_occupancy) VALUES
 ('hotel_ec_01','2026-08-17','double','flex',168,'USD',3,8,'Free cancellation through the stated local deadline','2026-08-16T18:00:00-05:00',1,2),
 ('hotel_ec_02','2026-08-17','twin','semi',151,'USD',2,6,'One-night fee after noon on arrival eve','2026-08-16T12:00:00-05:00',0,2),
 ('hotel_ec_03','2026-08-17','single','prepaid',119,'USD',4,9,'Non-refundable after booking confirmation',NULL,1,1);
