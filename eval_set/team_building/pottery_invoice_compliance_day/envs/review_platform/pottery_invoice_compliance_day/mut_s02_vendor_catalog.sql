INSERT OR IGNORE INTO merchants(merchant_id,name,category,city,area,address,phone,rating_tenths,review_count,avg_price_minor,price_band,hours,tags,has_private_room,max_party_size) VALUES
('venue_pottery_lumen_heping','陶光工坊和平店','venue','天津','和平区','和平区睦南道88号','022-28176797',45,41,1332000,'$$','09:30-20:30','陶艺,团建,服务类发票,对公转账,丁腈手套,低接触釉料,老师资质公示,定金2800元,烧制7天',1,31),
('venue_pottery_southbank','南岸陶社和平体验店','venue','天津','和平区','和平区大理道37号','022-26591464',46,42,1344000,'$$','10:30-19:30','陶艺,团建,发票待确认,材料销售发票,低接触替代,定金3200元,提前一周可全退',1,32);
INSERT OR IGNORE INTO deals(deal_id,merchant_id,title,description,price_minor,list_price_minor,serves,valid_until,status) VALUES
('deal_pottery_lumen_0703','venue_pottery_lumen_heping','27人釉色共创半日','含拉坯、上釉、老师示范和统一烧制配送；开票与资质以书面问答为准。',1339800,1576200,27,'2026-07-31','active'),
('deal_pottery_south_0703','venue_pottery_southbank','团队手捏与轻餐组合','可容纳27人，发票和定金条款需单独核验。',1344000,1500000,27,'2026-07-31','active');
