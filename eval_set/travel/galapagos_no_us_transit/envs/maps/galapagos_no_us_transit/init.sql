-- Reviewed neutral map corpus: 90 places, reviews, roads and transit records.
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
 ('place_pvg','Shanghai Pudong International Airport','airport',31.1443,121.8083,'CN','Shanghai',4.3,NULL,'{"daily":"00:00-24:00"}',NULL,NULL,'PVG'),
 ('place_hkg','Hong Kong International Airport','airport',22.3080,113.9185,'HK','Hong Kong',4.4,NULL,'{"daily":"00:00-24:00"}',NULL,NULL,'HKG'),
 ('place_mad','Adolfo Suarez Madrid-Barajas Airport','airport',40.4983,-3.5676,'ES','Madrid',4.2,NULL,'{"daily":"00:00-24:00"}',NULL,NULL,'MAD'),
 ('place_gye','Jose Joaquin de Olmedo Airport','airport',-2.1574,-79.8836,'EC','Guayaquil',4.1,NULL,'{"daily":"00:00-24:00"}',NULL,NULL,'GYE'),
 ('place_uio','Mariscal Sucre International Airport','airport',-0.1292,-78.3575,'EC','Quito',4.2,NULL,'{"daily":"00:00-24:00"}',NULL,NULL,'UIO'),
 ('place_gps','Seymour Airport Baltra','airport',-0.4538,-90.2659,'EC','Baltra',4.0,NULL,'{"daily":"06:00-18:00"}',NULL,NULL,'GPS'),
 ('place_itabaca_baltra','Itabaca Channel Baltra Dock','dock',-0.4850,-90.2550,'EC','Baltra',4.0,1,'{"daily":"06:00-18:30"}',NULL,NULL,'Baltra dock'),
 ('place_itabaca_santacruz','Itabaca Channel Santa Cruz Dock','dock',-0.4865,-90.2542,'EC','Santa Cruz',4.0,1,'{"daily":"06:00-18:30"}',NULL,NULL,'Santa Cruz dock'),
 ('place_puerto_ayora_bus','Puerto Ayora Bus Terminal','bus_station',-0.7398,-90.3180,'EC','Puerto Ayora',4.1,1,'{"daily":"05:30-21:00"}',NULL,NULL,'Puerto Ayora bus terminal'),
 ('place_workshop_venue','Puerto Ayora Marine Data Lab','venue',-0.7450,-90.3140,'EC','Puerto Ayora',4.7,NULL,'{"workshop":"08:00-18:00"}',NULL,NULL,'Avenida Charles Darwin 102'),
 ('place_jardin_tranquilo','Jardin Tranquilo','hotel',-0.7440,-90.3150,'EC','Puerto Ayora',4.6,3,'{"front_desk":"24h"}',NULL,NULL,'Calle Petrel 17'),
 ('place_puerto_clinic','Santa Cruz Community Clinic','clinic',-0.7425,-90.3165,'EC','Puerto Ayora',4.2,1,'{"weekday":"07:00-20:00"}',NULL,NULL,'Puerto Ayora clinic');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<18)
INSERT INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted)
SELECT printf('place_ec_%02d',n),
       CASE n WHEN 1 THEN 'Guayaquil Airport Bus Stop' WHEN 2 THEN 'Terminal Garden Footbridge' WHEN 3 THEN 'Quito Airport Taxi Desk' WHEN 4 THEN 'Tababela Pharmacy' WHEN 5 THEN 'Baltra Airport Shuttle Bay' WHEN 6 THEN 'Santa Cruz Highlands Junction' WHEN 7 THEN 'Bellavista Shared Taxi Stand' WHEN 8 THEN 'Puerto Ayora Municipal Pier' WHEN 9 THEN 'Charles Darwin Research Station' WHEN 10 THEN 'Puerto Ayora Central Pharmacy' WHEN 11 THEN 'Academy Bay Cash Point' WHEN 12 THEN 'Tortuga Bay Trailhead' WHEN 13 THEN 'Puerto Ayora Market' WHEN 14 THEN 'San Cristobal Ferry Office' WHEN 15 THEN 'Isabela Public Dock' WHEN 16 THEN 'Guayaquil Airport Clinic' WHEN 17 THEN 'Quito Baggage Service Desk' ELSE 'Puerto Ayora Police Post' END,
       CASE n%7 WHEN 0 THEN 'dock' WHEN 1 THEN 'bus_station' WHEN 2 THEN 'hotel' WHEN 3 THEN 'taxi' WHEN 4 THEN 'pharmacy' WHEN 5 THEN 'attraction' ELSE 'service' END,
       -2.2+n*0.09,-79.9-n*0.52,'EC',CASE WHEN n<=2 OR n=16 THEN 'Guayaquil' WHEN n<=4 OR n=17 THEN 'Quito' WHEN n=5 THEN 'Baltra' WHEN n IN (6,7) THEN 'Santa Cruz' WHEN n IN (14,15) THEN CASE n WHEN 14 THEN 'San Cristobal' ELSE 'Isabela' END ELSE 'Puerto Ayora' END,
       3.8+(n%9)*0.1,CASE n%4 WHEN 0 THEN NULL ELSE 1+(n%3) END,'{"daily":"07:00-20:00"}',NULL,NULL,
       CASE WHEN n<=2 THEN 'Guayaquil airport service area' WHEN n<=4 THEN 'Quito airport service area' WHEN n<=7 THEN 'Baltra and Santa Cruz transfer chain' ELSE 'Puerto Ayora visitor service point' END
FROM seq;

INSERT INTO roads(road_id,name,city,geom_json) VALUES
 ('road_uio_airport_city_late','Quito airport to city late-arrival route','Quito','[[-0.129,-78.357],[-0.180,-78.430],[-0.220,-78.510]]'),
 ('road_baltra_to_puerto_ayora_standard','Baltra airport to Puerto Ayora standard chain','Santa Cruz','[[-0.454,-90.266],[-0.485,-90.255],[-0.487,-90.254],[-0.745,-90.314]]'),
 ('road_baltra_pickup_late_change','Certified Baltra pickup corridor','Santa Cruz','[[-0.454,-90.266],[-0.486,-90.254],[-0.745,-90.314]]'),
 ('road_venue_jardin_walk','Workshop venue to Jardin Tranquilo walk','Puerto Ayora','[[-0.745,-90.314],[-0.744,-90.315]]'),
 ('road_puerto_clinic_walk','Workshop venue to community clinic','Puerto Ayora','[[-0.745,-90.314],[-0.7425,-90.3165]]'),
 ('road_gye_airport_bus','Guayaquil airport to bus stop','Guayaquil','[[-2.157,-79.884],[-2.160,-79.887]]'),
 ('road_uio_taxi_desk','Quito arrivals to taxi desk','Quito','[[-0.129,-78.357],[-0.131,-78.359]]'),
 ('road_highlands_bellavista','Highlands junction to Bellavista','Santa Cruz','[[-0.650,-90.330],[-0.690,-90.340]]'),
 ('road_puerto_pier_market','Municipal pier to market','Puerto Ayora','[[-0.744,-90.311],[-0.739,-90.318]]'),
 ('road_tortuga_trail','Puerto Ayora to Tortuga Bay trailhead','Puerto Ayora','[[-0.745,-90.314],[-0.752,-90.322]]');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<20)
INSERT INTO place_reviews(place_id,author,rating,text,time)
SELECT CASE WHEN n<=12 THEN (CASE n WHEN 1 THEN 'place_gye' WHEN 2 THEN 'place_uio' WHEN 3 THEN 'place_gps' WHEN 4 THEN 'place_itabaca_baltra' WHEN 5 THEN 'place_itabaca_santacruz' WHEN 6 THEN 'place_puerto_ayora_bus' WHEN 7 THEN 'place_workshop_venue' WHEN 8 THEN 'place_jardin_tranquilo' WHEN 9 THEN 'place_puerto_clinic' WHEN 10 THEN 'place_ec_08' WHEN 11 THEN 'place_ec_10' ELSE 'place_ec_12' END) ELSE printf('place_ec_%02d',n-2) END,
       printf('reviewer_%02d',n),4+(n%2),
       CASE n WHEN 1 THEN 'The Guayaquil terminal is compact and the covered connection is easy with luggage.' WHEN 2 THEN 'Quito airport is far from the old city, so late arrivals benefit from an airport-area hotel.' WHEN 3 THEN 'Baltra arrivals require several ground and channel steps before reaching Puerto Ayora.' WHEN 4 THEN 'The Baltra-side barge queue changes quickly when one vessel is out of service.' WHEN 5 THEN 'The Santa Cruz dock has shared taxis, but the last departure times should be checked.' WHEN 6 THEN 'The town bus terminal is practical for daylight arrivals and less simple after dark.' WHEN 7 THEN 'The venue entrance is close to the waterfront and has limited vehicle waiting space.' WHEN 8 THEN 'The garden-side rooms are quiet and the venue walk is short in daylight.' WHEN 9 THEN 'The clinic stocks common motion-sickness supplies but closes earlier on weekends.' WHEN 10 THEN 'The municipal pier is busy at excursion departure times and calmer in late afternoon.' WHEN 11 THEN 'The central pharmacy accepts cards, while some island counters remain cash-only.' WHEN 12 THEN 'The Tortuga Bay trail is land-based but requires a long walk and sun protection.' WHEN 13 THEN 'The bus stop has clear route boards and no staffed luggage assistance.' WHEN 14 THEN 'The airport footbridge is lit overnight and avoids a vehicle transfer.' WHEN 15 THEN 'The taxi desk quotes fixed airport-zone rates before assigning a driver.' WHEN 16 THEN 'The pharmacy can explain local brands but does not replace a medical consultation.' WHEN 17 THEN 'The shuttle bay closes after the final scheduled airport arrival wave.' WHEN 18 THEN 'The highlands junction adds transfer time when road works use single-lane control.' WHEN 19 THEN 'The shared taxi stand groups passengers by destination and may wait to fill seats.' ELSE 'The market has cash services, food stalls and variable opening hours on Sundays.' END,
       strftime('%Y-%m-%d','2026-06-01','+'||n||' days')
FROM seq;

INSERT INTO transit_lines(line_id,name,mode,operator,segment_minutes_json) VALUES
 ('line_gye_airport_bus','Guayaquil Airport Connector','bus','ATM Guayaquil','[8,7,10]'),
 ('line_uio_airport_bus','Quito Airport Express','bus','Aeroservicios','[20,25,18]'),
 ('line_baltra_shuttle','Baltra Airport Shuttle','bus','Galapagos Airport Authority','[12]'),
 ('line_santacruz_bus','Santa Cruz Highlands Bus','bus','Cooperativa Santa Cruz','[18,25,30]'),
 ('line_puerto_local','Puerto Ayora Local Loop','bus','Municipio Santa Cruz','[10,8,12]');
INSERT INTO transit_stops(stop_id,name,lat,lng,city) VALUES
 ('stop_gye_terminal','Guayaquil Airport Terminal',-2.157,-79.884,'Guayaquil'),('stop_gye_bus','Guayaquil Airport Bus Stop',-2.160,-79.887,'Guayaquil'),
 ('stop_uio_terminal','Quito Airport Terminal',-0.129,-78.357,'Quito'),('stop_uio_city','Quito Central Transfer Stop',-0.220,-78.510,'Quito'),
 ('stop_gps_terminal','Baltra Airport Terminal',-0.454,-90.266,'Baltra'),('stop_baltra_dock','Baltra Channel Dock',-0.485,-90.255,'Baltra'),
 ('stop_santacruz_dock','Santa Cruz Channel Dock',-0.487,-90.254,'Santa Cruz'),('stop_bellavista','Bellavista Junction',-0.690,-90.340,'Santa Cruz'),
 ('stop_puerto_terminal','Puerto Ayora Bus Terminal',-0.740,-90.318,'Puerto Ayora'),('stop_workshop','Marine Data Lab',-0.745,-90.314,'Puerto Ayora');
INSERT INTO transit_schedule(line_id,stop_id,direction,stop_seq,time) VALUES
 ('line_gye_airport_bus','stop_gye_terminal','city',1,'06:20'),('line_gye_airport_bus','stop_gye_bus','city',2,'06:28'),
 ('line_uio_airport_bus','stop_uio_terminal','city',1,'06:00'),('line_uio_airport_bus','stop_uio_city','airport',2,'20:30'),
 ('line_baltra_shuttle','stop_gps_terminal','dock',1,'09:45'),('line_baltra_shuttle','stop_baltra_dock','airport',2,'15:40'),
 ('line_santacruz_bus','stop_santacruz_dock','southbound',1,'10:20'),('line_santacruz_bus','stop_bellavista','southbound',2,'10:48'),
 ('line_santacruz_bus','stop_puerto_terminal','southbound',3,'11:25'),('line_santacruz_bus','stop_puerto_terminal','northbound',1,'07:10'),
 ('line_puerto_local','stop_puerto_terminal','waterfront',1,'08:00'),('line_puerto_local','stop_workshop','waterfront',2,'08:12'),
 ('line_puerto_local','stop_workshop','terminal',1,'17:20'),('line_puerto_local','stop_puerto_terminal','terminal',2,'17:32'),
 ('line_santacruz_bus','stop_bellavista','northbound',2,'07:42');
