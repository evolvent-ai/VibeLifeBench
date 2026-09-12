PRAGMA journal_mode = DELETE;
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
('pl_zhou_mu_office','Pudong Lujiazui Financial Center 4F CN-text (300sqm fit-up)','office_space',31.2398,121.5022,'CN','Shanghai',NULL,NULL,'{"monday": {"open": "00:00", "close": "23:59"}, "tuesday": {"open": "00:00", "close": "23:59"}, "wednesday": {"open": "00:00", "close": "23:59"}, "thursday": {"open": "00:00", "close": "23:59"}, "friday": {"open": "00:00", "close": "23:59"}, "saturday": {"open": "00:00", "close": "23:59"}, "sunday": {"open": "00:00", "close": "23:59"}}',NULL,NULL,'ShanghaiCN-termPudong New AreaPudong Lujiazui Financial Center 4 floor (commercial fit-up anchor)'),
('pl_lujiazui_fc_property','Pudong Lujiazui Financial Centerproperty managementservice center','property_office',31.2401,121.5018,'CN','Shanghai',4.6,3,'{"monday": {"open": "08:30", "close": "20:00"}, "tuesday": {"open": "08:30", "close": "20:00"}, "wednesday": {"open": "08:30", "close": "20:00"}, "thursday": {"open": "08:30", "close": "20:00"}, "friday": {"open": "08:30", "close": "20:00"}, "saturday": {"open": "09:00", "close": "18:00"}, "sunday": {"open": "09:00", "close": "18:00"}}','+86-21-5588-3000','https://example.com/lujiazui-fc','ShanghaiCN-termPudong New AreaPudong Lujiazui Financial Center property managementservice center'),
('pl_jingan_fire_dept','Jingan Districtfire safetyCN-text CN-text','fire_dept',31.2278,121.4458,'CN','Shanghai',4.5,2,'{"monday": {"open": "08:30", "close": "17:30"}, "tuesday": {"open": "08:30", "close": "17:30"}, "wednesday": {"open": "08:30", "close": "17:30"}, "thursday": {"open": "08:30", "close": "17:30"}, "friday": {"open": "08:30", "close": "17:30"}, "saturday": {"closed": true}, "sunday": {"closed": true}}','+86-21-5588-9119','https://example.com/jingan-fire','ShanghaiCN-termJingan District fire safetyCN-text'),
('pl_huan_commercial_office','CN-textdesign CN-textcenter','commercial_design_build',31.2272,121.4458,'CN','Shanghai',4.7,4,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9001','https://example.com/huan-commercial','ShanghaiCN-termJingan District CN-textdesigncenter (prov_v3_001_commercial_design_build)'),
('pl_shenpin_lujiazui_office','CN-textcommercial space LujiazuiCN-text','commercial_design_build',31.2406,121.5025,'CN','Shanghai',4.8,4,'{"monday": {"open": "09:00", "close": "19:00"}, "tuesday": {"open": "09:00", "close": "19:00"}, "wednesday": {"open": "09:00", "close": "19:00"}, "thursday": {"open": "09:00", "close": "19:00"}, "friday": {"open": "09:00", "close": "19:00"}, "saturday": {"open": "10:00", "close": "18:00"}, "sunday": {"closed": true}}','+86-21-5555-9002','https://example.com/shenpin-cs','ShanghaiCN-termPudong New Area LujiazuiCN-text (prov_v3_002_commercial_design_build)'),
('pl_lingchuang_beibund_office','CN-textworks CN-termoutsideCN-text','commercial_design_build',31.2491,121.5067,'CN','Shanghai',4.5,3,'{"monday": {"open": "08:30", "close": "18:00"}, "tuesday": {"open": "08:30", "close": "18:00"}, "wednesday": {"open": "08:30", "close": "18:00"}, "thursday": {"open": "08:30", "close": "18:00"}, "friday": {"open": "08:30", "close": "18:00"}, "saturday": {"open": "09:00", "close": "16:00"}, "sunday": {"closed": true}}','+86-21-5555-9003','https://example.com/lingchuang-cs','ShanghaiCN-text CN-termoutsideCN-text (prov_v3_003_commercial_design_build)'),
('pl_qihang_xinzhuang_office','CN-textdecorationcommercial CN-textcommercialCN-text','commercial_design_build',31.1133,121.3878,'CN','Shanghai',4.4,3,'{"monday": {"open": "09:00", "close": "18:00"}, "tuesday": {"open": "09:00", "close": "18:00"}, "wednesday": {"open": "09:00", "close": "18:00"}, "thursday": {"open": "09:00", "close": "18:00"}, "friday": {"open": "09:00", "close": "18:00"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9004','https://example.com/qihang-cs','ShanghaiCN-textlineCN-term CN-textcommercialCN-text (prov_v3_004_commercial_design_build)'),
('pl_addxieyi_julu_studio','ADDCN-textdesign CN-textdesignCN-text','commercial_design_build',31.2156,121.4533,'CN','Shanghai',4.9,5,'{"monday": {"open": "10:00", "close": "20:00"}, "tuesday": {"open": "10:00", "close": "20:00"}, "wednesday": {"open": "10:00", "close": "20:00"}, "thursday": {"open": "10:00", "close": "20:00"}, "friday": {"open": "10:00", "close": "20:00"}, "saturday": {"open": "11:00", "close": "18:00"}, "sunday": {"closed": true}}','+86-21-5555-9005','https://example.com/addxieyi','ShanghaiCN-termJingan District CN-textdesignCN-text (prov_v3_005_commercial_design_build)'),
('pl_boyuan_bund_design','CN-textdesign outsideCN-textdesignCN-term','commercial_design_build',31.2389,121.4901,'CN','Shanghai',4.6,4,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9007','https://example.com/boyuan-cs','ShanghaiCN-text outsideCN-textdesignCN-term (prov_v3_007_commercial_design_build)'),
('pl_hurui_zhenru_office','CN-textfit-out CN-text','commercial_design_build',31.2533,121.4078,'CN','Shanghai',4.2,3,'{"monday": {"open": "08:30", "close": "18:00"}, "tuesday": {"open": "08:30", "close": "18:00"}, "wednesday": {"open": "08:30", "close": "18:00"}, "thursday": {"open": "08:30", "close": "18:00"}, "friday": {"open": "08:30", "close": "18:00"}, "saturday": {"open": "09:00", "close": "16:00"}, "sunday": {"closed": true}}','+86-21-5555-9008','https://example.com/hurui-co','ShanghaiCN-text CN-text (prov_v3_008_commercial_design_build)'),
('pl_safehands_insurance_broker','CN-textinsurance broker PudongcommercialCN-term','insurance_broker',31.2356,121.5044,'CN','Shanghai',4.7,3,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9901','https://example.com/safehands-broker','ShanghaiCN-termPudong New Area CN-textinsurance broker commercialCN-term'),
('pl_chuanlian_iot_integrator','CN-text CN-text','smart_control_integrator',31.2114,121.5908,'CN','Shanghai',4.6,4,'{"monday": {"open": "09:00", "close": "18:30"}, "tuesday": {"open": "09:00", "close": "18:30"}, "wednesday": {"open": "09:00", "close": "18:30"}, "thursday": {"open": "09:00", "close": "18:30"}, "friday": {"open": "09:00", "close": "18:30"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9906','https://example.com/chuanlian-iot','ShanghaiCN-termPudong New Area CN-text (commercial smart-control integrator)'),
('pl_aishi_furniture_warehouse','CN-textfurniture commercialCN-term PudongCN-text','office_furniture_supplier',31.2266,121.5311,'CN','Shanghai',4.5,3,'{"monday": {"open": "08:30", "close": "18:00"}, "tuesday": {"open": "08:30", "close": "18:00"}, "wednesday": {"open": "08:30", "close": "18:00"}, "thursday": {"open": "08:30", "close": "18:00"}, "friday": {"open": "08:30", "close": "18:00"}, "saturday": {"open": "09:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9907','https://example.com/aishi-furniture','ShanghaiCN-termPudong New Area CN-textfurniture commercialCN-text'),
('pl_guangshen_glass_partition','CN-textcommercial PudongCN-text','glass_partition_supplier',31.2289,121.5384,'CN','Shanghai',4.6,3,'{"monday": {"open": "09:00", "close": "19:00"}, "tuesday": {"open": "09:00", "close": "19:00"}, "wednesday": {"open": "09:00", "close": "19:00"}, "thursday": {"open": "09:00", "close": "19:00"}, "friday": {"open": "09:00", "close": "19:00"}, "saturday": {"open": "10:00", "close": "18:00"}, "sunday": {"open": "10:00", "close": "16:00"}}','+86-21-5555-9905','https://example.com/guangshen-partition','ShanghaiCN-termPudong New Area CN-text CN-text'),
('pl_chanyi_supervision_office','CN-textNo.CN-textworksCN-text PudongCN-textoffice','third_party_supervision',31.2358,121.4977,'CN','Shanghai',4.8,3,'{"monday": {"open": "09:00", "close": "18:00"}, "tuesday": {"open": "09:00", "close": "18:00"}, "wednesday": {"open": "09:00", "close": "18:00"}, "thursday": {"open": "09:00", "close": "18:00"}, "friday": {"open": "09:00", "close": "18:00"}, "saturday": {"open": "10:00", "close": "17:00"}, "sunday": {"closed": true}}','+86-21-5555-9904','https://example.com/chanyi-supervision','ShanghaiCN-termPudong New Area PudongCN-text CN-text');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: roads_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- Shanghai expressway / arterial backbone connecting the Lujiazui anchor
-- (pl_zhou_mu_office) to vendor / property / regulator places.
-- Geometries are 2-point straight-line approximations.

INSERT INTO roads (road_id,name,city,geom_json) VALUES
('rd_neihuan_pudong','withinCN-termhighCN-text (Inner Ring East — Pudong)','Shanghai','[[31.2398, 121.5022], [31.2266, 121.5311]]'),
('rd_yan_an_elevated','CN-texthighCN-term (Yan_an Elevated — bund corridor)','Shanghai','[[31.2398, 121.5022], [31.2389, 121.4901]]'),
('rd_north_south_pudong','CN-texthighCN-term PudongCN-term (North-South Elevated Pudong)','Shanghai','[[31.2398, 121.5022], [31.2114, 121.5908]]'),
('rd_jingan_corridor','JinganCN-text CN-text','Shanghai','[[31.2272, 121.4458], [31.2156, 121.4533]]'),
('rd_zhouhuan_pudong','PudongCN-text (Pudong Loop)','Shanghai','[[31.2398, 121.5022], [31.2289, 121.5384]]');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: road_events_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- T05 traffic-disruption candidates tied to specific commercial-fit-out
-- delivery / haul windows. All seeded inactive (active=0); the event
-- library activates them when the corresponding hold-window opens.

INSERT INTO road_events (event_id,road_id,start_dt,end_dt,kind,magnitude,note,active) VALUES
('re_seed_fitout_glass_partition_haul','rd_zhouhuan_pudong','2026-07-10T09:00:00+08:00','2026-07-10T11:00:00+08:00','heavy_traffic',0.5,'Seeded heavy-traffic window overlapping CN-text glass-partition delivery to Lujiazui 4F. Combine with weather check.',0),
('re_seed_fitout_furniture_haul','rd_neihuan_pudong','2026-07-12T07:00:00+08:00','2026-07-12T09:30:00+08:00','heavy_traffic',0.4,'Seeded weekend-morning queue overlapping CN-text office-furniture delivery for 30 workstations + 2 meeting rooms.',0),
('re_seed_fitout_fire_dept_visit','rd_jingan_corridor','2026-07-14T08:30:00+08:00','2026-07-14T10:30:00+08:00','heavy_traffic',0.5,'Seeded morning queue on Jingan corridor as Jingan District fire safetyCN-text arrives for on-site fire-acceptance inspection D13.',0);

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: transit_events_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;
-- Commercial fit-out has no transit lines; placeholder kept to satisfy schema.
COMMIT;
