-- Curated Stage-0 seed for career_background_check_consent / email.

BEGIN;

INSERT INTO account_config (id, email, name, created_at) VALUES
  (1, 'sang.wu@163.com', 'Sang Wu', '2018-08-01T00:00:00Z');

INSERT INTO folders (id, name) VALUES
  (1, 'INBOX'),
  (2, 'Sent'),
  (3, 'Drafts'),
  (4, 'Trash'),
  (5, 'Spam');

INSERT INTO messages (id, folder_id, message_id, subject, from_addr, to_addr_json, date, body_text, is_read, is_important, headers_json, size, created_at) VALUES
  (1, 1, '<20260608.020000.cegobxbrdhx@yanmunet.com>', '【Yanmu Network】translated textposition restructuringtranslated textnotice', 'Yanmu Network HR Yi Hui <hr.yihui@yanmunet.com>', '["sang.wu@163.com"]', '2026-06-08T02:00:00Z', 'Sang WuHello：translated textcompanytranslated text，transaction middlewaretranslated text，companybasisLabor Contract Lawtranslated textstarttranslated text，last working daytranslated text 2026-06-30。severanceproposaltranslated textbackground-check authorizationdisputetranslated text。', 1, 1, '{}', 227, '2026-06-08T02:00:00Z'),
  (2, 1, '<20260607.012000.owi2jtoduzx@cmbchina.example>', 'translated textmortgagetranslated text', 'China Merchants Bank <service@cmbchina.example>', '["sang.wu@163.com"]', '2026-06-07T01:20:00Z', 'translated textmortgagetranslated text 6 translated text 12 translated text，translated textconfirmpayroll accounttranslated text；emaildo nottranslated textreplytranslated text。', 1, 0, '{}', 121, '2026-06-07T01:20:00Z'),
  (3, 1, '<20260606.031000.p7yzilrk6yx@mch-sh.example>', 'translated text', 'translated text <appointment@mch-sh.example>', '["sang.wu@163.com"]', '2026-06-06T03:10:00Z', 'Ling Botranslated textweektranslated text，translated text；translated text。', 1, 1, '{}', 114, '2026-06-06T03:10:00Z'),
  (4, 1, '<20260605.113000.3ddbt6fyiwx@family.example>', 'householdweektranslated text', 'Ling Bo <ling.bo@family.example>', '["sang.wu@163.com"]', '2026-06-05T11:30:00Z', 'translated text、translated text，weektranslated textfirsttranslated text，translated text。', 1, 0, '{}', 102, '2026-06-05T11:30:00Z'),
  (5, 1, '<20260604.081500.txpar344mnx@yanmunet.com>', 'transactionsystemtranslated textstabletranslated textretrospective', 'Yanmu Network translated text <architecture@yanmunet.com>', '["sang.wu@163.com"]', '2026-06-04T08:15:00Z', 'translated textservicetranslated text，retrospectivetranslated texttop uptranslated textdatatranslated textrecord。', 1, 0, '{}', 114, '2026-06-04T08:15:00Z'),
  (6, 1, '<20260603.064000.beeuuae3qix@yanmunet.com>', 'departuretranslated textmaterialstranslated textmemo', 'Yanmu Network IT servicetranslated text <it-service@yanmunet.com>', '["sang.wu@163.com"]', '2026-06-03T06:40:00Z', 'translated textworktranslated text；translated textdata、translated text。', 1, 1, '{}', 120, '2026-06-03T06:40:00Z'),
  (7, 1, '<20260602.003000.ja22uvrn3qx@jobs.example>', 'Shanghaibackendroleweektranslated text', 'Recruiting Platform <digest@jobs.example>', '["sang.wu@163.com"]', '2026-06-02T00:30:00Z', 'translated textweekShanghainewtransaction、translated textplatform、logisticstranslated textfintechbackendrole；translated textjob applicationtranslated textviewemployment arrangement。', 1, 0, '{}', 123, '2026-06-02T00:30:00Z'),
  (8, 1, '<20260601.090000.i5bgwv7cusx@github.example>', 'translated textsecurityupdate', 'GitHub Notifications <notifications@github.example>', '["sang.wu@163.com"]', '2026-06-01T09:00:00Z', 'translated textneedtranslated text，translated text。', 0, 0, '{}', 105, '2026-06-01T09:00:00Z'),
  (9, 1, '<20260530.022000.fgfzkt4pv5x@property.example>', 'communitytranslated textreminder', 'translated textservicetranslated text <service@property.example>', '["sang.wu@163.com"]', '2026-05-30T02:20:00Z', 'translated text，onlinetranslated text。', 1, 0, '{}', 96, '2026-05-30T02:20:00Z'),
  (10, 1, '<20260528.011000.aj3fkbhxpcx@tax.example>', 'annualtranslated textincomplete', 'translated textservice <notice@tax.example>', '["sang.wu@163.com"]', '2026-05-28T01:10:00Z', 'systemtranslated textannualtranslated textdrafttranslated text，translated textpassedtranslated textreconciletranslated text。', 1, 0, '{}', 93, '2026-05-28T01:10:00Z'),
  (11, 1, '<20260526.073000.cthj56af64x@dev-sh.example>', 'translated textconfirm：translated text', 'Shanghaidevelopmenttranslated textcommunity <events@dev-sh.example>', '["sang.wu@163.com"]', '2026-05-26T07:30:00Z', 'translated textweektranslated textafternoontranslated textcasetranslated text，locationtranslated textdaytranslated text。', 1, 0, '{}', 90, '2026-05-26T07:30:00Z'),
  (12, 1, '<20260524.040000.olovg7fpiwx@broadband.example>', 'translated text', 'householdtranslated text <customer@broadband.example>', '["sang.wu@163.com"]', '2026-05-24T04:00:00Z', 'currenttranslated text，translated textproposal；translated textemailtranslated text。', 1, 0, '{}', 102, '2026-05-24T04:00:00Z'),
  (13, 1, '<20260522.120000.7q6zogu6a7x@163.com>', 'resumetranslated text', 'Sang Wu <sang.wu@163.com>', '["sang.wu@163.com"]', '2026-05-22T12:00:00Z', 'translated text：translated textresumetranslated textretaintranslated text，translated text、translated text、identitytranslated texthouseholdhealth information。', 1, 1, '{}', 150, '2026-05-22T12:00:00Z'),
  (14, 1, '<20260520.024000.sl4zil3inkx@library-sh.example>', 'translated textreminder', 'Shanghaitranslated text <notice@library-sh.example>', '["sang.wu@163.com"]', '2026-05-20T02:40:00Z', '《datatranslated textsystemtranslated text》translated text，translated text。', 1, 0, '{}', 87, '2026-05-20T02:40:00Z'),
  (15, 1, '<20260518.052000.s3idlmlh7kx@checkup-sh.example>', 'physical examinationtranslated text', 'physical examinationtranslated text <report@checkup-sh.example>', '["sang.wu@163.com"]', '2026-05-18T05:20:00Z', 'translated textphysical examinationtranslated textpassedtranslated textview；translated texthealthmaterials，translated textreconcilepurposetranslated textauthorizationscope。', 1, 1, '{}', 135, '2026-05-18T05:20:00Z'),
  (16, 1, '<20260515.014500.icme7y243ux@insurance.example>', 'householdtranslated textannualtranslated text', 'translated textservice <policy@insurance.example>', '["sang.wu@163.com"]', '2026-05-15T01:45:00Z', 'annualtranslated text，translated text；translated textpassedtranslated textidentity。', 1, 0, '{}', 108, '2026-05-15T01:45:00Z'),
  (17, 1, '<20260512.091000.pv7lcwg67zx@shjug.example>', 'Java translated textmaterials', 'Shanghai JUG <newsletter@shjug.example>', '["sang.wu@163.com"]', '2026-05-12T09:10:00Z', 'translated textmaterialstranslated text、GC translated textservicetranslated textcase，translated text。', 0, 0, '{}', 96, '2026-05-12T09:10:00Z'),
  (18, 1, '<20260509.002000.3jmawywtmox@cloud.example>', 'translated textreminder', 'translated textservice <billing@cloud.example>', '["sang.wu@163.com"]', '2026-05-09T00:20:00Z', 'translated textaccounttranslated text，translated textthentranslated textdatatranslated text。', 1, 0, '{}', 90, '2026-05-09T00:20:00Z'),
  (19, 1, '<20260506.030000.hgurrxmbarx@property.example>', 'translated text', 'translated text <engineering@property.example>', '["sang.wu@163.com"]', '2026-05-06T03:00:00Z', 'translated textweektranslated textmorningtranslated text，translated text。', 1, 0, '{}', 69, '2026-05-06T03:00:00Z'),
  (20, 1, '<20260502.100000.ymhbog3xp6x@163.com>', 'translated text', 'Sang Wu <sang.wu@163.com>', '["sang.wu@163.com"]', '2026-05-02T10:00:00Z', 'translated text：Yanmu Networktranslated text，translated textreconcileservice periodtranslated textsalarytranslated text。', 1, 1, '{}', 135, '2026-05-02T10:00:00Z');

INSERT INTO _counters (key, value) VALUES
  ('message_seq', 20),
  ('draft_seq', 0);

COMMIT;
