PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

INSERT INTO accounts (account_id, user_id, type, name, balance_minor, currency, opened_at, frozen) VALUES
('acct_zhangming_cny_checking', 'zhang_ming', 'checking', 'Business travel checking', 3285000, 'CNY', '2023-03-15T09:00:00+08:00', 0),
('acct_zhangming_jpy_wallet', 'zhang_ming', 'checking', 'Japan travel wallet', 120000, 'JPY', '2025-11-02T10:00:00+08:00', 0),
('acct_zhangming_hkd_wallet', 'zhang_ming', 'checking', 'Hong Kong transit wallet', 300000, 'HKD', '2025-06-18T10:00:00+08:00', 0),
('acct_zhangming_savings', 'zhang_ming', 'savings', 'Emergency savings', 8500000, 'CNY', '2020-08-01T09:00:00+08:00', 0);

INSERT INTO transactions (tx_id, account_id, posted_at, amount_minor, kind, counterparty, memo, balance_after_minor) VALUES
('tx_salary_june_credit', 'acct_zhangming_cny_checking', '2026-06-28T09:02:00+08:00', 2850000, 'deposit', 'Shanghai Technology Co.', 'June salary', 3650000),
('tx_july_rent', 'acct_zhangming_cny_checking', '2026-06-29T12:16:00+08:00', -520000, 'payment', 'Lujiazui Property Services', 'July apartment rent', 3130000),
('tx_summit_registration', 'acct_zhangming_cny_checking', '2026-06-20T15:22:00+08:00', -120000, 'payment', 'International Marketing Summit', 'Conference registration with company reimbursement evidence retained', 3010000),
('tx_travel_advance', 'acct_zhangming_cny_checking', '2026-06-30T17:08:00+08:00', 275000, 'deposit', 'Shanghai Technology Co.', 'Approved preliminary business travel advance', 3285000),
('tx_mobile_service_june', 'acct_zhangming_cny_checking', '2026-06-27T08:11:00+08:00', -6800, 'payment', 'China Mobile', 'Monthly phone service', 3003200),
('tx_office_lunch_park', 'acct_zhangming_cny_checking', '2026-06-24T12:43:00+08:00', -12600, 'payment', 'Century Avenue Kitchen', 'Team lunch unrelated to Tokyo travel', 3015800),
('tx_client_taxi_pudong', 'acct_zhangming_cny_checking', '2026-06-23T18:27:00+08:00', -9400, 'payment', 'Shanghai Taxi', 'Pudong client visit ground transport', 3028400),
('tx_office_supplies', 'acct_zhangming_cny_checking', '2026-06-18T16:04:00+08:00', -3850, 'payment', 'Office Depot Shanghai', 'Presentation folders and markers', 3037800),
('tx_domestic_rail_hangzhou', 'acct_zhangming_cny_checking', '2026-06-12T07:48:00+08:00', -14600, 'payment', 'China Railway', 'Shanghai–Hangzhou client workshop', 3041650),
('tx_hangzhou_hotel', 'acct_zhangming_cny_checking', '2026-06-12T21:31:00+08:00', -52800, 'payment', 'West Lake Business Hotel', 'One-night domestic client trip', 3056250),
('tx_hangzhou_refund', 'acct_zhangming_cny_checking', '2026-06-16T10:19:00+08:00', 8800, 'transfer_in', 'West Lake Business Hotel', 'Unused breakfast package refund', 3065050),
('tx_card_annual_fee', 'acct_zhangming_cny_checking', '2026-06-08T02:05:00+08:00', -12000, 'fee', 'China Merchants Bank', 'Annual account service fee', 3056250),
('tx_interest_may', 'acct_zhangming_cny_checking', '2026-05-31T23:55:00+08:00', 426, 'interest', 'China Merchants Bank', 'Monthly account interest', 3068250),
('tx_parent_transfer', 'acct_zhangming_cny_checking', '2026-05-23T09:34:00+08:00', -180000, 'transfer_out', 'Zhang Family Account', 'Family support transfer', 3067824),
('tx_medical_reimbursement', 'acct_zhangming_cny_checking', '2026-05-19T14:52:00+08:00', 23600, 'transfer_in', 'Company Benefits', 'Outpatient reimbursement', 3247824),
('tx_jpy_wallet_initial', 'acct_zhangming_jpy_wallet', '2025-11-02T10:06:00+08:00', 150000, 'deposit', 'Currency counter', 'Initial Japan travel-wallet load', 150000),
('tx_osaka_station_meal', 'acct_zhangming_jpy_wallet', '2026-05-16T19:33:00+09:00', -3200, 'payment', 'Shin-Osaka Bento', 'Meal from prior Osaka visit', 146800),
('tx_osaka_subway', 'acct_zhangming_jpy_wallet', '2026-05-17T08:21:00+09:00', -1480, 'payment', 'Osaka Metro', 'Prior trip local transport', 145320),
('tx_osaka_hotel_tax', 'acct_zhangming_jpy_wallet', '2026-05-18T07:42:00+09:00', -300, 'payment', 'Nakanoshima Hotel', 'Accommodation tax from prior trip', 145020),
('tx_jpy_wallet_fx_adjustment', 'acct_zhangming_jpy_wallet', '2026-06-20T11:14:00+08:00', -25020, 'withdrawal', 'Currency desk reconciliation', 'Wallet balance adjustment after cash withdrawal', 120000),
('tx_hkd_wallet_load', 'acct_zhangming_hkd_wallet', '2025-06-18T10:08:00+08:00', 300000, 'deposit', 'Currency counter', 'Transit reserve from prior Hong Kong itinerary', 300000),
('tx_hkd_airport_meal_history', 'acct_zhangming_hkd_wallet', '2025-10-09T17:26:00+08:00', -8600, 'payment', 'Chek Lap Kok Food Hall', 'Historical airport meal', 291400),
('tx_hkd_octopus_topup', 'acct_zhangming_hkd_wallet', '2025-10-09T18:01:00+08:00', -20000, 'payment', 'Octopus Service', 'Historical local transport top-up', 271400),
('tx_hkd_client_refund', 'acct_zhangming_hkd_wallet', '2025-10-14T13:18:00+08:00', 28600, 'transfer_in', 'Regional Sales Office', 'Prior Hong Kong trip expense reimbursement', 300000),
('tx_savings_year_end_bonus', 'acct_zhangming_savings', '2025-12-30T10:40:00+08:00', 4200000, 'deposit', 'Shanghai Technology Co.', '2025 performance bonus', 8120000),
('tx_savings_emergency_topup', 'acct_zhangming_savings', '2026-03-11T09:17:00+08:00', 500000, 'transfer_in', 'Business travel checking', 'Emergency reserve top-up', 8620000),
('tx_savings_insurance_premium', 'acct_zhangming_savings', '2026-04-02T13:09:00+08:00', -120000, 'payment', 'Ping An Life', 'Annual life-insurance premium', 8500000),
('tx_checking_to_savings_march', 'acct_zhangming_cny_checking', '2026-03-11T09:16:00+08:00', -500000, 'transfer_out', 'Emergency savings', 'Scheduled reserve transfer', 3195000);

INSERT INTO payees (payee_id, user_id, name, account_no, account_no_masked, bank_name, added_at) VALUES
('payee_company_finance', 'zhang_ming', 'Shanghai Technology Finance', '6222004100186732', '****6732', 'China Merchants Bank', '2024-02-06T10:20:00+08:00'),
('payee_home_property', 'zhang_ming', 'Lujiazui Property Services', '310066102947', '****2947', 'Bank of Shanghai', '2023-03-16T14:35:00+08:00'),
('payee_family_support', 'zhang_ming', 'Zhang Family Account', '6217003810274659', '****4659', 'China Construction Bank', '2022-08-09T11:12:00+08:00'),
('payee_mobile_carrier', 'zhang_ming', 'China Mobile Shanghai', '1008600216', '****0216', 'Industrial and Commercial Bank of China', '2023-04-01T08:30:00+08:00');

INSERT INTO recurring_payments (schedule_id, user_id, account_id, payee_id, amount_minor, freq, start_date, end_date, next_run_date, status) VALUES
('schedule_apartment_rent', 'zhang_ming', 'acct_zhangming_cny_checking', 'payee_home_property', 520000, 'monthly', '2023-04-01', NULL, '2026-07-29', 'active'),
('schedule_mobile_bill', 'zhang_ming', 'acct_zhangming_cny_checking', 'payee_mobile_carrier', 6800, 'monthly', '2023-04-27', NULL, '2026-07-27', 'active');

INSERT INTO pending_payments (pending_id, account_id, payee_id, amount_minor, memo, scheduled_for, status) VALUES
('pending_family_transfer_august', 'acct_zhangming_cny_checking', 'payee_family_support', 180000, 'August family support', '2026-08-23T09:00:00+08:00', 'pending'),
('pending_rent_july_end', 'acct_zhangming_cny_checking', 'payee_home_property', 520000, 'August apartment rent', '2026-07-29T12:00:00+08:00', 'pending');

INSERT INTO _counters (key, value) VALUES ('tx_seq', 9000), ('payee_seq', 9000), ('schedule_seq', 9000), ('pending_seq', 9000);
COMMIT;
