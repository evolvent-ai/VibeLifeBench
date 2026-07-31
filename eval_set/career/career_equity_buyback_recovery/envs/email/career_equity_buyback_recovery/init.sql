-- emails-mcp env -- career_equity_buyback_recovery -- init.sql
-- 纪辰(gaokai) 个人邮箱. Reference 2026-06-08.
-- 叙事邮件由 event.yaml 在运行时注入(id 101..108); 种子邮件 id < 100。
BEGIN;
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES (1,'gaokai_dev@163.com','纪辰 (Ji Chen)','2018-08-01T00:00:00Z');
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1,1,'<hr-notice@yiweicloud.com>','【弈维数科】关于岗位优化的书面通知','弈维数科 HR 宋珂 <hr.songke@yiweicloud.com>','["gaokai_dev@163.com"]','2026-06-08T10:00:00Z',
   '纪辰你好：因公司业务调整，你所在的交易中台组整体撤销，依据《劳动合同法》第四十条，公司决定与你解除劳动合同，最后工作日为 2026-06-30。股权回购差额方案与签署安排另函发送。请知悉。',1,1,'{}',120,'2026-06-08T10:00:00Z'),
  (2,1,'<welcome@lagou.com>','拉勾招聘：为你推荐了新职位','拉勾网 <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-06-09T08:00:00Z',
   '根据你的简历，本周为你推荐了若干上海后端职位，登录查看。',1,0,'{}',45,'2026-06-09T08:00:00Z'),
  (3,1,'<promo@peixun.com>','【限时】劳动仲裁代理 包赢不成不收费','某法律咨询 <promo@laodong-vip.com>','["gaokai_dev@163.com"]','2026-06-10T09:00:00Z',
   '专业代理劳动仲裁，先交2999元材料费，包赢！加微信 xxxx 立即办理。(广告)',0,0,'{}',52,'2026-06-10T09:00:00Z'),
  (4,1,'<newsletter@infoq.cn>','InfoQ 本周架构精选','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-06-11T08:00:00Z',
   '本周分布式系统与稳定性精选文章……',1,0,'{}',30,'2026-06-11T08:00:00Z'),
  (5,1,'<wife@family.com>','下周产检记得陪我','舒窈 <linyue@family.com>','["gaokai_dev@163.com"]','2026-06-11T19:00:00Z',
   '老公，下周三上午产检，你陪我去。工作的事别太焦虑，我们一起扛。',1,0,'{}',40,'2026-06-11T19:00:00Z');

-- ── 背景往来（工作/家庭/金融/社保/社区/招聘/生活），含回复线程 ──
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (6,1,'<tc-2026q2-plan@yiweicloud.com>','交易中台 Q2 迭代排期（含灰度窗口）','周铭 <zhouming@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-07T10:12:00Z',
   '各位，Q2 排期我贴在 wiki 了。这轮重点是订单链路的分库分表收尾，灰度窗口定在 4/20 和 5/11 两个周一晚上。纪辰负责的账务对账模块排在第二批，麻烦你把回滚方案在灰度前一周提上来。',1,0,NULL,NULL,'{}',249,'2026-04-07T10:12:00Z'),
  (7,1,'<tc-2026q2-plan-re1@yiweicloud.com>','Re: 交易中台 Q2 迭代排期（含灰度窗口）','纪辰 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-07T14:36:00Z',
   '收到。回滚方案我按上次线上事故的复盘模板写，周五前发群里。灰度第二批我这边没问题，只是 5/11 那周我要陪产检，晚上灰度可以，白天的复盘会麻烦挪到下午。',1,0,'<tc-2026q2-plan@yiweicloud.com>','<tc-2026q2-plan@yiweicloud.com>','{}',219,'2026-04-07T14:36:00Z'),
  (8,1,'<tc-2026q2-plan-re2@yiweicloud.com>','Re: 交易中台 Q2 迭代排期（含灰度窗口）','周铭 <zhouming@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-07T15:02:00Z',
   '行，复盘会我挪到 14:30。另外提醒下，这轮之后架构组可能会重新划一次模块归属，具体等通知。',1,0,'<tc-2026q2-plan@yiweicloud.com>','<tc-2026q2-plan@yiweicloud.com>','{}',129,'2026-04-07T15:02:00Z'),
  (9,1,'<oncall-0412@yiweicloud.com>','【值班】4/12 凌晨对账任务超时的处理记录','李哲 <lizhe@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-12T09:30:00Z',
   '昨晚对账任务跑了 3 小时没出结果，我先把批次拆成两半重跑过了。初步看是上游流水表增量太大，索引没走上。纪辰你熟这块，下周有空看下要不要加个时间分区？',1,0,NULL,NULL,'{}',219,'2026-04-12T09:30:00Z'),
  (10,1,'<oncall-0412-re1@yiweicloud.com>','Re: 【值班】4/12 凌晨对账任务超时的处理记录','纪辰 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-13T11:05:00Z',
   '看了下执行计划，确实是全表扫。我加了按 posted_at 的分区并把批次大小从 5 万降到 2 万，昨晚重跑 22 分钟结束。改动已合到主干，回滚开关留着。',1,0,'<oncall-0412@yiweicloud.com>','<oncall-0412@yiweicloud.com>','{}',195,'2026-04-13T11:05:00Z'),
  (11,1,'<arch-review-0421@yiweicloud.com>','架构评审：账务模块与结算域的边界','架构组 <arch@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-21T16:40:00Z',
   '本周四下午两点评审账务与结算的领域边界，会上会讨论模块归属调整。相关同学请提前看下附件里的现状图。纪辰、李哲请务必参加。',1,1,NULL,NULL,'{}',180,'2026-04-21T16:40:00Z'),
  (12,1,'<hr-org-survey@yiweicloud.com>','【HR】组织效能调研问卷（本周内填写）','弈维数科 HR <hr@yiweicloud.com>','["gaokai_dev@163.com"]','2026-04-28T10:00:00Z',
   '为了解各团队协作现状，请于本周五前完成问卷。问卷匿名，结果仅用于组织优化参考。',1,0,NULL,NULL,'{}',117,'2026-04-28T10:00:00Z'),
  (13,1,'<tc-handover-draft@yiweicloud.com>','账务对账模块交接文档（初稿）','纪辰 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-19T18:22:00Z',
   '按周铭要求先把对账模块的交接文档拉了个初稿，涵盖批次调度、异常补偿、和财务侧的接口约定。权限清单那块还差两个系统没梳理完，下周补上。',1,0,NULL,NULL,'{}',198,'2026-05-19T18:22:00Z'),
  (14,1,'<tc-handover-draft-re1@yiweicloud.com>','Re: 账务对账模块交接文档（初稿）','李哲 <lizhe@yiweicloud.com>','["gaokai_dev@163.com"]','2026-05-20T09:15:00Z',
   '看完了，写得挺细。补一句：财务侧那个月结接口去年换过一次签名方式，老文档里还是旧的，建议你在文档里标一下，不然接手的人容易踩。',1,0,'<tc-handover-draft@yiweicloud.com>','<tc-handover-draft@yiweicloud.com>','{}',189,'2026-05-20T09:15:00Z'),
  (15,1,'<family-checkup-0409@family.com>','产检时间又改了','舒窈 <linyue@family.com>','["gaokai_dev@163.com"]','2026-04-09T20:14:00Z',
   '医生说以后固定每周三上午，九点到十一点半这个区间，一直到十月。你把这个时间空出来，别再排会了。这次医生说指标都正常，就是让我少熬夜。',1,1,NULL,NULL,'{}',198,'2026-04-09T20:14:00Z'),
  (16,1,'<family-checkup-0409-re1@family.com>','Re: 产检时间又改了','纪辰 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-09T21:03:00Z',
   '记下了，我把周三上午在日历里锁死。这周的复盘会我已经让周铭挪到下午了。',1,0,'<family-checkup-0409@family.com>','<family-checkup-0409@family.com>','{}',105,'2026-04-09T21:03:00Z'),
  (17,1,'<family-crib@family.com>','婴儿床和推车的链接','舒窈 <linyue@family.com>','["gaokai_dev@163.com"]','2026-05-06T21:40:00Z',
   '我妈说婴儿床她来买，我们就把推车和安全座椅定了吧。我看中两个牌子，晚上回来一起看看。另外月嫂那边中介让我们六月底前定，说好的档期抢手。',1,0,NULL,NULL,'{}',201,'2026-05-06T21:40:00Z'),
  (18,1,'<hospital-notice@shjiaotong-hosp.cn>','产科建档提醒','上海某妇幼保健院 <no-reply@shjiaotong-hosp.cn>','["gaokai_dev@163.com"]','2026-04-15T08:30:00Z',
   '您已完成产科建档。后续产检请携带母子健康手册按预约时间前来，如需改期请提前一个工作日在公众号操作。',1,0,NULL,NULL,'{}',147,'2026-04-15T08:30:00Z'),
  (19,1,'<cmb-stmt-0410@cmbchina.com>','招商银行 4 月账单已出','招商银行 <no-reply@cmbchina.com>','["gaokai_dev@163.com"]','2026-04-10T07:00:00Z',
   '您尾号 9901 的信用卡 4 月账单已生成，应还金额请登录手机银行查询，最后还款日为 4 月 25 日。',1,0,NULL,NULL,'{}',127,'2026-04-10T07:00:00Z'),
  (20,1,'<cmb-payroll-0510@cmbchina.com>','工资入账通知','招商银行 <no-reply@cmbchina.com>','["gaokai_dev@163.com"]','2026-05-10T10:05:00Z',
   '您尾号 8823 的储蓄卡于 5 月 10 日有一笔工资入账，详情请在手机银行查询交易明细。',1,0,NULL,NULL,'{}',112,'2026-05-10T10:05:00Z'),
  (21,1,'<broker-monthly@guojun-sec.com>','您的证券账户 4 月对账单','国君证券 <service@guojun-sec.com>','["gaokai_dev@163.com"]','2026-05-05T09:20:00Z',
   '尊敬的客户，您 4 月的证券账户对账单已生成，可在交易软件「我的-对账单」中查看持仓与资金变动明细。',1,0,NULL,NULL,'{}',142,'2026-05-05T09:20:00Z'),
  (22,1,'<broker-risk@guojun-sec.com>','风险测评到期提醒','国君证券 <service@guojun-sec.com>','["gaokai_dev@163.com"]','2026-05-22T09:00:00Z',
   '您的投资者风险承受能力评估将于下月到期，到期后部分产品将无法买入，请及时重新测评。',0,0,NULL,NULL,'{}',123,'2026-05-22T09:00:00Z'),
  (23,1,'<mortgage-rate@ccb.com>','个人住房贷款利率调整通知','建设银行 <no-reply@ccb.com>','["gaokai_dev@163.com"]','2026-04-18T09:00:00Z',
   '根据最新 LPR 报价，您名下住房贷款利率将于下一还款日起按合同约定重新定价，月供金额将相应调整。',1,0,NULL,NULL,'{}',137,'2026-04-18T09:00:00Z'),
  (24,1,'<shbao-annual@shrsj.gov.cn>','2026 年度社保缴费基数申报提醒','上海人社 <no-reply@shrsj.gov.cn>','["gaokai_dev@163.com"]','2026-05-28T09:00:00Z',
   '本年度社保缴费基数申报期为 6 月 1 日至 6 月 30 日，请通过用人单位或一网通办核对本人申报基数。',0,0,NULL,NULL,'{}',133,'2026-05-28T09:00:00Z'),
  (25,1,'<gjj-balance@shgjj.gov.cn>','公积金账户余额变动','上海公积金中心 <no-reply@shgjj.gov.cn>','["gaokai_dev@163.com"]','2026-05-16T08:00:00Z',
   '您的住房公积金账户于本月发生汇缴，可通过公众号或一网通办查询明细与账户余额。',1,0,NULL,NULL,'{}',114,'2026-05-16T08:00:00Z'),
  (26,1,'<infoq-w15@infoq.cn>','InfoQ 架构周刊：分布式事务的三种落地姿势','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-04-14T08:00:00Z',
   '本期精选：从 TCC 到 Saga，几家一线团队在订单与账务场景下的事务方案对比；以及一篇关于分库分表后对账体系重建的实践总结。',1,0,NULL,NULL,'{}',172,'2026-04-14T08:00:00Z'),
  (27,1,'<gh-digest@github.com>','GitHub：你关注的 3 个仓库有新版本','GitHub <noreply@github.com>','["gaokai_dev@163.com"]','2026-04-25T12:00:00Z',
   'seata 发布 2.3.0，主要修复了 AT 模式下的悬挂问题；另有两个你 star 过的项目发布了小版本。',1,0,NULL,NULL,'{}',121,'2026-04-25T12:00:00Z'),
  (28,1,'<geekbang-course@geekbang.org>','你购买的课程更新了 2 讲','极客时间 <no-reply@geekbang.org>','["gaokai_dev@163.com"]','2026-05-12T20:00:00Z',
   '《分布式系统设计》更新了「一致性协议的工程取舍」等 2 讲，累计学习进度 62%。',0,0,NULL,NULL,'{}',109,'2026-05-12T20:00:00Z'),
  (29,1,'<lagou-rec-0420@lagou.com>','拉勾：本周为你匹配到 12 个职位','拉勾网 <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-04-20T09:00:00Z',
   '根据你的简历方向（Java/Go 后端、分布式），本周为你匹配到 12 个上海地区职位，登录查看详情。',1,0,NULL,NULL,'{}',129,'2026-04-20T09:00:00Z'),
  (30,1,'<boss-view-0509@zhipin.com>','有 3 家企业查看了你的简历','BOSS直聘 <no-reply@zhipin.com>','["gaokai_dev@163.com"]','2026-05-09T18:30:00Z',
   '近 7 天有 3 家企业查看了你的在线简历。完善项目经历可提升被查看概率。',0,0,NULL,NULL,'{}',99,'2026-05-09T18:30:00Z'),
  (31,1,'<maimai-msg@maimai.cn>','脉脉：你有 2 条未读私信','脉脉 <no-reply@maimai.cn>','["gaokai_dev@163.com"]','2026-05-25T21:10:00Z',
   '有猎头向你发送了私信，登录查看。',0,0,NULL,NULL,'{}',48,'2026-05-25T21:10:00Z'),
  (32,1,'<sh-power-0505@sgcc.com.cn>','4 月电费账单','国网上海电力 <no-reply@sgcc.com.cn>','["gaokai_dev@163.com"]','2026-05-05T10:00:00Z',
   '您 4 月用电量 218 度，费用已从绑定账户代扣成功。',1,0,NULL,NULL,'{}',68,'2026-05-05T10:00:00Z'),
  (33,1,'<lease-renew@family.com>','房东说租约的事','二房东-张 <zhangsan_landlord@163.com>','["gaokai_dev@163.com"]','2026-05-30T19:20:00Z',
   '小纪，你这套的租约是八月底到期。我这边想涨一点，涨幅按周边行情来。你要是续租提前跟我说，不续的话也早点讲，我好挂出去。',0,1,NULL,NULL,'{}',177,'2026-05-30T19:20:00Z'),
  (34,3,'<draft-handover-checklist@163.com>','（草稿）交接清单待补项','纪辰 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-21T22:40:00Z',
   '待补：财务月结接口签名方式、灰度开关清单、值班文档权限、对账异常处理 SOP 的最新版本。',0,0,NULL,NULL,'{}',125,'2026-05-21T22:40:00Z'),
  (35,3,'<draft-resume-update@163.com>','（草稿）简历更新要点','纪辰 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-06-02T23:15:00Z',
   '要补：分库分表收尾的量化结果、对账任务从 3 小时降到 22 分钟这条、带过 5 人小组的经历。',0,0,NULL,NULL,'{}',124,'2026-06-02T23:15:00Z'),
  (36,5,'<promo-loan@xinyongdai.example.net>','【预审通过】您有一笔 30 万额度待激活','快信贷 <promo@xinyongdai.example.net>','["gaokai_dev@163.com"]','2026-04-30T11:20:00Z',
   '恭喜您通过预审，最高可借 30 万，当天放款，点击链接激活额度。',0,0,NULL,NULL,'{}',88,'2026-04-30T11:20:00Z'),
  (37,5,'<promo-invest@licai-vip.example.net>','年化 12% 稳健理财，名额有限','财富管家 <vip@licai-vip.example.net>','["gaokai_dev@163.com"]','2026-05-27T15:45:00Z',
   '优质项目开放认购，年化 12%，起投 5 万，先到先得。',0,0,NULL,NULL,'{}',70,'2026-05-27T15:45:00Z');
COMMIT;

BEGIN;
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (38,1,'<20240520-rsu-plan@yiweicloud.com>','【历史文件】2024 年限制性股票授予确认与离职结算规则','弈维数科股权激励办公室 <equity@yiweicloud.com>','["gaokai_dev@163.com"]','2024-05-20T09:00:00Z',
   '纪辰你好：附件所列 5000 股限制性股票已完成归属。根据你签收的《2024 年限制性股票授予确认书》第 8.3 条，员工离职时，已归属份额以离职回购基准日可查询的市场收盘价作为结算价格；未归属份额按计划规则失效。若公司拟调整已归属份额的结算方式，应另行书面说明并取得双方确认。请妥善保存本邮件及授予确认书。',1,1,NULL,NULL,'{}',430,'2024-05-20T09:00:00Z');
COMMIT;
