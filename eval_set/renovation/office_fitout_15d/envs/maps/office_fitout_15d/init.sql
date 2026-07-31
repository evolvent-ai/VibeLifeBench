-- ──────────────────────────────────────────────────────────
-- source: places_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- 15 places: 1 office anchor + 1 property office + 1 fire dept + 12 commercial vendors.
-- Lat/lng are SYNTHESIZED from Shanghai district anchors with deterministic md5
-- jitter (see env/maps/README.md). They are plausible but NOT real addresses.
-- Each commercial-vendor place_id maps to a provider_id from
-- data/provider_profiles_seed.jsonl (category=commercial_design_build, prov_v3_001..009).

INSERT INTO places (place_id,name,category,lat,lng,country,city,rating,price_level,hours_json,phone,website,formatted) VALUES
('pl_zhou_mu_office','陆家嘴金融中心 4F 办公空间 (300sqm fit-up)','office_space',31.2398,121.5022,'CN','Shanghai',NULL,NULL,'{"monday": {"open": "00:00", "close": "23:59"}, "tuesday": {"open": "00:00", "close": "23:59"}, "wednesday": {"open": "00:00", "close": "23:59"}, "thursday": {"open": "00:00", "close": "23:59"}, "friday": {"open": "00:00", "close": "23:59"}, "saturday": {"open": "00:00", "close": "23:59"}, "sunday": {"open": "00:00", "close": "23:59"}}',NULL,NULL,'上海市浦东新区陆家嘴金融中心 4 层 (commercial fit-up anchor)'),
('pl_lujiazui_fc_property','陆家嘴金融中心物业服务中心','property_office',31.2401,121.5018,'CN','Shanghai',4.6,3,'{"monday": {"open": "08:30", "close": "20:00"}, "tuesday": {"open": "08:30", "close": "20:00"}, "wednesday": {"open": "08:30", "close": "20:00"}, "thursday": {"open": "08:30", "close": "20:00"}, "friday": {"open": "08:30", "close": "20:00"}, "saturday": {"open": "09:00", "close": "18:00"}, "sunday": {"open": "09:00", "close": "18:00"}}','+86-21-5588-3000','https://example.com/lujiazui-fc','上海市浦东新区陆家嘴金融中心 物业服务中心'),
('pl_jingan_fire_dept','静安区消防救援支队 验收科','fire_dept',31.2278,121.4458,'CN','Shanghai',4.5,2,'{"monday": {"open": "08:30", "close": "17:30"}, "tuesday": {"open": "08:30", "close": "17:30"}, "wednesday": {"open": "08:30", "close": "17:30"}, "thursday": {"open": "08:30", "close": "17:30"}, "friday": {"open": "08:30", "close": "17:30"}, "saturday": {"closed": true}, "sunday": {"closed": true}}','+86-21-5588-9119','https://example.com/jingan-fire','上海市静安区 消防救援支队'),
('pl_huan_commercial_office','沪安公装设计 江宁路公装中心','commercial_design_build',31.2272,121.4458,'CN','Shanghai',4.7,4,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9001','https://example.com/huan-commercial','上海市静安区 江宁路公装设计中心 (prov_v3_001_commercial_design_build)'),
('pl_shenpin_lujiazui_office','申品商业空间 陆家嘴公装样板间','commercial_design_build',31.2406,121.5025,'CN','Shanghai',4.8,4,'{"monday": {"open": "09:00", "close": "19:00"}, "tuesday": {"open": "09:00", "close": "19:00"}, "wednesday": {"open": "09:00", "close": "19:00"}, "thursday": {"open": "09:00", "close": "19:00"}, "friday": {"open": "09:00", "close": "19:00"}, "saturday": {"open": "10:00", "close": "18:00"}, "sunday": {"closed": true}}','+86-21-5555-9002','https://example.com/shenpin-cs','上海市浦东新区 陆家嘴公装样板间 (prov_v3_002_commercial_design_build)'),
('pl_lingchuang_beibund_office','领创公装工程 北外滩公装办公点','commercial_design_build',31.2491,121.5067,'CN','Shanghai',4.5,3,'{"monday": {"open": "08:30", "close": "18:00"}, "tuesday": {"open": "08:30", "close": "18:00"}, "wednesday": {"open": "08:30", "close": "18:00"}, "thursday": {"open": "08:30", "close": "18:00"}, "friday": {"open": "08:30", "close": "18:00"}, "saturday": {"open": "09:00", "close": "16:00"}, "sunday": {"closed": true}}','+86-21-5555-9003','https://example.com/lingchuang-cs','上海市虹口区 北外滩公装办公点 (prov_v3_003_commercial_design_build)'),
('pl_qihang_xinzhuang_office','启航装饰商业 莘庄商业综合体','commercial_design_build',31.1133,121.3878,'CN','Shanghai',4.4,3,'{"monday": {"open": "09:00", "close": "18:00"}, "tuesday": {"open": "09:00", "close": "18:00"}, "wednesday": {"open": "09:00", "close": "18:00"}, "thursday": {"open": "09:00", "close": "18:00"}, "friday": {"open": "09:00", "close": "18:00"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9004','https://example.com/qihang-cs','上海市闵行区 莘庄商业综合体 (prov_v3_004_commercial_design_build)'),
('pl_addxieyi_julu_studio','ADD写艺空间设计 巨鹿路设计工作室','commercial_design_build',31.2156,121.4533,'CN','Shanghai',4.9,5,'{"monday": {"open": "10:00", "close": "20:00"}, "tuesday": {"open": "10:00", "close": "20:00"}, "wednesday": {"open": "10:00", "close": "20:00"}, "thursday": {"open": "10:00", "close": "20:00"}, "friday": {"open": "10:00", "close": "20:00"}, "saturday": {"open": "11:00", "close": "18:00"}, "sunday": {"closed": true}}','+86-21-5555-9005','https://example.com/addxieyi','上海市静安区 巨鹿路设计工作室 (prov_v3_005_commercial_design_build)'),
('pl_boyuan_bund_design','博远公装设计 外滩公装设计馆','commercial_design_build',31.2389,121.4901,'CN','Shanghai',4.6,4,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9007','https://example.com/boyuan-cs','上海市黄浦区 外滩公装设计馆 (prov_v3_007_commercial_design_build)'),
('pl_hurui_zhenru_office','沪睿商办装修 真如商务公装基地','commercial_design_build',31.2533,121.4078,'CN','Shanghai',4.2,3,'{"monday": {"open": "08:30", "close": "18:00"}, "tuesday": {"open": "08:30", "close": "18:00"}, "wednesday": {"open": "08:30", "close": "18:00"}, "thursday": {"open": "08:30", "close": "18:00"}, "friday": {"open": "08:30", "close": "18:00"}, "saturday": {"open": "09:00", "close": "16:00"}, "sunday": {"closed": true}}','+86-21-5555-9008','https://example.com/hurui-co','上海市普陀区 真如商务公装基地 (prov_v3_008_commercial_design_build)'),
('pl_safehands_insurance_broker','慧择保险经纪 浦东商业部','insurance_broker',31.2356,121.5044,'CN','Shanghai',4.7,3,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9901','https://example.com/safehands-broker','上海市浦东新区 慧择保险经纪 商业部'),
('pl_chuanlian_iot_integrator','川联智能办公集成 张江智能办公园','smart_control_integrator',31.2114,121.5908,'CN','Shanghai',4.6,4,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9906','https://example.com/chuanlian-iot','上海市浦东新区 张江智能办公园 (commercial smart-control integrator)'),
('pl_aishi_furniture_warehouse','爱仕办公家具 商业部 浦东仓库','office_furniture_supplier',31.2266,121.5311,'CN','Shanghai',4.5,3,'{"monday": {"open": "08:30", "close": "18:00"}, "tuesday": {"open": "08:30", "close": "18:00"}, "wednesday": {"open": "08:30", "close": "18:00"}, "thursday": {"open": "08:30", "close": "18:00"}, "friday": {"open": "08:30", "close": "18:00"}, "saturday": {"open": "09:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9907','https://example.com/aishi-furniture','上海市浦东新区 爱仕办公家具 商业部仓库'),
('pl_guangshen_glass_partition','光晟玻璃隔断商业 浦东金桥展厅','glass_partition_supplier',31.2289,121.5384,'CN','Shanghai',4.6,3,'{"monday": {"open": "09:00", "close": "19:00"}, "tuesday": {"open": "09:00", "close": "19:00"}, "wednesday": {"open": "09:00", "close": "19:00"}, "thursday": {"open": "09:00", "close": "19:00"}, "friday": {"open": "09:00", "close": "19:00"}, "saturday": {"open": "10:00", "close": "18:00"}, "sunday": {"open": "10:00", "close": "16:00"}}','+86-21-5555-9905','https://example.com/guangshen-partition','上海市浦东新区 金桥展厅 光晟玻璃隔断'),
('pl_chanyi_supervision_office','禅艺第三方工程监理 浦东南路办公室','third_party_supervision',31.2358,121.4977,'CN','Shanghai',4.8,3,'{"monday": {"open": "09:00", "close": "18:00"}, "tuesday": {"open": "09:00", "close": "18:00"}, "wednesday": {"open": "09:00", "close": "18:00"}, "thursday": {"open": "09:00", "close": "18:00"}, "friday": {"open": "09:00", "close": "18:00"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9904','https://example.com/chanyi-supervision','上海市浦东新区 浦东南路 禅艺监理');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: roads_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- Shanghai expressway / arterial backbone connecting the Lujiazui anchor
-- (pl_zhou_mu_office) to vendor / property / regulator places.
-- Geometries are 2-point straight-line approximations.

INSERT INTO roads (road_id,name,city,geom_json) VALUES
('rd_neihuan_pudong','内环高架东段 (Inner Ring East — Pudong)','Shanghai','[[31.2398, 121.5022], [31.2266, 121.5311]]'),
('rd_yan_an_elevated','延安高架 (Yan_an Elevated — bund corridor)','Shanghai','[[31.2398, 121.5022], [31.2389, 121.4901]]'),
('rd_north_south_pudong','南北高架 浦东段 (North-South Elevated Pudong)','Shanghai','[[31.2398, 121.5022], [31.2114, 121.5908]]'),
('rd_jingan_corridor','静安公装 走廊','Shanghai','[[31.2272, 121.4458], [31.2156, 121.4533]]'),
('rd_zhouhuan_pudong','浦东周边环线 (Pudong Loop)','Shanghai','[[31.2398, 121.5022], [31.2289, 121.5384]]');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: road_events_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- T05 traffic-disruption candidates tied to specific commercial-fit-out
-- delivery / haul windows. All seeded inactive (active=0); the event
-- library activates them when the corresponding hold-window opens.

INSERT INTO road_events (event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
('re_seed_fitout_glass_partition_haul','rd_zhouhuan_pudong','2026-07-10T09:00:00+08:00','2026-07-10T11:00:00+08:00','heavy_traffic',0.5,'Seeded heavy-traffic window overlapping 光晟 glass-partition delivery to Lujiazui 4F. Combine with weather check.',0),
('re_seed_fitout_furniture_haul','rd_neihuan_pudong','2026-07-12T07:00:00+08:00','2026-07-12T09:30:00+08:00','heavy_traffic',0.4,'Seeded weekend-morning queue overlapping 爱仕 office-furniture delivery for 30 workstations + 2 meeting rooms.',0),
('re_seed_fitout_fire_dept_visit','rd_jingan_corridor','2026-07-14T08:30:00+08:00','2026-07-14T10:30:00+08:00','heavy_traffic',0.5,'Seeded morning queue on Jingan corridor as 静安区 消防救援支队 arrives for on-site fire-acceptance inspection D13.',0);

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: transit_events_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;
-- Commercial fit-out has no transit lines; placeholder kept to satisfy schema.
COMMIT;

