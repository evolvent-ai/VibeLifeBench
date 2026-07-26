-- emails-mcp env -- career_espp_refund_recovery -- init.sql
-- 卞翎(gaokai) 个人邮箱. Reference 2026-06-08.
-- 叙事邮件由 event.yaml 在运行时注入(id 101..108); 种子邮件 id < 100。
BEGIN;
DELETE FROM account_config;
INSERT INTO account_config (id, email, name, created_at) VALUES (1,'gaokai_dev@163.com','卞翎 (Bian Ling)','2018-08-01T00:00:00Z');
DELETE FROM folders;
INSERT INTO folders (id, name) VALUES (1,'INBOX'),(2,'Sent'),(3,'Drafts'),(4,'Trash'),(5,'Spam');
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1,1,'<hr-notice@ximingsemi.com>','【矽鸣半导】关于岗位优化的书面通知','矽鸣半导 HR 陆谦 <hr.luqian@ximingsemi.com>','["gaokai_dev@163.com"]','2026-06-08T10:00:00Z',
   '卞翎你好：因公司业务调整，你所在的 SC7 验证组整体撤销，依据《劳动合同法》第四十条，公司决定与你解除劳动合同，最后工作日为 2026-06-30。持股计划价差方案与签署安排另函发送。请知悉。',1,1,'{}',120,'2026-06-08T10:00:00Z'),
  (2,1,'<welcome@lagou.com>','拉勾招聘：为你推荐了新职位','拉勾网 <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-06-09T08:00:00Z',
   '根据你的简历，本周为你推荐了若干上海后端职位，登录查看。',1,0,'{}',45,'2026-06-09T08:00:00Z'),
  (3,1,'<promo@peixun.com>','【限时】劳动仲裁代理 包赢不成不收费','某法律咨询 <promo@laodong-vip.com>','["gaokai_dev@163.com"]','2026-06-10T09:00:00Z',
   '专业代理劳动仲裁，先交2999元材料费，包赢！加微信 xxxx 立即办理。(广告)',0,0,'{}',52,'2026-06-10T09:00:00Z'),
  (4,1,'<newsletter@infoq.cn>','InfoQ 本周架构精选','InfoQ <news@infoq.cn>','["gaokai_dev@163.com"]','2026-06-11T08:00:00Z',
   '本周分布式系统与稳定性精选文章……',1,0,'{}',30,'2026-06-11T08:00:00Z'),
  (5,1,'<wife@family.com>','下周产检记得陪我','舒窈 <linyue@family.com>','["gaokai_dev@163.com"]','2026-06-11T19:00:00Z',
   '老公，下周三上午产检，你陪我去。工作的事别太焦虑，我们一起扛。',1,0,'{}',40,'2026-06-11T19:00:00Z');

-- ── 背景往来（项目/家庭/金融/社保/行业/招聘/生活），含回复线程 ──
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (6,1,'<sv-tapeout-w15@ximingsemi.com>','SC7 项目流片前回归清单','陆敏 <lumin@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-08T09:40:00Z',
   '各位，SC7 计划 6 月底送 tapeout，回归清单我更新到第 3 版。卞翎负责的总线一致性验证环境，麻烦在 5 月中之前把随机激励的覆盖率补到 95% 以上，剩下的 corner case 走定向用例。',1,0,NULL,NULL,'{}',234,'2026-04-08T09:40:00Z'),
  (7,1,'<sv-tapeout-w15-re1@ximingsemi.com>','Re: SC7 项目流片前回归清单','卞翎 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-08T15:20:00Z',
   '收到。目前功能覆盖率 88%，缺的主要在跨时钟域和异常握手两块。定向用例我这周开始补，预计五一前能到 93%，剩下的靠 formal 补。另外每周三上午我要陪产检，例会麻烦排下午。',1,0,'<sv-tapeout-w15@ximingsemi.com>','<sv-tapeout-w15@ximingsemi.com>','{}',238,'2026-04-08T15:20:00Z'),
  (8,1,'<sv-tapeout-w15-re2@ximingsemi.com>','Re: SC7 项目流片前回归清单','陆敏 <lumin@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-08T16:05:00Z',
   '例会挪到周三下午三点。formal 那边资源紧张，你先跟老许对一下机时。',1,0,'<sv-tapeout-w15@ximingsemi.com>','<sv-tapeout-w15@ximingsemi.com>','{}',94,'2026-04-08T16:05:00Z'),
  (9,1,'<regress-fail-0417@ximingsemi.com>','夜间回归 12 个用例失败，疑似环境问题','许志远 <xuzhiyuan@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-17T08:50:00Z',
   '昨晚回归挂了 12 个，日志里都是同一个断言。我看了下不像 RTL 问题，更像是上周升级 VCS 之后 UVM 版本没对齐。卞翎你那边环境是不是也升了？',1,0,NULL,NULL,'{}',190,'2026-04-17T08:50:00Z'),
  (10,1,'<regress-fail-0417-re1@ximingsemi.com>','Re: 夜间回归 12 个用例失败，疑似环境问题','卞翎 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-17T10:30:00Z',
   '确认是版本问题。我把 UVM 锁回 1.2 并在 Makefile 里固化了版本号，重跑 12 个用例全过。建议后面工具链升级走统一公告，别各自升。',1,0,'<regress-fail-0417@ximingsemi.com>','<regress-fail-0417@ximingsemi.com>','{}',174,'2026-04-17T10:30:00Z'),
  (11,1,'<eda-license@ximingsemi.com>','【IT】EDA 工具 license 池调整通知','IT 支持 <it@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-24T17:10:00Z',
   '因预算调整，仿真类 license 并发数将从 5 月起下调。请各项目组按优先级申报机时，夜间批量任务建议错峰提交。',1,0,NULL,NULL,'{}',150,'2026-04-24T17:10:00Z'),
  (12,1,'<hr-org-survey@ximingsemi.com>','【HR】组织效能调研问卷','矽鸣半导 HR <hr@ximingsemi.com>','["gaokai_dev@163.com"]','2026-04-29T10:00:00Z',
   '请各位于本周五前填写本次调研，内容涉及项目协作、跨组沟通与工具链使用体验。问卷不记名，汇总结果用于下半年团队规划。',1,0,NULL,NULL,'{}',117,'2026-04-29T10:00:00Z'),
  (13,1,'<handover-verif-env@ximingsemi.com>','总线验证环境交接说明（初稿）','卞翎 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-20T19:05:00Z',
   '把总线一致性验证环境的交接文档拉了初稿：目录结构、随机种子管理、覆盖率合并脚本、以及和 DV 平台组的接口约定。机时申请那部分还要跟 IT 确认权限怎么转。',1,0,NULL,NULL,'{}',218,'2026-05-20T19:05:00Z'),
  (14,1,'<handover-verif-env-re1@ximingsemi.com>','Re: 总线验证环境交接说明（初稿）','许志远 <xuzhiyuan@ximingsemi.com>','["gaokai_dev@163.com"]','2026-05-21T11:20:00Z',
   '看过了。提醒一点：覆盖率合并脚本里写死了你个人的 scratch 路径，接手的人跑不了，记得改成变量。',1,0,'<handover-verif-env@ximingsemi.com>','<handover-verif-env@ximingsemi.com>','{}',135,'2026-05-21T11:20:00Z'),
  (15,1,'<family-checkup-0410@family.com>','产检改成固定周三了','舒窈 <linyue@family.com>','["gaokai_dev@163.com"]','2026-04-10T20:30:00Z',
   '医生说从这周起固定每周三上午九点到十一点半，一直到十月。你把时间空出来。这次各项指标都正常，就是让我别老熬夜。',1,1,NULL,NULL,'{}',165,'2026-04-10T20:30:00Z'),
  (16,1,'<family-checkup-0410-re1@family.com>','Re: 产检改成固定周三了','卞翎 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-04-10T21:12:00Z',
   '知道了，日历上周三上午我锁死了。项目例会我已经让陆敏挪到下午。',1,0,'<family-checkup-0410@family.com>','<family-checkup-0410@family.com>','{}',93,'2026-04-10T21:12:00Z'),
  (17,1,'<family-yuesao@family.com>','月嫂中介催我们定档期','舒窈 <linyue@family.com>','["gaokai_dev@163.com"]','2026-05-08T21:55:00Z',
   '中介说好一点的月嫂六月底就得定，不然九月的档期抢不到。价格比去年涨了不少。还有婴儿床我妈说她买，我们定推车和安全座椅就行。',0,0,NULL,NULL,'{}',183,'2026-05-08T21:55:00Z'),
  (18,1,'<hospital-record@shfuyou-hosp.cn>','产科建档完成通知','上海某妇幼保健院 <no-reply@shfuyou-hosp.cn>','["gaokai_dev@163.com"]','2026-04-16T08:20:00Z',
   '您已完成产科建档，后续产检请携带母子健康手册按预约时段前来，改期请提前一个工作日在公众号操作。',1,0,NULL,NULL,'{}',141,'2026-04-16T08:20:00Z'),
  (19,1,'<cmb-stmt-0412@cmbchina.com>','招商银行 4 月账单已出','招商银行 <no-reply@cmbchina.com>','["gaokai_dev@163.com"]','2026-04-12T07:00:00Z',
   '您尾号 9901 的信用卡 4 月账单已生成，最后还款日 4 月 27 日，请登录手机银行查询应还金额。',1,0,NULL,NULL,'{}',124,'2026-04-12T07:00:00Z'),
  (20,1,'<ccb-mortgage@ccb.com>','住房贷款还款提醒','建设银行 <no-reply@ccb.com>','["gaokai_dev@163.com"]','2026-05-18T09:00:00Z',
   '您名下住房贷款本期月供将于还款日从签约账户扣划，请保持账户余额充足。',1,0,NULL,NULL,'{}',102,'2026-05-18T09:00:00Z'),
  (21,1,'<broker-stmt@haitong-sec.com>','您的证券账户 4 月对账单','海通证券 <service@haitong-sec.com>','["gaokai_dev@163.com"]','2026-05-06T09:15:00Z',
   '您 4 月的账户对账单已生成，可在交易软件查看持仓、资金流水与股份变动明细。',1,0,NULL,NULL,'{}',108,'2026-05-06T09:15:00Z'),
  (22,1,'<broker-espp@haitong-sec.com>','限售股份解禁提示','海通证券 <service@haitong-sec.com>','["gaokai_dev@163.com"]','2026-05-21T09:00:00Z',
   '您账户内部分限售股份的锁定期即将届满，解禁后可正常交易，具体日期以登记结算机构数据为准。',0,1,NULL,NULL,'{}',132,'2026-05-21T09:00:00Z'),
  (23,1,'<gjj-notice@shgjj.gov.cn>','公积金月度汇缴到账','上海公积金中心 <no-reply@shgjj.gov.cn>','["gaokai_dev@163.com"]','2026-05-17T08:00:00Z',
   '您的住房公积金账户本月已完成汇缴，可通过一网通办查询余额与缴存明细。',1,0,NULL,NULL,'{}',102,'2026-05-17T08:00:00Z'),
  (24,1,'<shrsj-base@shrsj.gov.cn>','社保缴费基数申报期提醒','上海人社 <no-reply@shrsj.gov.cn>','["gaokai_dev@163.com"]','2026-05-29T09:00:00Z',
   '本年度社保缴费基数申报期为 6 月 1 日至 6 月 30 日，请核对本人申报基数是否与实际工资相符。',0,0,NULL,NULL,'{}',127,'2026-05-29T09:00:00Z'),
  (25,1,'<eetimes-w16@eetimes.cn>','EE Times：先进封装产能与验证方法学','EE Times <news@eetimes.cn>','["gaokai_dev@163.com"]','2026-04-19T08:00:00Z',
   '本期关注 chiplet 互连协议的验证挑战，以及几家设计公司在覆盖率驱动验证上的实践对比。',1,0,NULL,NULL,'{}',120,'2026-04-19T08:00:00Z'),
  (26,1,'<accellera-news@accellera.org>','UVM 相关规范更新摘要','Accellera <news@accellera.org>','["gaokai_dev@163.com"]','2026-05-04T12:00:00Z',
   '本次更新涉及寄存器抽象层的若干澄清与两个已知问题的修订说明。',1,0,NULL,NULL,'{}',90,'2026-05-04T12:00:00Z'),
  (27,1,'<geekbang-course@geekbang.org>','课程更新提醒','极客时间 <no-reply@geekbang.org>','["gaokai_dev@163.com"]','2026-05-13T20:00:00Z',
   '《数字 IC 验证进阶》更新 2 讲，累计学习进度 55%。',0,0,NULL,NULL,'{}',68,'2026-05-13T20:00:00Z'),
  (28,1,'<lagou-rec-0422@lagou.com>','拉勾：本周匹配到 9 个职位','拉勾网 <no-reply@lagou.com>','["gaokai_dev@163.com"]','2026-04-22T09:00:00Z',
   '根据你的简历方向（IC 验证、后端），本周为你匹配到 9 个上海地区职位。',1,0,NULL,NULL,'{}',99,'2026-04-22T09:00:00Z'),
  (29,1,'<boss-view-0511@zhipin.com>','有 2 家企业查看了你的简历','BOSS直聘 <no-reply@zhipin.com>','["gaokai_dev@163.com"]','2026-05-11T18:40:00Z',
   '近 7 天有 2 家企业查看了你的在线简历。',0,0,NULL,NULL,'{}',54,'2026-05-11T18:40:00Z'),
  (30,1,'<liepin-hunter@liepin.com>','猎头顾问想与你联系','猎聘 <no-reply@liepin.com>','["gaokai_dev@163.com"]','2026-05-26T20:15:00Z',
   '有顾问关注了你的简历并发来沟通请求，登录查看。',0,0,NULL,NULL,'{}',69,'2026-05-26T20:15:00Z'),
  (31,1,'<sh-power-0507@sgcc.com.cn>','4 月电费账单','国网上海电力 <no-reply@sgcc.com.cn>','["gaokai_dev@163.com"]','2026-05-07T10:00:00Z',
   '您 4 月用电量 203 度，费用已代扣成功。',1,0,NULL,NULL,'{}',53,'2026-05-07T10:00:00Z'),
  (32,1,'<parking-renew@office-park.cn>','写字楼车位月租到期提醒','园区物业 <service@office-park.cn>','["gaokai_dev@163.com"]','2026-05-24T10:30:00Z',
   '您的车位月租将于下月初到期，如需续租请在物业系统提交申请。',0,0,NULL,NULL,'{}',87,'2026-05-24T10:30:00Z'),
  (33,1,'<lease-talk@family.com>','房东提到租约的事','房东-王 <wanglaoshi_fang@163.com>','["gaokai_dev@163.com"]','2026-05-31T19:40:00Z',
   '小卞，你那套八月底到期。我想按周边行情调一点租金，你要是续租提前说一声，不续我也好安排。',0,1,NULL,NULL,'{}',132,'2026-05-31T19:40:00Z'),
  (34,3,'<draft-verif-checklist@163.com>','（草稿）交接待补项','卞翎 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-05-22T22:30:00Z',
   '待补：覆盖率脚本里的硬编码路径、机时申请权限转移、随机种子归档位置、DV 平台组接口人。',0,0,NULL,NULL,'{}',126,'2026-05-22T22:30:00Z'),
  (35,3,'<draft-resume@163.com>','（草稿）简历要点','卞翎 <gaokai_dev@163.com>','["gaokai_dev@163.com"]','2026-06-03T23:05:00Z',
   '要写：SC7 总线一致性验证覆盖率 88%→95%、定位并修复工具链版本导致的 12 例回归失败、带过 4 人验证小组。',0,0,NULL,NULL,'{}',144,'2026-06-03T23:05:00Z'),
  (36,5,'<promo-card@xinka-vip.example.net>','【专享】高额信用卡极速下卡','办卡专员 <vip@xinka-vip.example.net>','["gaokai_dev@163.com"]','2026-05-02T11:00:00Z',
   '内部渠道，最高额度 20 万，三天下卡，点击申请。',0,0,NULL,NULL,'{}',67,'2026-05-02T11:00:00Z');
COMMIT;

BEGIN;
INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, in_reply_to, references_header, headers_json, size, created_at) VALUES
  (37,1,'<20240418-espp-plan@ximingsemi.com>','【历史文件】员工持股计划份额确认与离职赎回规则','矽鸣半导持股计划办公室 <espp@ximingsemi.com>','["gaokai_dev@163.com"]','2024-05-20T09:00:00Z',
   '卞翎你好：你名下 4955 股员工持股计划份额已完成归属。根据你签收的《员工持股计划份额确认书》第 7.2 条，员工离职时，已归属份额以离职赎回基准日可查询的市场收盘价作为结算价格；未归属份额按计划规则失效。若公司拟调整已归属份额的结算方式，应另行书面说明并取得双方确认。请妥善保存本邮件及确认书。',1,1,NULL,NULL,'{}',425,'2024-05-20T09:00:00Z');
COMMIT;
