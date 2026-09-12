-- Public geographic anchors are based on the source ledger; company/vendor records are synthetic.
INSERT INTO places
(place_id, name, category, lat, lng, country, city, rating, price_level, hours_json, phone, website, formatted)
VALUES
('pl_gz_office', 'event detailsinevent details（Dongfeng Middle Road）', 'office', 23.134200, 113.267300, 'CN', 'Guangzhou', 4.4, 0, '{"mon_fri":"08:30-19:00","sat":"closed","sun":"closed"}', '020-8330-6016', '', 'Yuexiu District, GuangzhouDongfeng Middle Roadevent details16event details'),
('pl_yuexiu_route', 'historic Yuexiubilingualcultureevent detailsassemblyinevent details', 'culture', 23.128550, 113.263900, 'CN', 'Guangzhou', 4.7, 0, '{"daily":"08:30-18:00","group_checkin":"reservationevent details"}', '020-8330-7216', '', 'Yuexiu District, GuangzhouZhongshan Fifth Roadevent details18event details'),
('pl_dim_sum', 'Huifu East Road Lingnan Dim Sum Studio', 'restaurant', 23.121250, 113.265900, 'CN', 'Guangzhou', 4.6, 2, '{"daily":"10:00-14:30,17:00-21:00","group_meal":"reservationevent details"}', '020-8330-8116', '', 'Yuexiu District, GuangzhouHuifu East Roadevent details6event details'),
('pl_beijing_road', 'Beijing Roadevent details', 'attraction', 23.123504, 113.263863, 'CN', 'Guangzhou', 4.5, 1, '{"daily":"open_area"}', '', 'https://www.gz.gov.cn/', 'Yuexiu District, GuangzhouBeijing Roadevent details'),
('pl_memorial_hall', 'inevent details', 'attraction', 23.135592, 113.259326, 'CN', 'Guangzhou', 4.7, 1, '{"daily":"09:00-17:30","last_entry":"17:00"}', '', 'https://www.gz.gov.cn/', 'Yuexiu District, GuangzhouDongfeng Middle Road299event details'),
('pl_nanyue_king_museum', 'event details', 'museum', 23.140693, 113.255626, 'CN', 'Guangzhou', 4.7, 1, '{"tue_sun":"09:00-17:30","mon":"closed_except_holidays"}', '', 'https://www.gz.gov.cn/', 'Yuexiu District, Guangzhouevent details867event details'),
('pl_yuexiu_park', 'Yuexiuevent details', 'park', 23.142514, 113.260408, 'CN', 'Guangzhou', 4.6, 0, '{"daily":"06:00-22:00"}', '', 'https://www.gz.gov.cn/', 'Yuexiu District, Guangzhouevent details988event details'),
('pl_peasant_institute', 'event details', 'museum', 23.129195, 113.270205, 'CN', 'Guangzhou', 4.6, 0, '{"tue_sun":"09:00-17:30","mon":"closed"}', '', 'https://www.gz.gov.cn/', 'Yuexiu District, Guangzhouinevent details42event details'),
('pl_guangxiao_temple', 'event details', 'attraction', 23.131917, 113.251193, 'CN', 'Guangzhou', 4.6, 1, '{"daily":"06:30-17:30"}', '', '', 'Yuexiu District, Guangzhouevent details109event details'),
('pl_revolution_museum', 'event details', 'museum', 23.131190, 113.278059, 'CN', 'Guangzhou', 4.5, 0, '{"tue_sun":"09:00-17:30","mon":"closed"}', '', 'https://www.gz.gov.cn/', 'Yuexiu District, Guangzhouevent details2event details'),
('pl_gongyuanqian_station', 'event details', 'station', 23.128100, 113.258850, 'CN', 'Guangzhou', 4.3, 0, '{"daily":"06:10-23:50"}', '', 'https://www.gzmtr.com/', 'Yuexiu District, GuangzhouZhongshan Fifth RoadGongyuanqian Station'),
('pl_beijinglu_station', 'Beijing Roadevent details', 'station', 23.121639, 113.265022, 'CN', 'Guangzhou', 4.2, 0, '{"daily":"06:10-23:50"}', '', 'https://www.gzmtr.com/', 'Yuexiu District, Guangzhouevent detailsBeijing Roadevent details'),
('pl_yuexiu_park_station', 'Yuexiuevent details', 'station', 23.142452, 113.256077, 'CN', 'Guangzhou', 4.2, 0, '{"daily":"06:10-23:50"}', '', 'https://www.gzmtr.com/', 'Yuexiu District, Guangzhouevent detailsYuexiuevent details'),
('pl_accessible_indoor_backup', 'event detailsoral historyaccessibleevent details', 'venue', 23.129820, 113.266120, 'CN', 'Guangzhou', 4.4, 1, '{"mon_sat":"09:00-18:00","sun":"reservation_only"}', '020-8330-7316', '', 'Yuexiu District, Guangzhouinevent details9event details'),
('pl_coach_pickup', 'event detailsteamevent details', 'transport', 23.133520, 113.260820, 'CN', 'Guangzhou', 4.0, 0, '{"daily":"07:00-20:00","coach_stop":"10_minutes_max"}', '', '', 'Yuexiu District, Guangzhouevent detailsteamtemporaryevent details'),
('pl_lunch_backup', 'Wenming Road Halal Cantonese Backup Restaurant', 'restaurant', 23.126800, 113.268800, 'CN', 'Guangzhou', 4.3, 2, '{"daily":"11:00-14:30,17:00-21:00"}', '020-8330-8216', '', 'Yuexiu District, GuangzhouWenming Roadevent details21event details'),
('pl_memorial_first_aid', 'event detailsemergencyserviceevent details', 'clinic', 23.134780, 113.260180, 'CN', 'Guangzhou', 4.1, 0, '{"daily":"08:00-20:00"}', '020-8330-9916', '', 'Yuexiu District, Guangzhouevent detailsemergencyserviceevent details'),
('pl_sun_yatsen_memorial_hospital', 'event details', 'hospital', 23.112370, 113.250637, 'CN', 'Guangzhou', 4.4, 0, '{"emergency":"24h"}', '', '', 'Yuexiu District, Guangzhouevent details107event details'),
('pl_accessible_rest_stop', 'event detailsaccessiblerest stops', 'public_service', 23.129050, 113.261900, 'CN', 'Guangzhou', 4.2, 0, '{"daily":"07:00-22:00"}', '', '', 'Yuexiu District, Guangzhouevent detailsaccessibleserviceevent details');

INSERT INTO place_reviews(place_id, author, rating, text, time) VALUES
('pl_yuexiu_route', 'event detailscultureprojectevent details', 5, 'bilingualassemblyevent detailsandgroupingcheck-inevent details；event detailsmemberevent details，event detailsteammustevent detailsevent dayevent detailsconstructionevent details。', '2026-05-18T10:20:00+08:00'),
('pl_yuexiu_route', 'administrationeventpost-event review', 4, '33 peopleevent detailscheck-inevent details，event details，event detailsindoorbackup planevent details。', '2026-06-03T16:40:00+08:00'),
('pl_dim_sum', 'event detailsprocurement', 4, 'event detailsandprovidepork-freeevent details；event detailsingredientsevent detailswritten confirmation，cannotonlyevent details。', '2026-05-26T14:15:00+08:00'),
('pl_dim_sum', 'event detailsteamevent details', 5, 'Englishmenuevent detailsprovide，kitchenevent details，suggestevent detailsbilingualevent detailsandoneevent details。', '2026-06-11T11:05:00+08:00'),
('pl_beijing_road', 'cityevent details', 4, 'event detailscultureevent detailsin，event detailsincrease；event detailstaskevent detailsclarifyassemblytimeandevent details。', '2026-04-19T18:30:00+08:00'),
('pl_memorial_hall', 'event detailseventevent details', 5, 'event detailsandevent details，teamevent detailscannotevent details，event detailsconfirmationindoorevent details。', '2026-05-09T09:50:00+08:00'),
('pl_nanyue_king_museum', 'event detailsrouteevent details', 5, 'indoorevent detailsextreme heatevent details，teamevent detailsandevent detailsreservation；event detailsmustevent detailsconfirmation。', '2026-06-14T13:00:00+08:00'),
('pl_yuexiu_park', 'event details', 4, 'event detailssteps，wheelchair routecannotevent detailsroute，event detailsweatherevent details。', '2026-05-30T08:45:00+08:00'),
('pl_peasant_institute', 'onboarding new colleaguesprojectevent details', 5, 'Chinese-English bilingualtaskevent details；entranceevent detailson-siteevent details。', '2026-06-08T15:25:00+08:00'),
('pl_guangxiao_temple', 'cultureevent details', 4, 'event details，event details；event detailsdetailsevent details、event detailsandevent details。', '2026-04-27T12:10:00+08:00'),
('pl_revolution_museum', 'event detailsteam', 4, 'event detailscontentevent detailsorganizational belongingevent details，33 peopleevent details，suggestevent details。', '2026-06-16T10:35:00+08:00'),
('pl_gongyuanqian_station', 'accessibleevent details', 4, 'event details，event detailsofevent details；assemblynotificationmustevent detailsandevent detailstime。', '2026-06-21T17:40:00+08:00'),
('pl_accessible_indoor_backup', 'riskevent details', 4, 'event details36event detailsandevent detailsaccessiblerestroom，event detailsorextreme heatde-escalation；cateringonlyevent detailsverifyevent details。', '2026-06-25T11:30:00+08:00'),
('pl_lunch_backup', 'event details', 4, 'event detailsinvoice made out to the companyevent detailsdepositevent details；event detailscapacityevent details33 people，onlyevent detailsbackup plan。', '2026-06-28T19:05:00+08:00');

INSERT INTO roads(road_id, name, city, geom_json) VALUES
('road_yuexiu_walk', 'YuexiuDongfeng Middle Road—Zhongshan Fifth Roadteamevent details', 'Guangzhou', '[[23.134200,113.267300],[23.132200,113.266600],[23.130200,113.265100],[23.128550,113.263900]]'),
('road_beijing_accessible', 'event details—Beijing Roadaccessibleevent details', 'Guangzhou', '[[23.128100,113.258850],[23.127200,113.261500],[23.125300,113.263200],[23.123504,113.263863]]'),
('road_memorial_detour', 'event details—event detailsteamevent details', 'Guangzhou', '[[23.135592,113.259326],[23.134780,113.260180],[23.133520,113.260820]]'),
('road_lunch_walk', 'Beijing Road—Huifu East Roadevent details', 'Guangzhou', '[[23.123504,113.263863],[23.122600,113.264800],[23.121250,113.265900]]');

INSERT INTO road_events(event_id, road_id, start_dt, end_dt, kind, magnitude, note, active) VALUES
('rdevt_gz_memorial_work_qnra', 'road_memorial_detour', '2026-05-14T08:00:00+08:00', '2026-05-14T18:00:00+08:00', 'closure', 0.4, 'event detailsemergencyevent details，event detailsroute。', 0);

INSERT INTO transit_stops(stop_id, name, lat, lng, city) VALUES
('stop_gongyuanqian', 'Gongyuanqian Station', 23.128100, 113.258850, 'Guangzhou'),
('stop_beijinglu', 'Beijing Roadevent details', 23.121639, 113.265022, 'Guangzhou'),
('stop_yuexiu_park', 'Yuexiuevent details', 23.142452, 113.256077, 'Guangzhou'),
('stop_peasant_institute', 'event details', 23.129195, 113.270205, 'Guangzhou');

INSERT INTO transit_lines(line_id, name, mode, operator, segment_minutes_json) VALUES
('line_gz_1', 'Guangzhouevent details1event details', 'subway', 'Guangzhouevent details', '{"default":3}'),
('line_gz_2', 'Guangzhouevent details2event details', 'subway', 'Guangzhouevent details', '{"default":4}'),
('line_gz_6', 'Guangzhouevent details6event details', 'subway', 'Guangzhouevent details', '{"default":3}');

INSERT INTO transit_schedule(line_id, stop_id, direction, stop_seq, time) VALUES
('line_gz_1', 'stop_gongyuanqian', 'Guangzhouevent details', 1, '08:42'),
('line_gz_1', 'stop_peasant_institute', 'Guangzhouevent details', 2, '08:45'),
('line_gz_1', 'stop_peasant_institute', 'event details', 1, '17:32'),
('line_gz_1', 'stop_gongyuanqian', 'event details', 2, '17:35'),
('line_gz_2', 'stop_yuexiu_park', 'Guangzhouevent details', 1, '08:35'),
('line_gz_2', 'stop_gongyuanqian', 'Guangzhouevent details', 2, '08:39'),
('line_gz_2', 'stop_gongyuanqian', 'event details', 1, '17:28'),
('line_gz_2', 'stop_yuexiu_park', 'event details', 2, '17:32'),
('line_gz_6', 'stop_beijinglu', 'event details', 1, '09:03'),
('line_gz_6', 'stop_beijinglu', 'event details', 1, '17:46');

INSERT INTO transit_events(event_id, line_id, stop_id, start_dt, end_dt, kind, note, active) VALUES
('txevt_gz_liftmaint_bkra', NULL, 'stop_gongyuanqian', '2026-06-02T09:00:00+08:00', '2026-06-02T16:00:00+08:00', 'delayed', 'event details；event dayevent detailsreviewaccessibleevent details。', 0);

-- Earlier Guangzhou cross-cultural program records
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_yuexiu_library_nq', 'Yuexiu Districtevent details', 'library', 23.1248, 113.2743, 'CN', 'Guangzhou', 4.5, 1, '{"mon":"closed","tue-sun":"09:00-18:00"}', '020-8382-1047', NULL, 'Yuexiu DistrictWenming Roadevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_memorial_east_ramp_vk', 'event detailsentrance', 'accessible_entrance', 23.1372, 113.2597, 'CN', 'Guangzhou', 4.2, 1, '{"daily":"07:30-18:30"}', NULL, NULL, 'Yuexiu DistrictDongfeng Middle Roadevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_dongshan_artroom_bm', 'event details', 'community_center', 23.1231, 113.2954, 'CN', 'Guangzhou', 4.3, 1, '{"tue-sun":"10:00-20:00"}', '020-8765-3092', NULL, 'Yuexiu Districtevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_huifu_foodlab_jr', 'Huifu East Roadcateringevent details', 'cooking_school', 23.1178, 113.2711, 'CN', 'Guangzhou', 4.6, 2, '{"daily":"09:30-21:00"}', '020-8334-6618', NULL, 'Yuexiu DistrictHuifu East Roadevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_beijinglu_print_fs', 'Beijing Roadbilingualevent details', 'printing', 23.1206, 113.2704, 'CN', 'Guangzhou', 4.1, 1, '{"weekday":"08:30-20:30"}', '020-8332-4097', NULL, 'Yuexiu DistrictBeijing Roadevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_haizhu_busbay_tc', 'event details', 'bus_stop', 23.1142, 113.2658, 'CN', 'Guangzhou', 3.9, 1, '{"daily":"06:00-23:00"}', NULL, NULL, 'Yuexiu Districtevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_liurong_workshop_xp', 'event details', 'cultural_center', 23.1288, 113.2614, 'CN', 'Guangzhou', 4.4, 2, '{"wed-sun":"10:00-17:30"}', '020-8107-5281', NULL, 'Yuexiu Districtevent details');
INSERT INTO "places" ('place_id', 'name', 'category', 'lat', 'lng', 'country', 'city', 'rating', 'price_level', 'hours_json', 'phone', 'website', 'formatted') VALUES ('pl_gz_dongfeng_clinic_qa', 'Dongfeng Middle Roadevent details', 'clinic', 23.1341, 113.2785, 'CN', 'Guangzhou', 4.0, 1, '{"daily":"08:00-21:30"}', '020-8356-1204', NULL, 'Yuexiu DistrictDongfeng Middle Road');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (91, 'pl_gz_yuexiu_library_nq', 'route_planner', 5, 'event detailsandevent details，event details。event details，event detailsneedreservation。', '2026-04-03T12:19:00+08:00');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (97, 'pl_gz_memorial_east_ramp_vk', 'access_reviewer', 4, 'event details，event details；eventevent details。', '2026-02-15T10:44:00+08:00');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (106, 'pl_gz_dongshan_artroom_bm', 'community_host', 3, 'event details，event details。event details，event details。', '2026-06-03T09:31:00+08:00');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (118, 'pl_gz_huifu_foodlab_jr', 'food_ops', 5, 'ingredientsevent detailsinevent details，event detailsequipment。event detailslockevent details。', '2026-05-10T14:06:00+08:00');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (124, 'pl_gz_beijinglu_print_fs', 'localization', 4, 'event detailsEnglishtaskevent details；proper namesevent detailsneedevent details。', '2026-03-12T16:28:00+08:00');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (139, 'pl_gz_haizhu_busbay_tc', 'driver_coordinator', 3, 'event details，event detailstemporary parkingevent details。event detailsneedevent details。', '2026-05-09T08:52:00+08:00');
INSERT INTO "place_reviews" ('id', 'place_id', 'author', 'rating', 'text', 'time') VALUES (147, 'pl_gz_liurong_workshop_xp', 'learning_partner', 4, 'event detailsEnglishevent details，event details；event details。', '2026-01-30T17:16:00+08:00');
INSERT INTO "roads" ('road_id', 'name', 'city', 'geom_json') VALUES ('rd_gz_wenming_west_hk', 'Wenming Roadevent details', 'Guangzhou', '{"type":"LineString","coordinates":[[113.2708,23.1250],[113.2761,23.1246]]}');
INSERT INTO "roads" ('road_id', 'name', 'city', 'geom_json') VALUES ('rd_gz_dongfeng_service_pv', 'Dongfeng Middle Roadevent details', 'Guangzhou', '{"type":"LineString","coordinates":[[113.2672,23.1368],[113.2802,23.1344]]}');
INSERT INTO "road_events" ('event_id', 'road_id', 'start_dt', 'end_dt', 'kind', 'magnitude', 'note', 'active') VALUES ('rdevt_gz_wenming_resurface_ns', 'rd_gz_wenming_west_hk', '2026-03-10T22:20:00+08:00', '2026-03-13T05:40:00+08:00', 'heavy_traffic', 0.35, 'event details，constructionevent details。', 0);
INSERT INTO "road_events" ('event_id', 'road_id', 'start_dt', 'end_dt', 'kind', 'magnitude', 'note', 'active') VALUES ('rdevt_gz_dongfeng_crane_wd', 'rd_gz_dongfeng_service_pv', '2026-05-16T06:30:00+08:00', '2026-05-16T11:20:00+08:00', 'closure', 0.8, 'equipmentevent details，event detailstemporaryevent details。', 0);
INSERT INTO "transit_events" ('event_id', 'line_id', 'stop_id', 'start_dt', 'end_dt', 'kind', 'note', 'active') VALUES ('txevt_gz_line1_signal_ct', 'line_gz_1', 'stop_peasant_institute', '2026-04-18T14:10:00+08:00', '2026-04-18T15:05:00+08:00', 'delayed', 'event details，event details。', 0);
INSERT INTO "notifications" ('created_at', 'channel', 'payload_json') VALUES ('2026-05-16T11:42:00+08:00', 'operations', '{"title":"Dongfeng Middle Roadevent details","body":"event details，event detailstemporary parkingevent details。"}');
