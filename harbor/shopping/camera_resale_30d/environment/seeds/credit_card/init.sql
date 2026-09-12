-- Generated credit_card seed for camera_resale_30d
BEGIN;
INSERT INTO cards (card_id, user_id, issuer, product_name, masked_no, type, credit_limit_minor, available_credit_minor, statement_balance_minor, unbilled_balance_minor, min_payment_due_minor, due_date, cycle_start_day, cycle_end_day, grace_period_days, status, interest_apr_bp) VALUES ('card_rscam_01', 'usr_zhan_peng', 'China Merchants Bank', 'CMB Young Card (Visa)', '**** **** **** 3521', 'Visa', 3000000, 2200000, 780000, 99600, 50000, '2026-07-10', 6, 5, 25, 'active', 1800);
INSERT INTO statements (statement_id, card_id, period_start, period_end, opening_balance_minor, new_charges_minor, payments_minor, closing_balance_minor, min_payment_due_minor, due_date, status) VALUES ('stmt_rscam', 'card_rscam_01', '2026-06-06', '2026-07-05', 0, 780000, 0, 780000, 50000, '2026-07-10', 'open');
INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('line_rscam_1', 'stmt_rscam', '2026-06-15T19:20:05+08:00', 780000, 'Sonar Official Flagship Store', '5732', 'Digital Imaging', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_rscam_1', 'card_rscam_01', '2026-06-15T10:05:08+08:00', 84000, 'Sonar Official Store', '5732', 'Digital Imaging', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_rscam_fx', 'card_rscam_01', '2026-06-15T11:30:00+08:00', 15600, 'PAYPAL US', '4814', 'Digital Imaging', 'purchase');
INSERT INTO rewards_balances (card_id, points_balance, ytd_earned, lifetime_earned, updated_at) VALUES ('card_rscam_01', 18420, 9650, 54200, '2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta, balance_after, note) VALUES ('rl_rscam_1', 'card_rscam_01', '2026-06-15T19:20:05+08:00', 'earn', 6899, 18420, 'Procurement points');
INSERT INTO _counters (key,value) VALUES ('payment_seq',0),('line_seq',1),('dispute_seq',0),('ledger_seq',1);
COMMIT;

-- Curated paid statements for ordinary studio and household spending, separate from the active camera-sale and PayPal lines.
BEGIN;
INSERT INTO statements (statement_id,card_id,period_start,period_end,opening_balance_minor,new_charges_minor,payments_minor,closing_balance_minor,min_payment_due_minor,due_date,status) VALUES
('stmt_camera_january_slate','card_rscam_01','2026-01-06','2026-02-05',0,31590,31590,0,0,'2026-02-08','paid'),
('stmt_camera_february_amber','card_rscam_01','2026-02-06','2026-03-05',0,29960,29960,0,0,'2026-03-08','paid'),
('stmt_camera_march_cobalt','card_rscam_01','2026-03-06','2026-04-05',0,31132,31132,0,0,'2026-04-08','paid'),
('stmt_camera_april_olive','card_rscam_01','2026-04-06','2026-05-05',0,29480,29480,0,0,'2026-05-08','paid'),
('stmt_camera_may_coral','card_rscam_01','2026-05-06','2026-06-05',0,122742,122742,0,0,'2026-06-08','paid');
INSERT INTO statement_lines (line_id,statement_id,posted_at,amount_minor,merchant_name,mcc,category,kind) VALUES
('line_camera_slate_metro','stmt_camera_january_slate','2026-01-09T08:12:00+08:00',2450,'Guangzhou Metro QR Ride Code','4111','Public Transit','purchase'),
('line_camera_slate_cowork','stmt_camera_january_slate','2026-01-13T09:30:00+08:00',7800,'Pearl River Creative Space','6513','Coworking','purchase'),
('line_camera_slate_lunch','stmt_camera_january_slate','2026-01-17T12:18:00+08:00',1260,'Yinji Rice Noodle Roll, Haizhu Branch','5812','Dining','purchase'),
('line_camera_slate_print','stmt_camera_january_slate','2026-01-21T15:44:00+08:00',3200,'Light Domain Output Lab','7338','Photography Printing','purchase'),
('line_camera_slate_bike','stmt_camera_january_slate','2026-01-25T18:06:00+08:00',680,'Qingju Bike','4121','Shared Mobility','purchase'),
('line_camera_slate_cloud','stmt_camera_january_slate','2026-01-29T10:22:00+08:00',4500,'CloudFrame Storage','7372','Digital Services','purchase'),
('line_camera_slate_insurance','stmt_camera_january_slate','2026-02-02T09:16:00+08:00',12900,'Anlan Equipment Insurance','6300','Insurance Coverage','purchase'),
('line_camera_slate_refund','stmt_camera_january_slate','2026-02-04T13:31:00+08:00',-1200,'Sample Print Refund','7338','Photography Printing','refund'),
('line_camera_amber_breakfast','stmt_camera_february_amber','2026-02-08T08:20:00+08:00',980,'Tao Tao Ju Breakfast','5812','Dining','purchase'),
('line_camera_amber_rail','stmt_camera_february_amber','2026-02-12T07:35:00+08:00',5600,'Rail Travel','4112','Intercity Transit','purchase'),
('line_camera_amber_stationery','stmt_camera_february_amber','2026-02-16T16:10:00+08:00',1880,'Fang Stationery','5943','Office Supplies','purchase'),
('line_camera_amber_rental','stmt_camera_february_amber','2026-02-20T11:42:00+08:00',7400,'Spectrum Equipment Rental','7394','Equipment Rental','purchase'),
('line_camera_amber_power','stmt_camera_february_amber','2026-02-24T07:58:00+08:00',3600,'China Southern Power Grid','4900','Utilities','purchase'),
('line_camera_amber_grocery','stmt_camera_february_amber','2026-02-27T19:25:00+08:00',2250,'Fresh Select Delivery','5411','Fresh Food','purchase'),
('line_camera_amber_workshop','stmt_camera_february_amber','2026-03-02T14:05:00+08:00',8900,'Southern Imaging Society','8299','Professional Training','purchase'),
('line_camera_amber_adjust','stmt_camera_february_amber','2026-03-04T10:48:00+08:00',-650,'Shared Bike Error Adjustment','4121','Shared Mobility','adjustment'),
('line_camera_cobalt_electric','stmt_camera_march_cobalt','2026-03-08T07:42:00+08:00',11742,'China Southern Power Grid','4900','Utilities','purchase'),
('line_camera_cobalt_coffee','stmt_camera_march_cobalt','2026-03-12T10:26:00+08:00',1460,'Yongpu Coffee, Haizhu Branch','5814','Dining','purchase'),
('line_camera_cobalt_drive','stmt_camera_march_cobalt','2026-03-16T09:50:00+08:00',5200,'China Auto Rental, Guangzhou South Station','7512','Short-Term Transport','purchase'),
('line_camera_cobalt_parking','stmt_camera_march_cobalt','2026-03-20T18:34:00+08:00',780,'Haizhu Parking Management','7523','Parking Services','purchase'),
('line_camera_cobalt_calibration','stmt_camera_march_cobalt','2026-03-24T13:12:00+08:00',9600,'Spectrum Color Calibration','7399','Professional Services','purchase'),
('line_camera_cobalt_books','stmt_camera_march_cobalt','2026-03-28T16:47:00+08:00',3100,'Guangzhou Books & Culture','5942','Books & Culture','purchase'),
('line_camera_cobalt_mobile','stmt_camera_march_cobalt','2026-04-01T08:55:00+08:00',2450,'China Unicom Guangdong','4814','Telecommunications','purchase'),
('line_camera_cobalt_refund','stmt_camera_march_cobalt','2026-04-04T12:29:00+08:00',-3200,'Car Rental Deposit Refund','7512','Short-Term Transport','refund'),
('line_camera_olive_repair','stmt_camera_april_olive','2026-04-08T11:25:00+08:00',6800,'Suicheng Imaging Repair','7622','Equipment Repair','purchase'),
('line_camera_olive_noodle','stmt_camera_april_olive','2026-04-12T12:06:00+08:00',1240,'Zhusheng Noodle House','5812','Dining','purchase'),
('line_camera_olive_storage','stmt_camera_april_olive','2026-04-16T09:38:00+08:00',4500,'CloudFrame Storage','7372','Digital Services','purchase'),
('line_camera_olive_courier','stmt_camera_april_olive','2026-04-20T15:24:00+08:00',2650,'SF Express','4215','Courier & Logistics','purchase'),
('line_camera_olive_bus','stmt_camera_april_olive','2026-04-24T08:14:00+08:00',790,'Yang Cheng Tong','4111','Public Transit','purchase'),
('line_camera_olive_course','stmt_camera_april_olive','2026-04-28T19:42:00+08:00',11800,'Commercial Photo Retouching Course','8299','Professional Training','purchase'),
('line_camera_olive_supplies','stmt_camera_april_olive','2026-05-02T17:08:00+08:00',3300,'Photography Supplies Store','5946','Photography Supplies','purchase'),
('line_camera_olive_credit','stmt_camera_april_olive','2026-05-04T11:16:00+08:00',-1600,'Out-of-Stock Supplies Refund','5946','Photography Supplies','refund'),
('line_camera_coral_cowork','stmt_camera_may_coral','2026-05-08T09:05:00+08:00',98000,'Pearl River Creative Space','6513','Coworking','purchase'),
('line_camera_coral_breakfast','stmt_camera_may_coral','2026-05-12T08:18:00+08:00',1680,'Dian Dou De, Haizhu Branch','5812','Dining','purchase'),
('line_camera_coral_lab','stmt_camera_may_coral','2026-05-16T14:32:00+08:00',4200,'Light Domain Output Lab','7338','Photography Printing','purchase'),
('line_camera_coral_metro','stmt_camera_may_coral','2026-05-20T18:02:00+08:00',1320,'Guangzhou Metro QR Ride Code','4111','Public Transit','purchase'),
('line_camera_coral_service','stmt_camera_may_coral','2026-05-24T10:46:00+08:00',7600,'Jiangnan Bike Shop','7699','Vehicle Maintenance','purchase'),
('line_camera_coral_cloud','stmt_camera_may_coral','2026-05-28T09:27:00+08:00',2850,'Online Stock Photo Subscription','7372','Digital Services','purchase'),
('line_camera_coral_power','stmt_camera_may_coral','2026-06-02T07:52:00+08:00',11742,'China Southern Power Grid','4900','Utilities','purchase'),
('line_camera_coral_refund','stmt_camera_may_coral','2026-06-04T16:05:00+08:00',-4650,'Fresh Select Out-of-Stock Refund','5411','Fresh Food','refund');
INSERT INTO payments (payment_id,card_id,posted_at,amount_minor,source_hint,applied_to_statement_minor,applied_to_unbilled_minor) VALUES
('pay_camera_slate_first','card_rscam_01','2026-02-06T08:30:00+08:00',15000,'Nanyue Bank Debit Card',15000,0),('pay_camera_slate_close','card_rscam_01','2026-02-07T19:12:00+08:00',16590,'Project Payment Balance',16590,0),
('pay_camera_amber_first','card_rscam_01','2026-03-06T09:14:00+08:00',14000,'Nanyue Bank Debit Card',14000,0),('pay_camera_amber_close','card_rscam_01','2026-03-07T20:06:00+08:00',15960,'Automatic Salary Account Repayment',15960,0),
('pay_camera_cobalt_first','card_rscam_01','2026-04-06T07:48:00+08:00',16000,'Project Payment Balance',16000,0),('pay_camera_cobalt_close','card_rscam_01','2026-04-07T21:15:00+08:00',15132,'Nanyue Bank Debit Card',15132,0),
('pay_camera_olive_first','card_rscam_01','2026-05-06T08:44:00+08:00',12000,'Automatic Salary Account Repayment',12000,0),('pay_camera_olive_close','card_rscam_01','2026-05-07T17:32:00+08:00',17480,'Project Payment Balance',17480,0),
('pay_camera_coral_first','card_rscam_01','2026-06-06T09:25:00+08:00',70000,'Nanyue Bank Debit Card',70000,0),('pay_camera_coral_close','card_rscam_01','2026-06-07T20:48:00+08:00',52742,'Final Project Payment Transfer',52742,0);
INSERT INTO rewards_ledger (ledger_id,card_id,posted_at,kind,delta,balance_after,note) VALUES
('reward_camera_metro','card_rscam_01','2026-01-09T08:13:00+08:00','earn',25,13210,'Metro Transit Points'),('reward_camera_cowork','card_rscam_01','2026-01-13T09:31:00+08:00','earn',78,13288,'Coworking Points'),
('reward_camera_print','card_rscam_01','2026-01-21T15:45:00+08:00','earn',32,13320,'Printing Service Points'),('reward_camera_cloud','card_rscam_01','2026-01-29T10:23:00+08:00','earn',45,13365,'Cloud Storage Points'),
('reward_camera_insurance','card_rscam_01','2026-02-02T09:17:00+08:00','earn',129,13494,'Equipment Insurance Points'),('reward_camera_rail','card_rscam_01','2026-02-12T07:36:00+08:00','earn',56,13550,'Rail Travel Points'),
('reward_camera_rental','card_rscam_01','2026-02-20T11:43:00+08:00','earn',74,13624,'Equipment Rental Points'),('reward_camera_workshop','card_rscam_01','2026-03-02T14:06:00+08:00','earn',89,13713,'Imaging Course Points'),
('reward_camera_electric','card_rscam_01','2026-03-08T07:43:00+08:00','earn',117,13830,'Electricity Points'),('reward_camera_drive','card_rscam_01','2026-03-16T09:51:00+08:00','earn',52,13882,'Car Rental Points'),
('reward_camera_calibration','card_rscam_01','2026-03-24T13:13:00+08:00','earn',96,13978,'Color Calibration Points'),('reward_camera_books','card_rscam_01','2026-03-28T16:48:00+08:00','earn',31,14009,'Books & Culture Points'),
('reward_camera_repair','card_rscam_01','2026-04-08T11:26:00+08:00','earn',68,14077,'Equipment Repair Points'),('reward_camera_courier','card_rscam_01','2026-04-20T15:25:00+08:00','earn',27,14104,'Logistics Service Points'),
('reward_camera_course','card_rscam_01','2026-04-28T19:43:00+08:00','earn',118,14222,'Photo Retouching Course Points'),('reward_camera_supplies','card_rscam_01','2026-05-02T17:09:00+08:00','earn',33,14255,'Photography Supplies Points'),
('reward_camera_coral_cowork','card_rscam_01','2026-05-08T09:06:00+08:00','earn',980,15235,'Quarterly Workspace Points'),('reward_camera_lab','card_rscam_01','2026-05-16T14:33:00+08:00','earn',42,15277,'Lab Printing Points'),
('reward_camera_bike','card_rscam_01','2026-05-24T10:47:00+08:00','earn',76,15353,'Bike Maintenance Points'),('reward_camera_gallery','card_rscam_01','2026-05-28T09:28:00+08:00','earn',29,15382,'Stock Photo Subscription Points'),
('reward_camera_power','card_rscam_01','2026-06-02T07:53:00+08:00','earn',117,15499,'Utilities Points'),('reward_camera_print_reverse','card_rscam_01','2026-02-04T13:32:00+08:00','adjust',-12,15487,'Sample Print Refund Points Reversal'),
('reward_camera_drive_reverse','card_rscam_01','2026-04-04T12:30:00+08:00','adjust',-32,15455,'Car Rental Deposit Refund Adjustment'),('reward_camera_supply_reverse','card_rscam_01','2026-05-04T11:17:00+08:00','adjust',-16,15439,'Supplies Refund Points Reversal'),
('reward_camera_green_bonus','card_rscam_01','2026-06-05T12:10:00+08:00','adjust',90,15529,'Monthly Green Transit Reward');
UPDATE _counters SET value=50 WHERE key='line_seq'; UPDATE _counters SET value=10 WHERE key='payment_seq'; UPDATE _counters SET value=26 WHERE key='ledger_seq';
COMMIT;
