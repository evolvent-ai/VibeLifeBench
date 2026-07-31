-- Mutation SQL
UPDATE rate_plans SET inventory_remaining=0 WHERE hotel_id='hotel_jardin_tranquilo' AND date BETWEEN '2026-08-16' AND '2026-08-23' AND flavor='flex';
UPDATE rate_plans SET inventory_remaining=2 WHERE hotel_id='hotel_cerro_verde' AND date BETWEEN '2026-08-16' AND '2026-08-23' AND flavor='flex';
UPDATE rate_plans SET nightly_price=nightly_price-35 WHERE hotel_id='hotel_malecon_central' AND flavor='prepaid';
