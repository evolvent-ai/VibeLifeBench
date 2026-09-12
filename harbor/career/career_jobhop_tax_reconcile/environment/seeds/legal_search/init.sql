-- record；record，record。
BEGIN;
INSERT INTO courts (court_id,name,level,region) VALUES
('court_kq_tax_service','record','record','record'),
('court_kq_pudong','record','record','record'),
('court_kq_first','record','record','record');
INSERT INTO statutes (statute_id,name,short_name,issuer,effective_date,status,summary) VALUES
('stat_kq_iit_2025','record2025record','2025record','record','2026-02-03','record','record2026record1record，record2025record2026record3record1record6record30record，record。'),
('stat_kq_iit_settlement_admin','Administrative Measures for Annual Individual Income Tax Settlement','Annual Settlement Measures','State Tax Administration','2025-02-26','effective','Order No. 57, effective February 26, 2025; covers annual settlement, corrections, deadlines, authorization boundaries, refunds, and record retention.'),
('stat_kq_iit_law','record','record','record','2019-01-01','record','record。'),
('stat_kq_withholding','record（record）','record','record','2019-01-01','record','record。'),
('stat_kq_admin','record','record','record','2001-05-01','record','record、record。');
INSERT INTO statute_articles (article_id,statute_id,article_no,seq,heading,text) VALUES
('art_kq_2025_booking','stat_kq_iit_2025','record',1,'2025record','2025record2026record3record1record6record30record；record。'),
('art_kq_annual','stat_kq_iit_settlement_admin','Article 3',3,'Annual settlement scope','Taxpayers must reconcile annual comprehensive income and withholding using verifiable source records.'),
('art_kq_period','stat_kq_iit_settlement_admin','Article 5',5,'Filing period','The statutory annual settlement filing period runs from March 1 through June 30.'),
('art_kq_prepare','stat_kq_iit_settlement_admin','Article 8',8,'Supporting materials','Taxpayers should prepare income, deduction, withholding, and correction records before filing.'),
('art_kq_appeal','stat_kq_iit_settlement_admin','Article 13',13,'Corrections and objections','A taxpayer may request correction and preserve unresolved objections until verified.'),
('art_kq_authorization','stat_kq_iit_settlement_admin','Article 14',14,'Authorization','Submission and final confirmation require the taxpayer or explicit authorization.'),
('art_kq_admin_retention','stat_kq_iit_settlement_admin','Article 16',16,'Record retention','Income, withholding, correction, and refund evidence must be retained; supporting materials are retained for five years.'),
('art_kq_refund_account','stat_kq_iit_settlement_admin','Article 26',26,'Refund account','A tax refund must be paid to the taxpayer''s verified account.'),
('art_kq_iit_comprehensive','stat_kq_iit_law','record',11,'record','record，record；record，record，record。'),
('art_kq_withhold_info','stat_kq_withholding','record',3,'record','record，record。'),
('art_kq_truth','stat_kq_admin','record',25,'record','record，record。');
INSERT INTO cases (case_id,case_number,title,court_id,case_type,cause,judgment_date,parties,summary,facts,reasoning,holding,ruling,outcome,keywords) VALUES
('case_kq_missing_month','(2025)record011record','record','court_kq_tax_service','record','record','2025-08-12','record：record；record：record','record，record。','record；record，record。','record、record；record，record。','record，record。','record。','record','record,record,record,record'),
('case_kq_false_delete','(2025)record0115record088record','record','court_kq_pudong','record','record','2025-10-20','record：record；record：record','record，record，record。','record，record。','record；record。','record。','record。','record','record,record,record'),
('case_kq_net_gross','(2024)record01record14320record','record','court_kq_first','record','record','2024-11-15','record：record；record：record','record。','record。','record，record、record。','record。','record。','record','record,record,record,record');
INSERT INTO citations (citation_id,case_id,target_type,target_id,label) VALUES
('cit_kq_1','case_kq_missing_month','article','art_kq_appeal','record'),
('cit_kq_2','case_kq_false_delete','article','art_kq_truth','record'),
('cit_kq_3','case_kq_net_gross','article','art_kq_withhold_info','record');
INSERT INTO _counters (key,value) VALUES ('saved_seq',0);
COMMIT;
