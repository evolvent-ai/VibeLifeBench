-- Reviewed Stage 0 lodging inventory: 20 properties and 50 rate-plan rows.
INSERT INTO hotels(hotel_id,name,city,district,geo_lat,geo_lng,star_rating,user_rating,user_rating_count,amenities_json,address_json,policies_json,description,capacity_estimate) VALUES
 ('hotel_suz_mourning_nearby','苏州静安礼居','苏州','吴中',31.260,120.630,4,8.8,220,'["wifi","breakfast","elevator","quiet_room"]','{"street":"宝带西路18号"}','{"front_desk":"24h","deposit":"card","smoking":"designated_only"}','距殡仪服务中心约两公里，电梯和安静楼层适合老人休息。',50);

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<19)
INSERT INTO hotels(hotel_id,name,city,district,geo_lat,geo_lng,star_rating,user_rating,user_rating_count,amenities_json,address_json,policies_json,description,capacity_estimate)
SELECT printf('hotel_east_%02d',n),
       (CASE n%4 WHEN 0 THEN '北京槐园酒店' WHEN 1 THEN '苏州河畔客舍' WHEN 2 THEN '上海静里宾馆' ELSE '宁波海曙旅居' END)||printf('-%02d',n),
       CASE n%4 WHEN 0 THEN '北京' WHEN 1 THEN '苏州' WHEN 2 THEN '上海' ELSE '宁波' END,
       CASE n%8 WHEN 0 THEN '朝阳' WHEN 1 THEN '姑苏' WHEN 2 THEN '静安' WHEN 3 THEN '海曙' WHEN 4 THEN '东城' WHEN 5 THEN '吴中' WHEN 6 THEN '长宁' ELSE '鄞州' END,
       29.8+(n%8)*0.18,116.3+(n%9)*0.55,3+(n%3),7.6+(n%12)*0.1,80+n*13,
       CASE n%4 WHEN 0 THEN '["wifi","laundry","late_checkin"]' WHEN 1 THEN '["wifi","elevator","family_room"]' WHEN 2 THEN '["wifi","metro_access","luggage_storage"]' ELSE '["wifi","quiet_room","breakfast"]' END,
       printf('{"street":"%s%d号"}',CASE n%4 WHEN 0 THEN '安贞路' WHEN 1 THEN '盘门路' WHEN 2 THEN '武定路' ELSE '柳汀街' END,20+n),
       CASE n%3 WHEN 0 THEN '{"deposit":"cash_or_card","quiet_hours":"22:00-07:00"}' WHEN 1 THEN '{"deposit":"card","late_arrival":"call_front_desk"}' ELSE '{"deposit":"none","accessible_room":"on_request"}' END,
       CASE n%10 WHEN 0 THEN '靠近地铁站，夜间抵达仍有照明良好的步行路线。' WHEN 1 THEN '前台可协助老人使用电梯，房间远离宴会区域。' WHEN 2 THEN '临近铁路客站，早班出发可缩短市内接驳时间。' WHEN 3 THEN '院内安静但餐饮选择较少，适合短住休整。' WHEN 4 THEN '可寄存行李，退房后前往窗口办事较方便。' WHEN 5 THEN '家庭房空间充足，双床需要在入住前再次确认。' WHEN 6 THEN '周边晚高峰拥堵，出租车上客点位于侧门。' WHEN 7 THEN '提供简单早餐，过敏信息需直接向餐厅确认。' WHEN 8 THEN '取消期限较宽，适合尚未完全确定的行程。' ELSE '距核心地点稍远，但公共交通换乘清晰。' END,
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
