-- Reviewed offline legal corpus: 60 distinct court/statute/article records.
INSERT INTO courts(court_id,name,level,region) VALUES ('court_shanghai_rules','上海公共法律资料索引','中级法院','上海');

INSERT INTO statutes(statute_id,name,short_name,issuer,effective_date,status,summary) VALUES
 ('legal_rule_temp_id_rail','铁路旅客临时乘车身份证明办理规则摘编','临时乘车证明','中国国家铁路集团旅客服务规则摘录','2026-01-01','现行有效','身份证遗失旅客应通过车站公安制证窗口或铁路官方渠道完成本人核验。'),
 ('legal_rule_reissue_remote','居民身份证异地受理与材料核验规则摘编','异地补办','上海市公安政务办事指南摘录','2026-01-01','现行有效','异地补办需要本人到场，材料清单以受理窗口和官方系统的实时要求为准。'),
 ('legal_rule_email_invalid','政务材料普通邮件提交风险提示','普通邮件无效','上海市政务数据安全指引摘录','2026-01-01','现行有效','证件、户籍和死亡证明等敏感材料不得通过普通邮件提交或进行非官方预审。');

INSERT INTO statute_articles(article_id,statute_id,article_no,seq,heading,text) VALUES
 ('art_temp_id_001','legal_rule_temp_id_rail','第一条',1,'本人办理','旅客身份证遗失时，应由本人持可核验信息到车站公安制证窗口或铁路官方渠道办理临时乘车身份证明。'),
 ('art_temp_id_002','legal_rule_temp_id_rail','第二条',2,'到站缓冲','临时乘车身份证明办理需要人工核验，应在乘车前预留充足的到站时间。'),
 ('art_reissue_001','legal_rule_reissue_remote','第一条',1,'本人到场','居民身份证异地受理需要本人到场采集或核验身份信息，不得由他人代替办理。'),
 ('art_reissue_002','legal_rule_reissue_remote','第二条',2,'材料核验','户籍页、死亡证明和关系说明以现场窗口或官方系统要求为准，摘要不构成结果承诺。'),
 ('art_email_001','legal_rule_email_invalid','第一条',1,'普通邮件风险','普通邮件不属于证件照片、户籍页、死亡证明或银行卡流水的安全提交渠道。');

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<17)
INSERT INTO statutes(statute_id,name,short_name,issuer,effective_date,status,summary)
SELECT printf('legal_reference_%02d',n),
       CASE n WHEN 1 THEN '铁路旅客退票与改签规则摘要' WHEN 2 THEN '老年旅客电子客票服务指引' WHEN 3 THEN '航空客票非自愿变更处理摘要' WHEN 4 THEN '旅馆住宿实名登记说明' WHEN 5 THEN '个人信息最小必要处理指引' WHEN 6 THEN '政务服务预约变更规则' WHEN 7 THEN '银行转账授权核验提示' WHEN 8 THEN '殡葬服务收费公示要求' WHEN 9 THEN '道路施工信息发布规范' WHEN 10 THEN '公共交通无障碍服务说明' WHEN 11 THEN '铁路候补订单处理规则' WHEN 12 THEN '消费者预付款风险提示' WHEN 13 THEN '电子邮件反钓鱼操作指南' WHEN 14 THEN '异地就医材料核验摘要' WHEN 15 THEN '住宿取消条款展示要求' WHEN 16 THEN '紧急联系人信息保护规则' ELSE '公共服务投诉受理流程' END,
       CASE n WHEN 1 THEN '铁路退改' WHEN 2 THEN '老人票务' WHEN 3 THEN '航班变更' WHEN 4 THEN '住宿实名' WHEN 5 THEN '最小必要' WHEN 6 THEN '预约变更' WHEN 7 THEN '支付授权' WHEN 8 THEN '殡葬收费' WHEN 9 THEN '道路施工' WHEN 10 THEN '无障碍' WHEN 11 THEN '候补处理' WHEN 12 THEN '预付款' WHEN 13 THEN '反钓鱼' WHEN 14 THEN '就医材料' WHEN 15 THEN '取消条款' WHEN 16 THEN '联系人保护' ELSE '投诉流程' END,
       CASE n%4 WHEN 0 THEN '交通运输公共信息摘录' WHEN 1 THEN '上海政务服务资料摘录' WHEN 2 THEN '消费者权益保护资料摘录' ELSE '公共安全服务资料摘录' END,
       '2025-01-01','现行有效',
       CASE n WHEN 1 THEN '退票与改签费用取决于票种、办理时间和承运方公布条件。' WHEN 2 THEN '车站可提供人工引导，但旅客仍需携带可核验的身份信息。' WHEN 3 THEN '延误导致的非自愿变更应保留原订单与承运方通知作为依据。' WHEN 4 THEN '住宿登记需核验入住人信息，平台订单不能替代现场登记。' WHEN 5 THEN '处理个人资料应限定目的、字段和保存期限，避免无关扩散。' WHEN 6 THEN '预约时间被系统调整后，应以最新确认记录为准并重新核对地点。' WHEN 7 THEN '大额转账应核对收款人、金额、用途和用户的明确授权。' WHEN 8 THEN '殡葬服务项目、金额和收款主体应当清晰展示并留存票据。' WHEN 9 THEN '施工信息应标明生效时段、影响范围和可行绕行建议。' WHEN 10 THEN '面向老年旅客的服务应提供清晰指引并减少复杂换乘。' WHEN 11 THEN '候补结果、退款状态和替代车次需要分别核对，不能混为已购票。' WHEN 12 THEN '预付款前应识别退款条件、履约主体和争议处理入口。' WHEN 13 THEN '索要敏感证件的陌生邮件应先核验域名和官方联系方式。' WHEN 14 THEN '异地就医资料与证件补办材料适用范围不同，不应相互替代。' WHEN 15 THEN '住宿产品应在付款前展示取消期限、费用和不可退条件。' WHEN 16 THEN '紧急联系人信息只用于必要沟通，不得用于营销或公开记录。' ELSE '公共服务投诉需要保留时间、渠道、事项和处理编号。' END
FROM seq;

WITH RECURSIVE seq(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM seq WHERE n<34)
INSERT INTO statute_articles(article_id,statute_id,article_no,seq,heading,text)
SELECT printf('art_reference_%03d',n),printf('legal_reference_%02d',((n-1)%17)+1),printf('第%d条',1+((n-1)/17)),1+((n-1)/17),
       CASE ((n-1)%17)+1 WHEN 1 THEN '时间与票种' WHEN 2 THEN '人工协助' WHEN 3 THEN '变更证据' WHEN 4 THEN '现场核验' WHEN 5 THEN '字段控制' WHEN 6 THEN '最新记录' WHEN 7 THEN '四项核对' WHEN 8 THEN '收费留痕' WHEN 9 THEN '影响范围' WHEN 10 THEN '老人便利' WHEN 11 THEN '状态区分' WHEN 12 THEN '退款条件' WHEN 13 THEN '发件核验' WHEN 14 THEN '适用边界' WHEN 15 THEN '取消披露' WHEN 16 THEN '限定用途' ELSE '受理编号' END,
       CASE ((n-1)%17)+1 WHEN 1 THEN '办理退改时应先确认产品规则和距离发车时间，不能只依据统一费率。' WHEN 2 THEN '老人出行可申请人工服务，同时应准备纸质或大字版行程说明。' WHEN 3 THEN '发生航班变化时应保存状态通知，并在执行替代方案前核对授权。' WHEN 4 THEN '住宿平台确认仅证明预订关系，实际入住仍需遵守实名登记要求。' WHEN 5 THEN '收集证件字段应限于当前业务需要，完成后按约定期限清理副本。' WHEN 6 THEN '预约变更以后应同步更新提醒、路线和对外说明，避免沿用旧号码。' WHEN 7 THEN '支付前需同时核对收款账户、金额、用途及用户是否明确同意。' WHEN 8 THEN '服务收费应形成可核对的项目清单，现金和转账均应留存凭证。' WHEN 9 THEN '道路事件应说明开始、结束、影响程度以及适合行人的替代通道。' WHEN 10 THEN '老人独自出行时应降低换乘复杂度，并把车次与接站口清晰告知。' WHEN 11 THEN '候补失败不等于退款到账，应分别检查订单状态和资金状态。' WHEN 12 THEN '预付项目应在付款前说明履约主体、退款条件与争议处理方式。' WHEN 13 THEN '陌生域名索要身份证件时应停止发送，并从官方渠道独立核验。' WHEN 14 THEN '相邻领域的办事指南只能参考，不能替代当前事项的正式要求。' WHEN 15 THEN '酒店取消条款应明确截止时间、时区和超过期限后的实际费用。' WHEN 16 THEN '联系人电话与关系信息只能用于紧急事项，不应复制到公开台账。' ELSE '提交投诉后应记录受理时间、渠道、编号和下一次跟进节点。' END
FROM seq;
