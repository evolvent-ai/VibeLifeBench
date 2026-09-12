-- Generated credit_card seed for highrise_handover_v5_30d
BEGIN;
INSERT INTO cards (card_id, user_id, issuer, product_name, masked_no, type, credit_limit_minor, available_credit_minor, statement_balance_minor, unbilled_balance_minor, min_payment_due_minor, due_date, cycle_start_day, cycle_end_day, grace_period_days, status, interest_apr_bp) VALUES ('card_hhigh_01', 'usr_chu_nuo', '招商银行', '招行 Young 卡 (Visa)', '**** **** **** 1937', 'Visa', 3000000, 2200000, 5900000, 107600, 50000, '2026-07-08', 6, 5, 25, 'active', 1800);
INSERT INTO statements (statement_id, card_id, period_start, period_end, opening_balance_minor, new_charges_minor, payments_minor, closing_balance_minor, min_payment_due_minor, due_date, status) VALUES ('stmt_hhigh', 'card_hhigh_01', '2026-06-06', '2026-07-05', 0, 5900000, 0, 5900000, 50000, '2026-07-08', 'open');
INSERT INTO statement_lines (line_id, statement_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('line_hhigh_1', 'stmt_hhigh', '2026-06-15T19:20:05+08:00', 5900000, 'TowerCheck 官方旗舰店', '5732', '精装收房', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_hhigh_1', 'card_hhigh_01', '2026-06-15T10:05:08+08:00', 84000, 'TowerCheck 官方店', '5732', '精装收房', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('tx_hhigh_fx', 'card_hhigh_01', '2026-06-15T11:30:00+08:00', 23600, 'PAYPAL US', '4814', '精装收房', 'purchase');
INSERT INTO rewards_balances (card_id, points_balance, ytd_earned, lifetime_earned, updated_at) VALUES ('card_hhigh_01', 18420, 9650, 54200, '2026-06-15T00:00:00Z');
INSERT INTO rewards_ledger (ledger_id, card_id, posted_at, kind, delta, balance_after, note) VALUES ('rl_hhigh_1', 'card_hhigh_01', '2026-06-15T19:20:05+08:00', 'earn', 6899, 18420, '采购积分');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0001', 'card_hhigh_01', '2026-04-08T09:01:00+08:00', 1517, '盒马鲜生', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0002', 'card_hhigh_01', '2026-01-15T10:02:00+08:00', 1834, '星巴克', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0003', 'card_hhigh_01', '2026-04-22T11:03:00+08:00', 2151, '中石化加油站', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0004', 'card_hhigh_01', '2026-01-02T12:04:00+08:00', 2468, '美团外卖', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0005', 'card_hhigh_01', '2026-04-09T13:05:00+08:00', 2785, '京东商城', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0006', 'card_hhigh_01', '2026-01-16T14:06:00+08:00', 3102, '滴滴出行', '4121', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0007', 'card_hhigh_01', '2026-04-23T15:07:00+08:00', 3419, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0008', 'card_hhigh_01', '2026-01-03T16:08:00+08:00', 3736, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0009', 'card_hhigh_01', '2026-04-10T17:09:00+08:00', 4053, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0010', 'card_hhigh_01', '2026-01-17T18:10:00+08:00', 4370, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0011', 'card_hhigh_01', '2026-04-24T19:11:00+08:00', -4687, '永辉超市', '5411', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0012', 'card_hhigh_01', '2026-01-04T08:12:00+08:00', 5004, '肯德基', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0013', 'card_hhigh_01', '2026-04-11T09:13:00+08:00', 5321, '万达影城', '7832', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0014', 'card_hhigh_01', '2026-01-18T10:14:00+08:00', 5638, '携程机票', '4511', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0015', 'card_hhigh_01', '2026-04-25T11:15:00+08:00', 5955, '如家酒店', '7011', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0016', 'card_hhigh_01', '2026-01-05T12:16:00+08:00', 6272, '沃尔玛', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0017', 'card_hhigh_01', '2026-04-12T13:17:00+08:00', 6589, '宜家家居', '5712', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0018', 'card_hhigh_01', '2026-01-19T14:18:00+08:00', 6906, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0019', 'card_hhigh_01', '2026-04-26T15:19:00+08:00', 7223, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0020', 'card_hhigh_01', '2026-01-06T16:20:00+08:00', 7540, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0021', 'card_hhigh_01', '2026-04-13T17:21:00+08:00', 7857, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0022', 'card_hhigh_01', '2026-01-20T18:22:00+08:00', -8174, '瑞幸咖啡', '5814', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0023', 'card_hhigh_01', '2026-04-27T19:23:00+08:00', 8491, '中国石油', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0024', 'card_hhigh_01', '2026-01-07T08:24:00+08:00', 8808, '天猫超市', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0025', 'card_hhigh_01', '2026-04-14T09:25:00+08:00', 9125, '海底捞', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0026', 'card_hhigh_01', '2026-01-21T10:26:00+08:00', 9442, '名创优品', '5331', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0027', 'card_hhigh_01', '2026-04-01T11:27:00+08:00', 9759, '地铁出行', '4111', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0028', 'card_hhigh_01', '2026-01-08T12:28:00+08:00', 10076, '三大运营商', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0029', 'card_hhigh_01', '2026-04-15T13:29:00+08:00', 10393, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0030', 'card_hhigh_01', '2026-01-22T14:30:00+08:00', 10710, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0031', 'card_hhigh_01', '2026-04-02T15:31:00+08:00', 11027, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0032', 'card_hhigh_01', '2026-01-09T16:32:00+08:00', 11344, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0033', 'card_hhigh_01', '2026-04-16T17:33:00+08:00', -11661, '盒马鲜生', '5411', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0034', 'card_hhigh_01', '2026-01-23T18:34:00+08:00', 11978, '星巴克', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0035', 'card_hhigh_01', '2026-04-03T19:35:00+08:00', 12295, '中石化加油站', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0036', 'card_hhigh_01', '2026-01-10T08:36:00+08:00', 12612, '美团外卖', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0037', 'card_hhigh_01', '2026-04-17T09:37:00+08:00', 12929, '京东商城', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0038', 'card_hhigh_01', '2026-01-24T10:38:00+08:00', 13246, '滴滴出行', '4121', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0039', 'card_hhigh_01', '2026-04-04T11:39:00+08:00', 13563, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0040', 'card_hhigh_01', '2026-01-11T12:40:00+08:00', 13880, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0041', 'card_hhigh_01', '2026-04-18T13:41:00+08:00', 14197, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0042', 'card_hhigh_01', '2026-01-25T14:42:00+08:00', 14514, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0043', 'card_hhigh_01', '2026-04-05T15:43:00+08:00', 14831, '永辉超市', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0044', 'card_hhigh_01', '2026-01-12T16:44:00+08:00', -15148, '肯德基', '5814', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0045', 'card_hhigh_01', '2026-04-19T17:45:00+08:00', 15465, '万达影城', '7832', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0046', 'card_hhigh_01', '2026-01-26T18:46:00+08:00', 15782, '携程机票', '4511', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0047', 'card_hhigh_01', '2026-04-06T19:47:00+08:00', 16099, '如家酒店', '7011', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0048', 'card_hhigh_01', '2026-01-13T08:48:00+08:00', 16416, '沃尔玛', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0049', 'card_hhigh_01', '2026-04-20T09:49:00+08:00', 16733, '宜家家居', '5712', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0050', 'card_hhigh_01', '2026-01-27T10:50:00+08:00', 17050, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0051', 'card_hhigh_01', '2026-04-07T11:51:00+08:00', 17367, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0052', 'card_hhigh_01', '2026-01-14T12:52:00+08:00', 17684, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0053', 'card_hhigh_01', '2026-04-21T13:53:00+08:00', 18001, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0054', 'card_hhigh_01', '2026-01-01T14:54:00+08:00', 18318, '瑞幸咖啡', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0055', 'card_hhigh_01', '2026-04-08T15:55:00+08:00', -18635, '中国石油', '5541', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0056', 'card_hhigh_01', '2026-01-15T16:56:00+08:00', 18952, '天猫超市', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0057', 'card_hhigh_01', '2026-04-22T17:57:00+08:00', 19269, '海底捞', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0058', 'card_hhigh_01', '2026-01-02T18:58:00+08:00', 19586, '名创优品', '5331', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0059', 'card_hhigh_01', '2026-04-09T19:59:00+08:00', 19903, '地铁出行', '4111', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0060', 'card_hhigh_01', '2026-01-16T08:00:00+08:00', 20220, '三大运营商', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0061', 'card_hhigh_01', '2026-04-23T09:01:00+08:00', 20537, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0062', 'card_hhigh_01', '2026-01-03T10:02:00+08:00', 20854, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0063', 'card_hhigh_01', '2026-04-10T11:03:00+08:00', 21171, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0064', 'card_hhigh_01', '2026-01-17T12:04:00+08:00', 21488, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0065', 'card_hhigh_01', '2026-04-24T13:05:00+08:00', 21805, '盒马鲜生', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0066', 'card_hhigh_01', '2026-01-04T14:06:00+08:00', -22122, '星巴克', '5814', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0067', 'card_hhigh_01', '2026-04-11T15:07:00+08:00', 22439, '中石化加油站', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0068', 'card_hhigh_01', '2026-01-18T16:08:00+08:00', 22756, '美团外卖', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0069', 'card_hhigh_01', '2026-04-25T17:09:00+08:00', 23073, '京东商城', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0070', 'card_hhigh_01', '2026-01-05T18:10:00+08:00', 23390, '滴滴出行', '4121', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0071', 'card_hhigh_01', '2026-04-12T19:11:00+08:00', 23707, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0072', 'card_hhigh_01', '2026-01-19T08:12:00+08:00', 24024, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0073', 'card_hhigh_01', '2026-04-26T09:13:00+08:00', 24341, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0074', 'card_hhigh_01', '2026-01-06T10:14:00+08:00', 24658, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0075', 'card_hhigh_01', '2026-04-13T11:15:00+08:00', 24975, '永辉超市', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0076', 'card_hhigh_01', '2026-01-20T12:16:00+08:00', 25292, '肯德基', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0077', 'card_hhigh_01', '2026-04-27T13:17:00+08:00', -25609, '万达影城', '7832', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0078', 'card_hhigh_01', '2026-01-07T14:18:00+08:00', 25926, '携程机票', '4511', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0079', 'card_hhigh_01', '2026-04-14T15:19:00+08:00', 26243, '如家酒店', '7011', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0080', 'card_hhigh_01', '2026-01-21T16:20:00+08:00', 26560, '沃尔玛', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0081', 'card_hhigh_01', '2026-04-01T17:21:00+08:00', 26877, '宜家家居', '5712', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0082', 'card_hhigh_01', '2026-01-08T18:22:00+08:00', 27194, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0083', 'card_hhigh_01', '2026-04-15T19:23:00+08:00', 27511, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0084', 'card_hhigh_01', '2026-01-22T08:24:00+08:00', 27828, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0085', 'card_hhigh_01', '2026-04-02T09:25:00+08:00', 28145, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0086', 'card_hhigh_01', '2026-01-09T10:26:00+08:00', 28462, '瑞幸咖啡', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0087', 'card_hhigh_01', '2026-04-16T11:27:00+08:00', 28779, '中国石油', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0088', 'card_hhigh_01', '2026-01-23T12:28:00+08:00', -29096, '天猫超市', '5732', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0089', 'card_hhigh_01', '2026-04-03T13:29:00+08:00', 29413, '海底捞', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0090', 'card_hhigh_01', '2026-01-10T14:30:00+08:00', 29730, '名创优品', '5331', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0091', 'card_hhigh_01', '2026-04-17T15:31:00+08:00', 30047, '地铁出行', '4111', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0092', 'card_hhigh_01', '2026-01-24T16:32:00+08:00', 30364, '三大运营商', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0093', 'card_hhigh_01', '2026-04-04T17:33:00+08:00', 30681, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0094', 'card_hhigh_01', '2026-01-11T18:34:00+08:00', 30998, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0095', 'card_hhigh_01', '2026-04-18T19:35:00+08:00', 31315, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0096', 'card_hhigh_01', '2026-01-25T08:36:00+08:00', 31632, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0097', 'card_hhigh_01', '2026-04-05T09:37:00+08:00', 31949, '盒马鲜生', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0098', 'card_hhigh_01', '2026-01-12T10:38:00+08:00', 32266, '星巴克', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0099', 'card_hhigh_01', '2026-04-19T11:39:00+08:00', -32583, '中石化加油站', '5541', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0100', 'card_hhigh_01', '2026-01-26T12:40:00+08:00', 32900, '美团外卖', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0101', 'card_hhigh_01', '2026-04-06T13:41:00+08:00', 33217, '京东商城', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0102', 'card_hhigh_01', '2026-01-13T14:42:00+08:00', 33534, '滴滴出行', '4121', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0103', 'card_hhigh_01', '2026-04-20T15:43:00+08:00', 33851, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0104', 'card_hhigh_01', '2026-01-27T16:44:00+08:00', 34168, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0105', 'card_hhigh_01', '2026-04-07T17:45:00+08:00', 34485, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0106', 'card_hhigh_01', '2026-01-14T18:46:00+08:00', 34802, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0107', 'card_hhigh_01', '2026-04-21T19:47:00+08:00', 35119, '永辉超市', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0108', 'card_hhigh_01', '2026-01-01T08:48:00+08:00', 35436, '肯德基', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0109', 'card_hhigh_01', '2026-04-08T09:49:00+08:00', 35753, '万达影城', '7832', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0110', 'card_hhigh_01', '2026-01-15T10:50:00+08:00', -36070, '携程机票', '4511', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0111', 'card_hhigh_01', '2026-04-22T11:51:00+08:00', 36387, '如家酒店', '7011', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0112', 'card_hhigh_01', '2026-01-02T12:52:00+08:00', 36704, '沃尔玛', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0113', 'card_hhigh_01', '2026-04-09T13:53:00+08:00', 37021, '宜家家居', '5712', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0114', 'card_hhigh_01', '2026-01-16T14:54:00+08:00', 37338, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0115', 'card_hhigh_01', '2026-04-23T15:55:00+08:00', 37655, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0116', 'card_hhigh_01', '2026-01-03T16:56:00+08:00', 37972, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0117', 'card_hhigh_01', '2026-04-10T17:57:00+08:00', 38289, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0118', 'card_hhigh_01', '2026-01-17T18:58:00+08:00', 38606, '瑞幸咖啡', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0119', 'card_hhigh_01', '2026-04-24T19:59:00+08:00', 38923, '中国石油', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0120', 'card_hhigh_01', '2026-01-04T08:00:00+08:00', 39240, '天猫超市', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0121', 'card_hhigh_01', '2026-04-11T09:01:00+08:00', -39557, '海底捞', '5812', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0122', 'card_hhigh_01', '2026-01-18T10:02:00+08:00', 39874, '名创优品', '5331', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0123', 'card_hhigh_01', '2026-04-25T11:03:00+08:00', 40191, '地铁出行', '4111', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0124', 'card_hhigh_01', '2026-01-05T12:04:00+08:00', 40508, '三大运营商', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0125', 'card_hhigh_01', '2026-04-12T13:05:00+08:00', 40825, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0126', 'card_hhigh_01', '2026-01-19T14:06:00+08:00', 41142, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0127', 'card_hhigh_01', '2026-04-26T15:07:00+08:00', 41459, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0128', 'card_hhigh_01', '2026-01-06T16:08:00+08:00', 41776, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0129', 'card_hhigh_01', '2026-04-13T17:09:00+08:00', 42093, '盒马鲜生', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0130', 'card_hhigh_01', '2026-01-20T18:10:00+08:00', 42410, '星巴克', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0131', 'card_hhigh_01', '2026-04-27T19:11:00+08:00', 42727, '中石化加油站', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0132', 'card_hhigh_01', '2026-01-07T08:12:00+08:00', -43044, '美团外卖', '5812', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0133', 'card_hhigh_01', '2026-04-14T09:13:00+08:00', 43361, '京东商城', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0134', 'card_hhigh_01', '2026-01-21T10:14:00+08:00', 43678, '滴滴出行', '4121', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0135', 'card_hhigh_01', '2026-04-01T11:15:00+08:00', 43995, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0136', 'card_hhigh_01', '2026-01-08T12:16:00+08:00', 44312, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0137', 'card_hhigh_01', '2026-04-15T13:17:00+08:00', 44629, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0138', 'card_hhigh_01', '2026-01-22T14:18:00+08:00', 44946, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0139', 'card_hhigh_01', '2026-04-02T15:19:00+08:00', 45263, '永辉超市', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0140', 'card_hhigh_01', '2026-01-09T16:20:00+08:00', 45580, '肯德基', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0141', 'card_hhigh_01', '2026-04-16T17:21:00+08:00', 45897, '万达影城', '7832', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0142', 'card_hhigh_01', '2026-01-23T18:22:00+08:00', 46214, '携程机票', '4511', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0143', 'card_hhigh_01', '2026-04-03T19:23:00+08:00', -46531, '如家酒店', '7011', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0144', 'card_hhigh_01', '2026-01-10T08:24:00+08:00', 46848, '沃尔玛', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0145', 'card_hhigh_01', '2026-04-17T09:25:00+08:00', 47165, '宜家家居', '5712', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0146', 'card_hhigh_01', '2026-01-24T10:26:00+08:00', 47482, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0147', 'card_hhigh_01', '2026-04-04T11:27:00+08:00', 47799, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0148', 'card_hhigh_01', '2026-01-11T12:28:00+08:00', 48116, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0149', 'card_hhigh_01', '2026-04-18T13:29:00+08:00', 48433, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0150', 'card_hhigh_01', '2026-01-25T14:30:00+08:00', 48750, '瑞幸咖啡', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0151', 'card_hhigh_01', '2026-04-05T15:31:00+08:00', 49067, '中国石油', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0152', 'card_hhigh_01', '2026-01-12T16:32:00+08:00', 49384, '天猫超市', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0153', 'card_hhigh_01', '2026-04-19T17:33:00+08:00', 49701, '海底捞', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0154', 'card_hhigh_01', '2026-01-26T18:34:00+08:00', -50018, '名创优品', '5331', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0155', 'card_hhigh_01', '2026-04-06T19:35:00+08:00', 50335, '地铁出行', '4111', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0156', 'card_hhigh_01', '2026-01-13T08:36:00+08:00', 50652, '三大运营商', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0157', 'card_hhigh_01', '2026-04-20T09:37:00+08:00', 50969, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0158', 'card_hhigh_01', '2026-01-27T10:38:00+08:00', 51286, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0159', 'card_hhigh_01', '2026-04-07T11:39:00+08:00', 51603, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0160', 'card_hhigh_01', '2026-01-14T12:40:00+08:00', 51920, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0161', 'card_hhigh_01', '2026-04-21T13:41:00+08:00', 52237, '盒马鲜生', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0162', 'card_hhigh_01', '2026-01-01T14:42:00+08:00', 52554, '星巴克', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0163', 'card_hhigh_01', '2026-04-08T15:43:00+08:00', 52871, '中石化加油站', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0164', 'card_hhigh_01', '2026-01-15T16:44:00+08:00', 53188, '美团外卖', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0165', 'card_hhigh_01', '2026-04-22T17:45:00+08:00', -53505, '京东商城', '5732', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0166', 'card_hhigh_01', '2026-01-02T18:46:00+08:00', 53822, '滴滴出行', '4121', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0167', 'card_hhigh_01', '2026-04-09T19:47:00+08:00', 54139, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0168', 'card_hhigh_01', '2026-01-16T08:48:00+08:00', 54456, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0169', 'card_hhigh_01', '2026-04-23T09:49:00+08:00', 54773, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0170', 'card_hhigh_01', '2026-01-03T10:50:00+08:00', 55090, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0171', 'card_hhigh_01', '2026-04-10T11:51:00+08:00', 55407, '永辉超市', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0172', 'card_hhigh_01', '2026-01-17T12:52:00+08:00', 55724, '肯德基', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0173', 'card_hhigh_01', '2026-04-24T13:53:00+08:00', 56041, '万达影城', '7832', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0174', 'card_hhigh_01', '2026-01-04T14:54:00+08:00', 56358, '携程机票', '4511', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0175', 'card_hhigh_01', '2026-04-11T15:55:00+08:00', 56675, '如家酒店', '7011', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0176', 'card_hhigh_01', '2026-01-18T16:56:00+08:00', -56992, '沃尔玛', '5411', '日常消费', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0177', 'card_hhigh_01', '2026-04-25T17:57:00+08:00', 57309, '宜家家居', '5712', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0178', 'card_hhigh_01', '2026-01-05T18:58:00+08:00', 57626, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0179', 'card_hhigh_01', '2026-04-12T19:59:00+08:00', 57943, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0180', 'card_hhigh_01', '2026-01-19T08:00:00+08:00', 58260, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0181', 'card_hhigh_01', '2026-04-26T09:01:00+08:00', 58577, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0182', 'card_hhigh_01', '2026-01-06T10:02:00+08:00', 58894, '瑞幸咖啡', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0183', 'card_hhigh_01', '2026-04-13T11:03:00+08:00', 59211, '中国石油', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0184', 'card_hhigh_01', '2026-01-20T12:04:00+08:00', 59528, '天猫超市', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0185', 'card_hhigh_01', '2026-04-27T13:05:00+08:00', 59845, '海底捞', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0186', 'card_hhigh_01', '2026-01-07T14:06:00+08:00', 60162, '名创优品', '5331', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0187', 'card_hhigh_01', '2026-04-14T15:07:00+08:00', -60479, '地铁出行', '4111', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0188', 'card_hhigh_01', '2026-01-21T16:08:00+08:00', 60796, '三大运营商', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0189', 'card_hhigh_01', '2026-04-01T17:09:00+08:00', 61113, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0190', 'card_hhigh_01', '2026-01-08T18:10:00+08:00', 61430, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0191', 'card_hhigh_01', '2026-04-15T19:11:00+08:00', 61747, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0192', 'card_hhigh_01', '2026-01-22T08:12:00+08:00', 62064, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0193', 'card_hhigh_01', '2026-04-02T09:13:00+08:00', 62381, '盒马鲜生', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0194', 'card_hhigh_01', '2026-01-09T10:14:00+08:00', 62698, '星巴克', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0195', 'card_hhigh_01', '2026-04-16T11:15:00+08:00', 63015, '中石化加油站', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0196', 'card_hhigh_01', '2026-01-23T12:16:00+08:00', 63332, '美团外卖', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0197', 'card_hhigh_01', '2026-04-03T13:17:00+08:00', 63649, '京东商城', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0198', 'card_hhigh_01', '2026-01-10T14:18:00+08:00', -63966, '滴滴出行', '4121', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0199', 'card_hhigh_01', '2026-04-17T15:19:00+08:00', 64283, '国家电网', '4900', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0200', 'card_hhigh_01', '2026-01-24T16:20:00+08:00', 64600, '移动通信', '4814', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0201', 'card_hhigh_01', '2026-04-04T17:21:00+08:00', 64917, '屈臣氏', '5912', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0202', 'card_hhigh_01', '2026-01-11T18:22:00+08:00', 65234, '优衣库', '5651', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0203', 'card_hhigh_01', '2026-04-18T19:23:00+08:00', 65551, '永辉超市', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0204', 'card_hhigh_01', '2026-01-25T08:24:00+08:00', 65868, '肯德基', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0205', 'card_hhigh_01', '2026-04-05T09:25:00+08:00', 66185, '万达影城', '7832', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0206', 'card_hhigh_01', '2026-01-12T10:26:00+08:00', 66502, '携程机票', '4511', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0207', 'card_hhigh_01', '2026-04-19T11:27:00+08:00', 66819, '如家酒店', '7011', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0208', 'card_hhigh_01', '2026-01-26T12:28:00+08:00', 67136, '沃尔玛', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0209', 'card_hhigh_01', '2026-04-06T13:29:00+08:00', -67453, '宜家家居', '5712', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0210', 'card_hhigh_01', '2026-01-13T14:30:00+08:00', 67770, '苏宁易购', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0211', 'card_hhigh_01', '2026-04-20T15:31:00+08:00', 68087, '顺丰速运', '4215', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0212', 'card_hhigh_01', '2026-01-27T16:32:00+08:00', 68404, '饿了么', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0213', 'card_hhigh_01', '2026-04-07T17:33:00+08:00', 68721, '华润万家', '5411', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0214', 'card_hhigh_01', '2026-01-14T18:34:00+08:00', 69038, '瑞幸咖啡', '5814', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0215', 'card_hhigh_01', '2026-04-21T19:35:00+08:00', 69355, '中国石油', '5541', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0216', 'card_hhigh_01', '2026-01-01T08:36:00+08:00', 69672, '天猫超市', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0217', 'card_hhigh_01', '2026-04-08T09:37:00+08:00', 69989, '海底捞', '5812', '日常消费', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0218', 'card_hhigh_01', '2026-01-15T10:38:00+08:00', 70306, '名创优品', '5331', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0219', 'card_hhigh_01', '2026-04-22T11:39:00+08:00', 70623, '地铁出行', '4111', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0220', 'card_hhigh_01', '2026-01-02T12:40:00+08:00', -70940, '三大运营商', '4814', '其他', 'refund');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0221', 'card_hhigh_01', '2026-04-09T13:41:00+08:00', 71257, '阿迪达斯', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0222', 'card_hhigh_01', '2026-01-16T14:42:00+08:00', 71574, '耐克', '5661', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0223', 'card_hhigh_01', '2026-04-23T15:43:00+08:00', 71891, '小米之家', '5732', '其他', 'purchase');
INSERT INTO unbilled_transactions (tx_id, card_id, posted_at, amount_minor, merchant_name, mcc, category, kind) VALUES ('dtx_hhigh_0224', 'card_hhigh_01', '2026-01-03T16:44:00+08:00', 72208, '华为体验店', '5732', '其他', 'purchase');
INSERT INTO _counters (key,value) VALUES ('payment_seq',0),('line_seq',1),('dispute_seq',0),('ledger_seq',1);
COMMIT;

-- 手工复核整改：32 个真实消费关系各自使用七笔非等差金额与自然复购日期，清除连续数列填充。
BEGIN;
WITH profiles(n, amounts, schedule_key) AS (VALUES
(1,'[12840,23560,8420,31980,17640,45210,9800]','A'),
(2,'[3600,4200,3900,5100,4700,4300,5600]','B'),
(3,'[32000,28000,35000,30000,42000,26000,38000]','C'),
(4,'[4280,7650,3190,11240,5860,9340,6720]','D'),
(5,'[18900,45800,129900,27600,68800,34500,219000]','E'),
(6,'[2360,5840,1290,7680,3420,9150,4770]','F'),
(7,'[18600,24300,39800,27500,51200,22400,46700]','G'),
(8,'[9900,12900,15900,11900,18900,13900,16900]','H'),
(9,'[2680,15400,5960,3290,21800,7420,4680]','A'),
(10,'[23900,46800,15900,79900,32800,118000,52600]','B'),
(11,'[13860,26740,9460,35120,18290,47980,11240]','C'),
(12,'[2580,4860,3290,7120,5480,3960,8240]','D'),
(13,'[7600,9800,14200,6800,11600,15800,8400]','E'),
(14,'[126800,238500,89500,176400,312600,148900,204700]','F'),
(15,'[35800,52600,28900,68400,43700,91200,47600]','G'),
(16,'[9630,18420,25760,11890,32650,14280,28970]','H'),
(17,'[46900,128000,75900,218000,35600,98600,164000]','A'),
(18,'[89900,238000,45900,176000,329000,118000,267000]','B'),
(19,'[1800,2600,4200,1500,6800,3300,2400]','C'),
(20,'[3260,5740,2890,8460,4520,7180,3980]','D'),
(21,'[11640,22850,7340,30260,16890,41700,10580]','E'),
(22,'[3200,4500,3800,4900,4100,5300,3700]','F'),
(23,'[30000,36000,27500,41500,33000,29000,44500]','G'),
(24,'[15900,36800,8900,72900,24800,116000,45900]','H'),
(25,'[12600,23800,9800,34200,17600,28900,15400]','A'),
(26,'[4900,7600,3200,11800,6800,9400,5600]','B'),
(27,'[600,800,500,1200,700,1000,900]','C'),
(28,'[8800,12800,15800,9800,18800,13800,16800]','D'),
(29,'[45900,79800,32900,126000,57600,94800,68400]','E'),
(30,'[52900,88900,39900,138000,64600,109000,75900]','F'),
(31,'[69900,159900,42900,118900,249900,86900,189900]','G'),
(32,'[79900,179900,49900,139900,269900,95900,209900]','H')
), schedules(schedule_key, dates) AS (VALUES
('A','["2026-01-06T09:20:00+08:00","2026-01-22T18:35:00+08:00","2026-02-08T11:10:00+08:00","2026-02-24T19:05:00+08:00","2026-03-12T08:45:00+08:00","2026-04-03T17:25:00+08:00","2026-04-21T12:40:00+08:00"]'),
('B','["2026-01-08T10:15:00+08:00","2026-01-27T15:50:00+08:00","2026-02-14T09:30:00+08:00","2026-03-02T20:10:00+08:00","2026-03-19T13:05:00+08:00","2026-04-07T18:20:00+08:00","2026-04-25T11:55:00+08:00"]'),
('C','["2026-01-11T08:40:00+08:00","2026-01-30T17:15:00+08:00","2026-02-18T12:25:00+08:00","2026-03-07T19:35:00+08:00","2026-03-23T09:05:00+08:00","2026-04-10T16:50:00+08:00","2026-04-28T14:20:00+08:00"]'),
('D','["2026-01-04T12:10:00+08:00","2026-01-19T18:45:00+08:00","2026-02-05T08:55:00+08:00","2026-02-22T15:30:00+08:00","2026-03-10T20:05:00+08:00","2026-03-29T11:40:00+08:00","2026-04-16T17:10:00+08:00"]'),
('E','["2026-01-13T09:35:00+08:00","2026-02-01T14:25:00+08:00","2026-02-17T19:10:00+08:00","2026-03-05T10:50:00+08:00","2026-03-21T16:15:00+08:00","2026-04-09T08:30:00+08:00","2026-04-27T18:05:00+08:00"]'),
('F','["2026-01-16T11:05:00+08:00","2026-02-03T17:40:00+08:00","2026-02-20T09:20:00+08:00","2026-03-09T13:55:00+08:00","2026-03-26T19:25:00+08:00","2026-04-13T10:35:00+08:00","2026-04-30T15:45:00+08:00"]'),
('G','["2026-01-07T08:25:00+08:00","2026-01-25T16:55:00+08:00","2026-02-12T12:05:00+08:00","2026-03-01T18:30:00+08:00","2026-03-18T09:40:00+08:00","2026-04-05T14:15:00+08:00","2026-04-23T20:00:00+08:00"]'),
('H','["2026-01-10T13:15:00+08:00","2026-01-28T09:45:00+08:00","2026-02-15T17:20:00+08:00","2026-03-04T11:35:00+08:00","2026-03-22T19:50:00+08:00","2026-04-11T08:15:00+08:00","2026-04-29T16:40:00+08:00"]')
)
UPDATE unbilled_transactions
SET amount_minor = CASE WHEN kind='refund' THEN -abs(CAST((SELECT json_extract(profiles.amounts,'$[' || CAST((CAST(substr(unbilled_transactions.tx_id,-4) AS INTEGER)-1)/32 AS INTEGER) || ']') FROM profiles WHERE profiles.n=((CAST(substr(unbilled_transactions.tx_id,-4) AS INTEGER)-1)%32)+1) AS INTEGER)) ELSE CAST((SELECT json_extract(profiles.amounts,'$[' || CAST((CAST(substr(unbilled_transactions.tx_id,-4) AS INTEGER)-1)/32 AS INTEGER) || ']') FROM profiles WHERE profiles.n=((CAST(substr(unbilled_transactions.tx_id,-4) AS INTEGER)-1)%32)+1) AS INTEGER) END,
    posted_at = (SELECT json_extract(schedules.dates,'$[' || CAST((CAST(substr(unbilled_transactions.tx_id,-4) AS INTEGER)-1)/32 AS INTEGER) || ']') FROM profiles JOIN schedules USING(schedule_key) WHERE profiles.n=((CAST(substr(unbilled_transactions.tx_id,-4) AS INTEGER)-1)%32)+1)
WHERE tx_id GLOB 'dtx_hhigh_[0-9][0-9][0-9][0-9]';
COMMIT;
