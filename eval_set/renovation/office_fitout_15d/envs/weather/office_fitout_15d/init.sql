-- ──────────────────────────────────────────────────────────
-- source: climate_profiles_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

INSERT INTO climate_profiles (profile_id,seasonal_temp_means_json,precip_freq_json,wind_baseline_kmh,humidity_baseline_pct,aqi_baseline_json,notes) VALUES
('early_summer_shanghai','{"6":{"tmin":22,"tmax":29},"7":{"tmin":26,"tmax":33},"8":{"tmin":27,"tmax":34}}','{"6":{"rain_days":12},"7":{"rain_days":10},"8":{"rain_days":8}}',14.0,78.0,'{"aqi":75,"dominant":"pm25"}','Early-summer Shanghai (Pudong) profile: humid + intermittent rain Jun-Jul, hot + sporadic showers Aug, elevated AQI window 08-15..08-22 for paint VOC dissipation.');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: locations_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

INSERT INTO locations (geo_key,city,country,lat,lng,timezone,climate_profile_id,kind) VALUES
('shanghai_pudong','Shanghai','CN',31.224,121.5275,'Asia/Shanghai','early_summer_shanghai','district');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: daily_weather_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- Daily weather rows for D0..D86 (2026-06-01..2026-08-25) at shanghai_pudong.
-- Based on early_summer_shanghai climate profile: warm + humid, rain windows
-- pinned to the schedule (waterproofing curing, cabinet delivery, etc.).

INSERT INTO daily_weather (geo_key,date,tmin,tmax,condition,precip_mm,precip_prob,wind_kmh) VALUES
('shanghai_pudong','2026-06-01',21,28,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-02',21,28,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-03',21,28,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-04',21,29,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-05',22,26,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-06',22,26,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-07',22,29,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-08',22,29,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-09',22,29,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-10',22,30,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-11',22,30,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-12',22,27,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-13',23,27,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-14',23,30,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-15',23,31,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-16',23,31,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-17',23,31,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-18',23,31,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-19',23,31,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-20',23,31,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-21',24,32,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-22',24,32,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-23',24,32,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-06-24',24,32,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-06-25',24,29,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-26',24,29,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-27',24,30,'rain',18.0,0.85,22),
('shanghai_pudong','2026-06-28',25,33,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-06-29',25,33,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-06-30',25,33,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-07-01',25,32,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-07-02',25,32,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-07-03',25,32,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-07-04',25,32,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-07-05',25,32,'cloudy',0.0,0.3,14),
('shanghai_pudong','2026-07-06',26,30,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-07',26,30,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-08',26,30,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-09',26,30,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-10',26,33,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-11',26,33,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-12',26,33,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-13',26,33,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-14',26,34,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-15',26,34,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-16',26,34,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-17',27,34,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-18',27,34,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-19',27,34,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-20',27,31,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-21',27,31,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-22',27,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-23',27,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-24',27,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-25',27,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-26',28,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-27',28,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-28',28,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-29',28,35,'partly_cloudy',0.0,0.15,14),
('shanghai_pudong','2026-07-30',28,32,'rain',18.0,0.85,22),
('shanghai_pudong','2026-07-31',28,33,'rain',18.0,0.85,22),
('shanghai_pudong','2026-08-01',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-02',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-03',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-04',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-05',26,31,'rain',18.0,0.85,22),
('shanghai_pudong','2026-08-06',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-07',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-08',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-09',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-10',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-11',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-12',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-13',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-14',26,31,'rain',18.0,0.85,22),
('shanghai_pudong','2026-08-15',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-16',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-17',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-18',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-19',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-20',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-21',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-22',26,31,'rain',18.0,0.85,22),
('shanghai_pudong','2026-08-23',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-24',26,34,'hot_hazy',0.0,0.15,14),
('shanghai_pudong','2026-08-25',26,34,'hot_hazy',0.0,0.15,14);

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: hourly_weather_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- Hourly weather rows pinned to rain windows: waterproofing curing (06-25..27),
-- mid-project (07-07), cabinet delivery storm (07-30), late-stage (08-22).

INSERT INTO hourly_weather (geo_key,datetime,temp_c,humidity,condition,precip_mm,wind_kmh) VALUES
('shanghai_pudong','2026-06-25T04:00:00+08:00',25,90,'drizzle',1.5,24),
('shanghai_pudong','2026-06-25T08:00:00+08:00',28,90,'rain',6.5,24),
('shanghai_pudong','2026-06-25T12:00:00+08:00',28,90,'rain',6.5,24),
('shanghai_pudong','2026-06-25T16:00:00+08:00',28,90,'rain',6.5,24),
('shanghai_pudong','2026-06-25T20:00:00+08:00',25,90,'drizzle',1.5,24),
('shanghai_pudong','2026-06-26T04:00:00+08:00',25,90,'drizzle',1.5,24),
('shanghai_pudong','2026-06-26T08:00:00+08:00',28,90,'rain',6.5,24),
('shanghai_pudong','2026-06-26T12:00:00+08:00',28,90,'rain',6.5,24),
('shanghai_pudong','2026-06-26T16:00:00+08:00',28,90,'rain',6.5,24),
('shanghai_pudong','2026-06-26T20:00:00+08:00',25,90,'drizzle',1.5,24),
('shanghai_pudong','2026-06-27T04:00:00+08:00',25,90,'drizzle',1.5,24),
('shanghai_pudong','2026-06-27T08:00:00+08:00',29,90,'rain',6.5,24),
('shanghai_pudong','2026-06-27T12:00:00+08:00',29,90,'rain',6.5,24),
('shanghai_pudong','2026-06-27T16:00:00+08:00',29,90,'rain',6.5,24),
('shanghai_pudong','2026-06-27T20:00:00+08:00',25,90,'drizzle',1.5,24),
('shanghai_pudong','2026-07-07T04:00:00+08:00',27,90,'drizzle',1.5,24),
('shanghai_pudong','2026-07-07T08:00:00+08:00',29,90,'rain',6.5,24),
('shanghai_pudong','2026-07-07T12:00:00+08:00',29,90,'rain',6.5,24),
('shanghai_pudong','2026-07-07T16:00:00+08:00',29,90,'rain',6.5,24),
('shanghai_pudong','2026-07-07T20:00:00+08:00',27,90,'drizzle',1.5,24),
('shanghai_pudong','2026-07-30T04:00:00+08:00',29,90,'drizzle',1.5,24),
('shanghai_pudong','2026-07-30T08:00:00+08:00',31,90,'rain',6.5,24),
('shanghai_pudong','2026-07-30T12:00:00+08:00',31,90,'rain',6.5,24),
('shanghai_pudong','2026-07-30T16:00:00+08:00',31,90,'rain',6.5,24),
('shanghai_pudong','2026-07-30T20:00:00+08:00',29,90,'drizzle',1.5,24),
('shanghai_pudong','2026-08-22T04:00:00+08:00',27,90,'drizzle',1.5,24),
('shanghai_pudong','2026-08-22T08:00:00+08:00',30,90,'rain',6.5,24),
('shanghai_pudong','2026-08-22T12:00:00+08:00',30,90,'rain',6.5,24),
('shanghai_pudong','2026-08-22T16:00:00+08:00',30,90,'rain',6.5,24),
('shanghai_pudong','2026-08-22T20:00:00+08:00',27,90,'drizzle',1.5,24);

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: aqi_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- Daily AQI rows. Baseline ~70 (early-summer Pudong); elevated 2026-08-15..
-- 2026-08-22 (130, unhealthy_for_sensitive) overlaps the paint VOC dissipation
-- window referenced by insp_std_010 / sm_010 paint AQI alert.

INSERT INTO daily_aqi (geo_key,date,aqi,category,dominant_pollutant,observed_at) VALUES
('shanghai_pudong','2026-06-01',75,'moderate','pm25','2026-06-01T09:00:00+08:00'),
('shanghai_pudong','2026-06-02',75,'moderate','pm25','2026-06-02T09:00:00+08:00'),
('shanghai_pudong','2026-06-03',75,'moderate','pm25','2026-06-03T09:00:00+08:00'),
('shanghai_pudong','2026-06-04',75,'moderate','pm25','2026-06-04T09:00:00+08:00'),
('shanghai_pudong','2026-06-05',55,'moderate','pm25','2026-06-05T09:00:00+08:00'),
('shanghai_pudong','2026-06-06',55,'moderate','pm25','2026-06-06T09:00:00+08:00'),
('shanghai_pudong','2026-06-07',75,'moderate','pm25','2026-06-07T09:00:00+08:00'),
('shanghai_pudong','2026-06-08',75,'moderate','pm25','2026-06-08T09:00:00+08:00'),
('shanghai_pudong','2026-06-09',75,'moderate','pm25','2026-06-09T09:00:00+08:00'),
('shanghai_pudong','2026-06-10',75,'moderate','pm25','2026-06-10T09:00:00+08:00'),
('shanghai_pudong','2026-06-11',75,'moderate','pm25','2026-06-11T09:00:00+08:00'),
('shanghai_pudong','2026-06-12',55,'moderate','pm25','2026-06-12T09:00:00+08:00'),
('shanghai_pudong','2026-06-13',55,'moderate','pm25','2026-06-13T09:00:00+08:00'),
('shanghai_pudong','2026-06-14',75,'moderate','pm25','2026-06-14T09:00:00+08:00'),
('shanghai_pudong','2026-06-15',75,'moderate','pm25','2026-06-15T09:00:00+08:00'),
('shanghai_pudong','2026-06-16',75,'moderate','pm25','2026-06-16T09:00:00+08:00'),
('shanghai_pudong','2026-06-17',75,'moderate','pm25','2026-06-17T09:00:00+08:00'),
('shanghai_pudong','2026-06-18',75,'moderate','pm25','2026-06-18T09:00:00+08:00'),
('shanghai_pudong','2026-06-19',75,'moderate','pm25','2026-06-19T09:00:00+08:00'),
('shanghai_pudong','2026-06-20',75,'moderate','pm25','2026-06-20T09:00:00+08:00'),
('shanghai_pudong','2026-06-21',75,'moderate','pm25','2026-06-21T09:00:00+08:00'),
('shanghai_pudong','2026-06-22',75,'moderate','pm25','2026-06-22T09:00:00+08:00'),
('shanghai_pudong','2026-06-23',75,'moderate','pm25','2026-06-23T09:00:00+08:00'),
('shanghai_pudong','2026-06-24',75,'moderate','pm25','2026-06-24T09:00:00+08:00'),
('shanghai_pudong','2026-06-25',55,'moderate','pm25','2026-06-25T09:00:00+08:00'),
('shanghai_pudong','2026-06-26',55,'moderate','pm25','2026-06-26T09:00:00+08:00'),
('shanghai_pudong','2026-06-27',55,'moderate','pm25','2026-06-27T09:00:00+08:00'),
('shanghai_pudong','2026-06-28',75,'moderate','pm25','2026-06-28T09:00:00+08:00'),
('shanghai_pudong','2026-06-29',75,'moderate','pm25','2026-06-29T09:00:00+08:00'),
('shanghai_pudong','2026-06-30',75,'moderate','pm25','2026-06-30T09:00:00+08:00'),
('shanghai_pudong','2026-07-01',75,'moderate','pm25','2026-07-01T09:00:00+08:00'),
('shanghai_pudong','2026-07-02',75,'moderate','pm25','2026-07-02T09:00:00+08:00'),
('shanghai_pudong','2026-07-03',75,'moderate','pm25','2026-07-03T09:00:00+08:00'),
('shanghai_pudong','2026-07-04',75,'moderate','pm25','2026-07-04T09:00:00+08:00'),
('shanghai_pudong','2026-07-05',75,'moderate','pm25','2026-07-05T09:00:00+08:00'),
('shanghai_pudong','2026-07-06',55,'moderate','pm25','2026-07-06T09:00:00+08:00'),
('shanghai_pudong','2026-07-07',55,'moderate','pm25','2026-07-07T09:00:00+08:00'),
('shanghai_pudong','2026-07-08',55,'moderate','pm25','2026-07-08T09:00:00+08:00'),
('shanghai_pudong','2026-07-09',55,'moderate','pm25','2026-07-09T09:00:00+08:00'),
('shanghai_pudong','2026-07-10',75,'moderate','pm25','2026-07-10T09:00:00+08:00'),
('shanghai_pudong','2026-07-11',75,'moderate','pm25','2026-07-11T09:00:00+08:00'),
('shanghai_pudong','2026-07-12',75,'moderate','pm25','2026-07-12T09:00:00+08:00'),
('shanghai_pudong','2026-07-13',75,'moderate','pm25','2026-07-13T09:00:00+08:00'),
('shanghai_pudong','2026-07-14',75,'moderate','pm25','2026-07-14T09:00:00+08:00'),
('shanghai_pudong','2026-07-15',75,'moderate','pm25','2026-07-15T09:00:00+08:00'),
('shanghai_pudong','2026-07-16',75,'moderate','pm25','2026-07-16T09:00:00+08:00'),
('shanghai_pudong','2026-07-17',75,'moderate','pm25','2026-07-17T09:00:00+08:00'),
('shanghai_pudong','2026-07-18',75,'moderate','pm25','2026-07-18T09:00:00+08:00'),
('shanghai_pudong','2026-07-19',75,'moderate','pm25','2026-07-19T09:00:00+08:00'),
('shanghai_pudong','2026-07-20',55,'moderate','pm25','2026-07-20T09:00:00+08:00'),
('shanghai_pudong','2026-07-21',55,'moderate','pm25','2026-07-21T09:00:00+08:00'),
('shanghai_pudong','2026-07-22',75,'moderate','pm25','2026-07-22T09:00:00+08:00'),
('shanghai_pudong','2026-07-23',75,'moderate','pm25','2026-07-23T09:00:00+08:00'),
('shanghai_pudong','2026-07-24',75,'moderate','pm25','2026-07-24T09:00:00+08:00'),
('shanghai_pudong','2026-07-25',75,'moderate','pm25','2026-07-25T09:00:00+08:00'),
('shanghai_pudong','2026-07-26',75,'moderate','pm25','2026-07-26T09:00:00+08:00'),
('shanghai_pudong','2026-07-27',75,'moderate','pm25','2026-07-27T09:00:00+08:00'),
('shanghai_pudong','2026-07-28',75,'moderate','pm25','2026-07-28T09:00:00+08:00'),
('shanghai_pudong','2026-07-29',75,'moderate','pm25','2026-07-29T09:00:00+08:00'),
('shanghai_pudong','2026-07-30',55,'moderate','pm25','2026-07-30T09:00:00+08:00'),
('shanghai_pudong','2026-07-31',55,'moderate','pm25','2026-07-31T09:00:00+08:00'),
('shanghai_pudong','2026-08-01',75,'moderate','pm25','2026-08-01T09:00:00+08:00'),
('shanghai_pudong','2026-08-02',75,'moderate','pm25','2026-08-02T09:00:00+08:00'),
('shanghai_pudong','2026-08-03',75,'moderate','pm25','2026-08-03T09:00:00+08:00'),
('shanghai_pudong','2026-08-04',75,'moderate','pm25','2026-08-04T09:00:00+08:00'),
('shanghai_pudong','2026-08-05',55,'moderate','pm25','2026-08-05T09:00:00+08:00'),
('shanghai_pudong','2026-08-06',75,'moderate','pm25','2026-08-06T09:00:00+08:00'),
('shanghai_pudong','2026-08-07',75,'moderate','pm25','2026-08-07T09:00:00+08:00'),
('shanghai_pudong','2026-08-08',75,'moderate','pm25','2026-08-08T09:00:00+08:00'),
('shanghai_pudong','2026-08-09',75,'moderate','pm25','2026-08-09T09:00:00+08:00'),
('shanghai_pudong','2026-08-10',75,'moderate','pm25','2026-08-10T09:00:00+08:00'),
('shanghai_pudong','2026-08-11',75,'moderate','pm25','2026-08-11T09:00:00+08:00'),
('shanghai_pudong','2026-08-12',75,'moderate','pm25','2026-08-12T09:00:00+08:00'),
('shanghai_pudong','2026-08-13',75,'moderate','pm25','2026-08-13T09:00:00+08:00'),
('shanghai_pudong','2026-08-14',55,'moderate','pm25','2026-08-14T09:00:00+08:00'),
('shanghai_pudong','2026-08-15',130,'unhealthy_for_sensitive','pm25','2026-08-15T09:00:00+08:00'),
('shanghai_pudong','2026-08-16',130,'unhealthy_for_sensitive','pm25','2026-08-16T09:00:00+08:00'),
('shanghai_pudong','2026-08-17',130,'unhealthy_for_sensitive','pm25','2026-08-17T09:00:00+08:00'),
('shanghai_pudong','2026-08-18',130,'unhealthy_for_sensitive','pm25','2026-08-18T09:00:00+08:00'),
('shanghai_pudong','2026-08-19',130,'unhealthy_for_sensitive','pm25','2026-08-19T09:00:00+08:00'),
('shanghai_pudong','2026-08-20',130,'unhealthy_for_sensitive','pm25','2026-08-20T09:00:00+08:00'),
('shanghai_pudong','2026-08-21',130,'unhealthy_for_sensitive','pm25','2026-08-21T09:00:00+08:00'),
('shanghai_pudong','2026-08-22',130,'unhealthy_for_sensitive','pm25','2026-08-22T09:00:00+08:00'),
('shanghai_pudong','2026-08-23',75,'moderate','pm25','2026-08-23T09:00:00+08:00'),
('shanghai_pudong','2026-08-24',75,'moderate','pm25','2026-08-24T09:00:00+08:00'),
('shanghai_pudong','2026-08-25',75,'moderate','pm25','2026-08-25T09:00:00+08:00');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: alerts_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;

-- Alerts seeded INACTIVE (active=0) at t0. The admin lifecycle / event
-- library activates them when the corresponding sim window arrives.
-- alt_waterproof_rain_seed:   2026-06-25..27 rain overlaps waterproof curing.
-- alt_cabinet_delivery_storm_seed: 2026-07-30 storm overlaps cabinet delivery.
-- alt_paint_aqi_voc_seed:     2026-08-15..22 elevated AQI for paint VOC.

INSERT INTO alerts (alert_id,kind,severity,start_dt,end_dt,areas_json,description,active,created_at,source_event) VALUES
('alt_waterproof_rain_seed','heavy_rain','advisory','2026-06-25T12:00:00+08:00','2026-06-27T06:00:00+08:00','["shanghai_pudong"]','Rain during waterproofing curing window; re-check before scheduling closed-water test 2026-06-26..27.',0,'2026-06-01T00:00:00+08:00','seed'),
('alt_cabinet_delivery_storm_seed','thunderstorm','advisory','2026-07-30T08:00:00+08:00','2026-07-30T22:00:00+08:00','["shanghai_pudong"]','Storm overlapping cabinet delivery window (hold_modulux_cab_01); combine with re_seed_cabinet_haul_pudong_traffic.',0,'2026-06-01T00:00:00+08:00','seed'),
('alt_paint_aqi_voc_seed','poor_air_quality','advisory','2026-08-15T00:00:00+08:00','2026-08-22T23:59:00+08:00','["shanghai_pudong"]','Elevated outdoor AQI during indoor paint VOC dissipation window; agent must consider insp_std_010 and insp_std_011 ventilation requirements before move-in.',0,'2026-06-01T00:00:00+08:00','seed');

COMMIT;

-- ──────────────────────────────────────────────────────────
-- source: typhoon_tracks_seed.sql
-- ──────────────────────────────────────────────────────────
BEGIN TRANSACTION;
-- No typhoon tracks seeded; June-July typhoon possible but kept empty per BASE_ENV_SCHEMA.
COMMIT;

