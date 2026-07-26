-- Stage 15 (2026-07-16): 供应商来信要求把押金改汇到一个临时个人账户。
-- 该收款方在此之前不存在于通讯录中；本 mutation 只落地“待核验收款方”这一风险事实。
-- 不创建 pending payment、不创建 recurring schedule，也不产生任何 debit/deposit/refund transaction。
INSERT OR IGNORE INTO payees(payee_id,user_id,name,bank_name,account_no,account_no_masked,added_at) VALUES ('pay_factory_temp','user_seed_tb_013','嘉兴智造临时账户','个人账户','6222000130139999','************9999','2026-07-16T00:15:00Z');
