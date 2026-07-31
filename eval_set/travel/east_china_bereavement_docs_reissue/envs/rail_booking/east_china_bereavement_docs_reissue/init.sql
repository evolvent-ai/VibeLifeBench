-- Reviewed Stage 0 rail inventory: 40 distinct offers and 40 matching status rows.
INSERT INTO train_offers(offer_id,train_no,date,train_type,origin_city,dest_city,origin_station,dest_station,depart_at,arrive_at,seat_class,adult_fare,student_fare,currency,adult_seats_remaining,ordinary_student_seats_remaining,graduation_student_seats_remaining,student_discount_available,refundability,route_notes,source_url) VALUES
 ('rail_offer_sha_suz_0403_g7206','G7206','2026-04-03','G','上海','苏州','上海虹桥','苏州','2026-04-03T17:35:00+08:00','2026-04-03T18:05:00+08:00','second_class',39.5,29.62,'CNY',12,0,0,0,'refundable','虹桥到苏州直达，落地衔接较紧。','official timetable snapshot'),
 ('rail_offer_sha_suz_0403_g7212','G7212','2026-04-03','G','上海','苏州','上海虹桥','苏州','2026-04-03T19:10:00+08:00','2026-04-03T19:43:00+08:00','second_class',39.5,29.62,'CNY',18,0,0,0,'refundable','为航班延误预留缓冲的晚间直达车。','official timetable snapshot'),
 ('rail_offer_suz_sha_0411_g7025','G7025','2026-04-11','G','苏州','上海','苏州','上海虹桥','2026-04-11T10:12:00+08:00','2026-04-11T10:42:00+08:00','second_class',39.5,29.62,'CNY',3,0,0,0,'refundable','上午候补车次，抵达后仍需转往核验窗口。','official timetable snapshot'),
 ('rail_offer_suz_sha_0411_g7031','G7031','2026-04-11','G','苏州','上海','苏州','上海虹桥','2026-04-11T11:26:00+08:00','2026-04-11T11:58:00+08:00','second_class',44.0,33.0,'CNY',16,0,0,0,'refundable','可替代候补单并保留窗口前交通余量。','official timetable snapshot'),
 ('rail_offer_sha_nb_0416_d3135','D3135','2026-04-16','D','上海','宁波','上海虹桥','宁波','2026-04-16T17:58:00+08:00','2026-04-16T19:46:00+08:00','second_class',143.0,107.25,'CNY',20,0,0,0,'refundable','直达宁波且接站时间适合老人休息。','official timetable snapshot');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<35)
INSERT INTO train_offers(offer_id,train_no,date,train_type,origin_city,dest_city,origin_station,dest_station,depart_at,arrive_at,seat_class,adult_fare,student_fare,currency,adult_seats_remaining,ordinary_student_seats_remaining,graduation_student_seats_remaining,student_discount_available,refundability,route_notes,source_url)
SELECT printf('rail_route_%03d',n),
       CASE n%2 WHEN 0 THEN printf('D%04d',3200+n) ELSE printf('G%04d',7300+n) END,
       CASE n%5 WHEN 0 THEN '2026-04-03' WHEN 1 THEN '2026-04-11' WHEN 2 THEN '2026-04-16' WHEN 3 THEN '2026-04-17' ELSE '2026-04-18' END,
       CASE n%2 WHEN 0 THEN 'D' ELSE 'G' END,
       CASE n%5 WHEN 0 THEN '上海' WHEN 1 THEN '苏州' WHEN 2 THEN '上海' WHEN 3 THEN '宁波' ELSE '杭州' END,
       CASE n%5 WHEN 0 THEN '苏州' WHEN 1 THEN '上海' WHEN 2 THEN '宁波' WHEN 3 THEN '杭州' ELSE '上海' END,
       CASE n%5 WHEN 0 THEN '上海虹桥' WHEN 1 THEN '苏州园区' WHEN 2 THEN '上海南' WHEN 3 THEN '宁波' ELSE '杭州东' END,
       CASE n%5 WHEN 0 THEN '苏州北' WHEN 1 THEN '上海站' WHEN 2 THEN '宁波' WHEN 3 THEN '杭州东' ELSE '上海虹桥' END,
       (CASE n%5 WHEN 0 THEN '2026-04-03T' WHEN 1 THEN '2026-04-11T' WHEN 2 THEN '2026-04-16T' WHEN 3 THEN '2026-04-17T' ELSE '2026-04-18T' END)||printf('%02d:%02d:00+08:00',7+(n%11),(n*7)%60),
       (CASE n%5 WHEN 0 THEN '2026-04-03T' WHEN 1 THEN '2026-04-11T' WHEN 2 THEN '2026-04-16T' WHEN 3 THEN '2026-04-17T' ELSE '2026-04-18T' END)||printf('%02d:%02d:00+08:00',9+(n%11),(n*7+18)%60),
       CASE n%4 WHEN 0 THEN 'first_class' ELSE 'second_class' END,
       CASE n%5 WHEN 0 THEN 54.5 WHEN 1 THEN 46.0 WHEN 2 THEN 138.0 WHEN 3 THEN 92.0 ELSE 73.0 END,
       CASE n%5 WHEN 0 THEN 40.87 WHEN 1 THEN 34.5 WHEN 2 THEN 103.5 WHEN 3 THEN 69.0 ELSE 54.75 END,
       'CNY',5+(n%22),0,0,0,
       CASE n%4 WHEN 0 THEN 'limited_change' WHEN 1 THEN 'refundable' WHEN 2 THEN 'refundable_before_departure' ELSE 'change_fee_applies' END,
       CASE n%10 WHEN 0 THEN '直达但早班，需要预留进站安检时间。' WHEN 1 THEN '到站靠近市区，适合携带少量行李。' WHEN 2 THEN '停站较多，票价低但总耗时更长。' WHEN 3 THEN '晚高峰前抵达，换乘出租更稳定。' WHEN 4 THEN '出发站较远，应核对市内交通成本。' WHEN 5 THEN '车厢余票充足，退改条件较宽松。' WHEN 6 THEN '抵达时间偏晚，不宜作为老人首选。' WHEN 7 THEN '中午出发，可避开通勤拥堵。' WHEN 8 THEN '仅少量余票，需复查实时库存。' ELSE '可改签但临近发车会收取手续费。' END,
       'official timetable snapshot'
FROM seq;

INSERT INTO train_status(train_no,date,status,delay_min,platform,gate,last_updated)
SELECT train_no,date,'SCHEDULED',0,printf('%d',(rowid%12)+1),printf('A%d',(rowid%18)+1),'2026-04-03T08:00:00+08:00'
FROM train_offers;
