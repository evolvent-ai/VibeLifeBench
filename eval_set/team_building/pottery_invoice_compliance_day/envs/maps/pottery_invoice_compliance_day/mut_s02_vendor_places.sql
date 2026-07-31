INSERT OR IGNORE INTO places(place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
('place_pottery_lumen_heping','陶光工坊和平店','attraction',39.11842,117.19507,'CN','天津',4.5,2,'{"mon":"09:30-20:30","thu":"09:30-20:30"}','022-28176797','https://pottery.example/lumen','天津市和平区睦南道88号'),
('place_pottery_southbank','南岸陶社和平体验店','attraction',39.11680,117.19020,'CN','天津',4.6,2,'{"mon":"10:30-19:30","thu":"10:30-19:30"}','022-26591464','https://pottery.example/southbank','天津市和平区大理道37号');
INSERT INTO place_reviews(place_id,author,rating,text,time)
SELECT 'place_pottery_lumen_heping','企业活动访客',4,'二层室内场地可乘电梯抵达，一层大堂适合集合；附近车位有限，地铁后步行更稳妥。','2026-06-24T15:32:07+08:00'
WHERE NOT EXISTS (SELECT 1 FROM place_reviews WHERE place_id='place_pottery_lumen_heping' AND author='企业活动访客');
INSERT INTO place_reviews(place_id,author,rating,text,time)
SELECT 'place_pottery_southbank','行政活动访客',4,'院内等候区较小，团队到店需分批下车；雨天建议从大理道东口进入。','2026-06-18T11:20:00+08:00'
WHERE NOT EXISTS (SELECT 1 FROM place_reviews WHERE place_id='place_pottery_southbank' AND author='行政活动访客');
