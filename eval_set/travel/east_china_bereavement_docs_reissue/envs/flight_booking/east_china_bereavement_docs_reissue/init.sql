-- Reviewed Stage 0 flight inventory: 20 flights, 30 fare buckets and 20 status rows.
INSERT INTO flights(flight_no,origin,dest,depart_dt,arrive_dt,equipment,base_price,currency,carrier) VALUES
 ('MU5102','PEK','SHA','2026-04-03T14:15:00+08:00','2026-04-03T16:25:00+08:00','B737-800',1680,'CNY','China Eastern'),
 ('CA1856','NGB','PEK','2026-04-21T18:10:00+08:00','2026-04-21T20:30:00+08:00','A320neo',980,'CNY','Air China'),
 ('CA1501','PEK','SHA','2026-04-03T09:05:00+08:00','2026-04-03T11:15:00+08:00','A321',1760,'CNY','Air China'),
 ('MU5120','PEK','PVG','2026-04-03T10:30:00+08:00','2026-04-03T12:45:00+08:00','A330-300',1820,'CNY','China Eastern'),
 ('HU7605','PEK','SHA','2026-04-03T11:50:00+08:00','2026-04-03T14:00:00+08:00','B737-900',1540,'CNY','Hainan Airlines'),
 ('FM9102','PEK','PVG','2026-04-03T12:40:00+08:00','2026-04-03T14:55:00+08:00','B737-700',1490,'CNY','Shanghai Airlines'),
 ('MU5108','PEK','SHA','2026-04-03T16:20:00+08:00','2026-04-03T18:35:00+08:00','A320',1360,'CNY','China Eastern'),
 ('CA1883','PEK','PVG','2026-04-03T17:10:00+08:00','2026-04-03T19:25:00+08:00','A330-200',1710,'CNY','Air China'),
 ('KN5955','PKX','PVG','2026-04-03T08:20:00+08:00','2026-04-03T10:35:00+08:00','B737-800',1280,'CNY','China United'),
 ('MU5156','PEK','SHA','2026-04-03T19:15:00+08:00','2026-04-03T21:25:00+08:00','A321',1190,'CNY','China Eastern'),
 ('MU5244','SHA','NGB','2026-04-16T15:20:00+08:00','2026-04-16T16:20:00+08:00','A319',720,'CNY','China Eastern'),
 ('GJ8752','PVG','NGB','2026-04-16T16:05:00+08:00','2026-04-16T17:10:00+08:00','A320',680,'CNY','Loong Air'),
 ('MU5453','PVG','NGB','2026-04-16T18:00:00+08:00','2026-04-16T19:00:00+08:00','A320neo',750,'CNY','China Eastern'),
 ('9C8683','SHA','NGB','2026-04-16T19:10:00+08:00','2026-04-16T20:15:00+08:00','A320',530,'CNY','Spring Airlines'),
 ('HO1021','PVG','NGB','2026-04-16T20:00:00+08:00','2026-04-16T21:05:00+08:00','A321',640,'CNY','Juneyao Air'),
 ('CA1542','NGB','PEK','2026-04-21T15:30:00+08:00','2026-04-21T17:50:00+08:00','B737-800',1180,'CNY','Air China'),
 ('MU5179','NGB','PKX','2026-04-21T16:40:00+08:00','2026-04-21T19:00:00+08:00','A320',1060,'CNY','China Eastern'),
 ('HU7290','NGB','PEK','2026-04-21T19:25:00+08:00','2026-04-21T21:45:00+08:00','B737-800',1020,'CNY','Hainan Airlines'),
 ('KN5976','NGB','PKX','2026-04-21T20:10:00+08:00','2026-04-21T22:25:00+08:00','B737-700',890,'CNY','China United'),
 ('FM9275','NGB','PVG','2026-04-18T11:15:00+08:00','2026-04-18T12:20:00+08:00','B737-800',620,'CNY','Shanghai Airlines');

INSERT INTO fare_buckets(flight_no,date,cabin,price,seats_remaining)
SELECT flight_no,substr(depart_dt,1,10),'ECONOMY',base_price,
       CASE CAST(substr(flight_no,-1) AS INTEGER)%5 WHEN 0 THEN 4 WHEN 1 THEN 7 WHEN 2 THEN 11 WHEN 3 THEN 15 ELSE 19 END
FROM flights;

INSERT INTO fare_buckets(flight_no,date,cabin,price,seats_remaining)
SELECT flight_no,substr(depart_dt,1,10),'BUSINESS',CAST(base_price*2.65 AS INTEGER),
       CASE CAST(substr(flight_no,-1) AS INTEGER)%3 WHEN 0 THEN 2 WHEN 1 THEN 3 ELSE 4 END
FROM flights WHERE flight_no IN ('MU5102','CA1856','CA1501','MU5120','HU7605','FM9102','MU5108','CA1883','MU5244','CA1542');

INSERT INTO flight_status(flight_no,date,status,actual_depart,actual_arrive,gate,terminal,delay_min,last_updated)
SELECT flight_no,substr(depart_dt,1,10),'scheduled',NULL,NULL,
       printf('%s%d',CASE origin WHEN 'PEK' THEN 'A' WHEN 'PKX' THEN 'B' WHEN 'NGB' THEN 'C' ELSE 'D' END,(rowid%24)+1),
       CASE origin WHEN 'PEK' THEN 'T2' WHEN 'PKX' THEN 'T1' WHEN 'NGB' THEN 'T2' WHEN 'PVG' THEN 'T1' ELSE 'T2' END,
       0,'2026-04-03T08:00:00+08:00'
FROM flights;
