-- Minimal public fixture for currency and scenario-clock regression tests.
PRAGMA foreign_keys = ON;
BEGIN;

INSERT INTO hotels (
  hotel_id, name, city, district, geo_lat, geo_lng, star_rating,
  user_rating, user_rating_count, amenities_json, address_json,
  policies_json, description, capacity_estimate
) VALUES (
  'htl_cd_chunxi_courtyard',
  '春熙庭院酒店',
  '成都',
  '春熙路',
  30.658,
  104.079,
  4,
  9.1,
  1260,
  '["wifi","breakfast","desk","laundry"]',
  '{"street":"春熙路","city":"成都","district":"春熙路"}',
  '{"check_in":"15:00","check_out":"12:00"}',
  'Self-contained Hotel mock regression fixture.',
  30
);

INSERT INTO rate_plans (
  hotel_id, date, room_type, flavor, nightly_price, currency,
  inventory_remaining, inventory_capacity, cancellation_policy,
  refundable_until, breakfast_included, max_occupancy
) VALUES
  ('htl_cd_chunxi_courtyard', '2026-08-10', 'superior_king', 'flex', 520, 'CNY', 6, 10, 'Free cancellation through the listed deadline; first-night penalty afterward', '2026-08-08T18:00:00+08:00', 1, 2),
  ('htl_cd_chunxi_courtyard', '2026-08-11', 'superior_king', 'flex', 520, 'CNY', 6, 10, 'Free cancellation through the listed deadline; first-night penalty afterward', '2026-08-08T18:00:00+08:00', 1, 2),
  ('htl_cd_chunxi_courtyard', '2026-08-12', 'superior_king', 'flex', 520, 'CNY', 6, 10, 'Free cancellation through the listed deadline; first-night penalty afterward', '2026-08-08T18:00:00+08:00', 1, 2),
  ('htl_cd_chunxi_courtyard', '2026-08-13', 'superior_king', 'flex', 520, 'CNY', 6, 10, 'Free cancellation through the listed deadline; first-night penalty afterward', '2026-08-08T18:00:00+08:00', 1, 2);

INSERT INTO scenario_clock (clock_id, scenario_date)
VALUES ('default', '2026-07-23');

INSERT INTO _counters (name, value) VALUES
  ('reservation_seq', 0),
  ('ticket_seq', 0);

COMMIT;
