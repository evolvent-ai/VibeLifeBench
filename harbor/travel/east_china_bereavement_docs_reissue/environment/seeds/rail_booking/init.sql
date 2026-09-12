-- Reviewed Stage 0 rail inventory: 40 distinct offers and 40 matching status rows.
INSERT INTO train_offers(offer_id,train_no,date,train_type,origin_city,dest_city,origin_station,dest_station,depart_at,arrive_at,seat_class,adult_fare,student_fare,currency,adult_seats_remaining,ordinary_student_seats_remaining,graduation_student_seats_remaining,student_discount_available,refundability,route_notes,source_url) VALUES
 ('rail_offer_sha_suz_0403_g7206','G7206','2026-04-03','G','Shanghai','Suzhou','Shanghai Hongqiao','Suzhou','2026-04-03T17:35:00+08:00','2026-04-03T18:05:00+08:00','second_class',39.5,29.62,'CNY',12,0,0,0,'refundable','scenario textSuzhouscenario text，scenario text。','official timetable snapshot'),
 ('rail_offer_sha_suz_0403_g7212','G7212','2026-04-03','G','Shanghai','Suzhou','Shanghai Hongqiao','Suzhou','2026-04-03T19:10:00+08:00','2026-04-03T19:43:00+08:00','second_class',39.5,29.62,'CNY',18,0,0,0,'refundable','scenario text。','official timetable snapshot'),
 ('rail_offer_suz_sha_0411_g7025','G7025','2026-04-11','G','Suzhou','Shanghai','Suzhou','Shanghai Hongqiao','2026-04-11T10:12:00+08:00','2026-04-11T10:42:00+08:00','second_class',39.5,29.62,'CNY',3,0,0,0,'refundable','scenario text，scenario textverification window。','official timetable snapshot'),
 ('rail_offer_suz_sha_0411_g7031','G7031','2026-04-11','G','Suzhou','Shanghai','Suzhou','Shanghai Hongqiao','2026-04-11T11:26:00+08:00','2026-04-11T11:58:00+08:00','second_class',44.0,33.0,'CNY',16,0,0,0,'refundable','scenario textwaitlist bookingscenario textservice windowscenario text。','official timetable snapshot'),
 ('rail_offer_sha_nb_0416_d3135','D3135','2026-04-16','D','Shanghai','Ningbo','Shanghai Hongqiao','Ningbo','2026-04-16T17:58:00+08:00','2026-04-16T19:46:00+08:00','second_class',143.0,107.25,'CNY',20,0,0,0,'refundable','scenario textNingboscenario texttimescenario textelderscenario text。','official timetable snapshot');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<35)
INSERT INTO train_offers(offer_id,train_no,date,train_type,origin_city,dest_city,origin_station,dest_station,depart_at,arrive_at,seat_class,adult_fare,student_fare,currency,adult_seats_remaining,ordinary_student_seats_remaining,graduation_student_seats_remaining,student_discount_available,refundability,route_notes,source_url)
SELECT printf('rail_route_%03d',n),
       CASE n%2 WHEN 0 THEN printf('D%04d',3200+n) ELSE printf('G%04d',7300+n) END,
       CASE n%5 WHEN 0 THEN '2026-04-03' WHEN 1 THEN '2026-04-11' WHEN 2 THEN '2026-04-16' WHEN 3 THEN '2026-04-17' ELSE '2026-04-18' END,
       CASE n%2 WHEN 0 THEN 'D' ELSE 'G' END,
       CASE n%5 WHEN 0 THEN 'Shanghai' WHEN 1 THEN 'Suzhou' WHEN 2 THEN 'Shanghai' WHEN 3 THEN 'Ningbo' ELSE 'Hangzhou' END,
       CASE n%5 WHEN 0 THEN 'Suzhou' WHEN 1 THEN 'Shanghai' WHEN 2 THEN 'Ningbo' WHEN 3 THEN 'Hangzhou' ELSE 'Shanghai' END,
       CASE n%5 WHEN 0 THEN 'Shanghai Hongqiao' WHEN 1 THEN 'Suzhou Industrial Park' WHEN 2 THEN 'Shanghai South' WHEN 3 THEN 'Ningbo' ELSE 'Hangzhou East' END,
       CASE n%5 WHEN 0 THEN 'Suzhou North' WHEN 1 THEN 'Shanghai Station' WHEN 2 THEN 'Ningbo' WHEN 3 THEN 'Hangzhou East' ELSE 'Shanghai Hongqiao' END,
       (CASE n%5 WHEN 0 THEN '2026-04-03T' WHEN 1 THEN '2026-04-11T' WHEN 2 THEN '2026-04-16T' WHEN 3 THEN '2026-04-17T' ELSE '2026-04-18T' END)||printf('%02d:%02d:00+08:00',7+(n%11),(n*7)%60),
       (CASE n%5 WHEN 0 THEN '2026-04-03T' WHEN 1 THEN '2026-04-11T' WHEN 2 THEN '2026-04-16T' WHEN 3 THEN '2026-04-17T' ELSE '2026-04-18T' END)||printf('%02d:%02d:00+08:00',9+(n%11),(n*7+18)%60),
       CASE n%4 WHEN 0 THEN 'first_class' ELSE 'second_class' END,
       CASE n%5 WHEN 0 THEN 54.5 WHEN 1 THEN 46.0 WHEN 2 THEN 138.0 WHEN 3 THEN 92.0 ELSE 73.0 END,
       CASE n%5 WHEN 0 THEN 40.87 WHEN 1 THEN 34.5 WHEN 2 THEN 103.5 WHEN 3 THEN 69.0 ELSE 54.75 END,
       'CNY',5+(n%22),0,0,0,
       CASE n%4 WHEN 0 THEN 'limited_change' WHEN 1 THEN 'refundable' WHEN 2 THEN 'refundable_before_departure' ELSE 'change_fee_applies' END,
       CASE n%10 WHEN 0 THEN 'scenario text，scenario texttime。' WHEN 1 THEN 'scenario text，scenario text。' WHEN 2 THEN 'scenario text，scenario text。' WHEN 3 THEN 'scenario text，scenario text。' WHEN 4 THEN 'scenario text，scenario textverifyscenario text。' WHEN 5 THEN 'scenario text，scenario text。' WHEN 6 THEN 'scenario texttimescenario text，scenario textelderscenario text。' WHEN 7 THEN 'scenario text，scenario text。' WHEN 8 THEN 'scenario text，scenario textinventory。' ELSE 'scenario text。' END,
       'official timetable snapshot'
FROM seq;

INSERT INTO train_status(train_no,date,status,delay_min,platform,gate,last_updated)
SELECT train_no,date,'SCHEDULED',0,printf('%d',(rowid%12)+1),printf('A%d',(rowid%18)+1),'2026-04-03T08:00:00+08:00'
FROM train_offers;
