-- Stage 7 mutation: August inventory for Puerto Ayora and the two mainland
-- gateway cities is released. Before this the rate plans exist but at their
-- pre-release depth; this is the point at which the real August picture
-- (venue-area rooms scarce, prepaid stock cheaper, mainland airport hotels
-- plentiful) becomes visible to search_hotels.

-- Venue-area flexible stock thins out across the workshop nights.
UPDATE rate_plans
   SET inventory_remaining = 3
 WHERE hotel_id = 'hotel_jardin_tranquilo'
   AND date BETWEEN '2026-08-16' AND '2026-08-23'
   AND flavor = 'flex';

-- The pier-front property pushes its non-refundable stock instead.
UPDATE rate_plans
   SET inventory_remaining = 8, nightly_price = nightly_price - 18
 WHERE hotel_id = 'hotel_malecon_central'
   AND date BETWEEN '2026-08-16' AND '2026-08-23'
   AND flavor = 'prepaid';

-- Its own flexible rate is quietly withdrawn for the peak nights.
UPDATE rate_plans
   SET inventory_remaining = 0
 WHERE hotel_id = 'hotel_malecon_central'
   AND date BETWEEN '2026-08-17' AND '2026-08-22'
   AND flavor = 'flex';

-- Mainland airport hotels are not under pressure and stay open and refundable.
UPDATE rate_plans
   SET inventory_remaining = inventory_remaining + 4
 WHERE hotel_id IN ('hotel_guayaquil_aero','hotel_quito_terminal')
   AND date BETWEEN '2026-08-14' AND '2026-08-17'
   AND flavor = 'flex';
