-- Mutation SQL
UPDATE fare_buckets SET seats_remaining=12, price=price-80 WHERE flight_no IN ('UA858','CM473','CM159','LA1411');
UPDATE fare_buckets SET seats_remaining=3, price=price+60 WHERE flight_no IN ('CX368','CX315','IB6453');
