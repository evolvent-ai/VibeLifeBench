-- Reviewed neutral flight inventory: 50 flights, 60 fare buckets and 50 status rows.
INSERT INTO flights(flight_no,origin,dest,depart_dt,arrive_dt,equipment,base_price,currency,carrier) VALUES
 ('UA858','PVG','LAX','2026-08-14T21:30:00+08:00','2026-08-14T18:10:00-07:00','B777-300ER',520,'USD','United Airlines'),
 ('CM473','LAX','PTY','2026-08-14T22:45:00-07:00','2026-08-15T06:30:00-05:00','B737-800',210,'USD','Copa Airlines'),
 ('CM159','PTY','UIO','2026-08-15T09:20:00-05:00','2026-08-15T11:25:00-05:00','B737-800',180,'USD','Copa Airlines'),
 ('LA1411','UIO','GPS','2026-08-16T07:30:00-05:00','2026-08-16T09:15:00-06:00','A320',170,'USD','LATAM'),
 ('CX368','PVG','HKG','2026-08-14T19:40:00+08:00','2026-08-14T22:25:00+08:00','A330-300',210,'USD','Cathay Pacific'),
 ('CX315','HKG','MAD','2026-08-15T00:50:00+08:00','2026-08-15T08:05:00+02:00','A350-900',790,'USD','Cathay Pacific'),
 ('IB6453','MAD','GYE','2026-08-15T11:45:00+02:00','2026-08-15T16:55:00-05:00','A330-200',690,'USD','Iberia'),
 ('AV1632','GYE','GPS','2026-08-16T09:15:00-05:00','2026-08-16T11:10:00-06:00','A319',190,'USD','Avianca Ecuador'),
 ('KL896','PVG','AMS','2026-08-14T23:05:00+08:00','2026-08-15T05:55:00+02:00','B787-9',580,'USD','KLM'),
 ('KL755','AMS','UIO','2026-08-15T10:10:00+02:00','2026-08-15T15:15:00-05:00','B787-9',610,'USD','KLM'),
 ('AV1688','UIO','GPS','2026-08-16T07:30:00-05:00','2026-08-16T09:15:00-06:00','A320',165,'USD','Avianca Ecuador'),
 ('AF111','PVG','CDG','2026-08-15T00:15:00+08:00','2026-08-15T07:20:00+02:00','B777-300ER',560,'USD','Air France'),
 ('AF870','CDG','GYE','2026-08-15T09:20:00+02:00','2026-08-15T15:25:00-05:00','A350-900',760,'USD','Air France'),
 ('AV1638','GYE','GPS','2026-08-17T14:10:00-05:00','2026-08-17T16:05:00-06:00','A319',220,'USD','Avianca Ecuador'),
 ('AV1633','GPS','GYE','2026-08-23T13:00:00-06:00','2026-08-23T15:00:00-05:00','A319',185,'USD','Avianca Ecuador'),
 ('IB6454','GYE','MAD','2026-08-23T19:10:00-05:00','2026-08-24T13:15:00+02:00','A330-200',680,'USD','Iberia'),
 ('IB6455','MAD','PVG','2026-08-24T17:10:00+02:00','2026-08-25T10:20:00+08:00','A350-900',730,'USD','Iberia');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<33)
INSERT INTO flights(flight_no,origin,dest,depart_dt,arrive_dt,equipment,base_price,currency,carrier)
SELECT (CASE n%6 WHEN 0 THEN 'LA' WHEN 1 THEN 'AV' WHEN 2 THEN 'IB' WHEN 3 THEN 'CM' WHEN 4 THEN 'UX' ELSE 'AR' END)||printf('%04d',2100+n),
       CASE n%8 WHEN 0 THEN 'GYE' WHEN 1 THEN 'UIO' WHEN 2 THEN 'GPS' WHEN 3 THEN 'SCY' WHEN 4 THEN 'PTY' WHEN 5 THEN 'BOG' WHEN 6 THEN 'LIM' ELSE 'MAD' END,
       CASE n%8 WHEN 0 THEN 'GPS' WHEN 1 THEN 'GYE' WHEN 2 THEN 'UIO' WHEN 3 THEN 'GYE' WHEN 4 THEN 'UIO' WHEN 5 THEN 'GYE' WHEN 6 THEN 'UIO' ELSE 'GYE' END,
       strftime('%Y-%m-%dT%H:%M:00Z','2026-08-10 06:00:00','+'||(n%16)||' days','+'||(n%13)||' hours','+'||((n*7)%60)||' minutes'),
       strftime('%Y-%m-%dT%H:%M:00Z','2026-08-10 08:00:00','+'||(n%16)||' days','+'||(n%13)||' hours','+'||((n*7+25)%60)||' minutes'),
       CASE n%5 WHEN 0 THEN 'A319' WHEN 1 THEN 'A320' WHEN 2 THEN 'B737-800' WHEN 3 THEN 'A321neo' ELSE 'B787-8' END,
       130+(n%11)*47,'USD',CASE n%6 WHEN 0 THEN 'LATAM' WHEN 1 THEN 'Avianca' WHEN 2 THEN 'Iberia' WHEN 3 THEN 'Copa Airlines' WHEN 4 THEN 'Air Europa' ELSE 'Aerolineas Argentinas' END
FROM seq;

INSERT INTO fare_buckets(flight_no,date,cabin,price,seats_remaining)
SELECT flight_no,substr(depart_dt,1,10),'ECONOMY',base_price,4+(rowid%19) FROM flights;
INSERT INTO fare_buckets(flight_no,date,cabin,price,seats_remaining)
SELECT flight_no,substr(depart_dt,1,10),'PREMIUM_ECONOMY',CAST(base_price*1.55 AS INTEGER),2+(rowid%5)
FROM flights WHERE flight_no IN ('UA858','CX368','CX315','IB6453','KL896','KL755','AF111','AF870','IB6454','IB6455');
INSERT INTO flight_status(flight_no,date,status,actual_depart,actual_arrive,gate,terminal,delay_min,last_updated)
SELECT flight_no,substr(depart_dt,1,10),'scheduled',NULL,NULL,NULL,NULL,0,'2026-07-24T00:00:00Z' FROM flights;
