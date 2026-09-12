-- legal_search_mock career_chronic_disclosure_boundary — init.sql
-- A synthesized English text (labor dispute) research corpus for a career evidence benchmark:
--   • 6 courts/English text across Shanghai/English text
--   • 4 statutes: English text + English text + English text + English text, with their key articles (English text simplified, public-domain style)
--   • 22 task-focused judgments + 55 additional published-style judgments = 77 cases (English text/English text/English text/noncompete restriction ... )
--   • citation links from cases → statute articles (and a few case→case references)
--   • task-specific user usr_feng_yi with 2 saved cases + private research notes
-- All party names anonymized (English text/English text). All text original/synthesized.
-- Reference date: 2026-05-20 (task-level only; the server has no clock).

BEGIN;

-- ── Courts / English text ─────────────────────────────────────────────
INSERT INTO courts (court_id, name, level, region) VALUES
  ('court_sh_pudong',   'English text',       'English text',   'English text'),
  ('court_sh_minhang',  'English text',         'English text',   'English text'),
  ('court_sh_no1',      'English text',       'English text',   'English text'),
  ('court_sh_high',     'English text',           'English text',   'English text'),
  ('court_bj_chaoyang', 'English text',         'English text',   'English text'),
  ('arb_sh_pudong',     'English text', 'English text', 'English text');

-- ── Statutes ───────────────────────────────────────────────────────
INSERT INTO statutes (statute_id, name, short_name, issuer, effective_date, status, summary) VALUES
  ('stat_lcl',  'English text', 'English text', 'English text', '2008-01-01', 'English text',
    'English text、English text、English text、English text，English text，English text、English text、English text。'),
  ('stat_ll',   'English text', 'English text', 'English text', '1995-01-01', 'English text',
    'English text，English text、English text、English text、English text。');

-- ── Statute articles (English text) ─────────────────────────────────────────
-- English text key articles
INSERT INTO statute_articles (article_id, statute_id, article_no, seq, heading, text) VALUES
  ('law-lcl-010-6sqxqt7ax', 'stat_lcl', 'English text',     10, 'English text',
    'English text，English text。English text，English text，English text。'),
  ('law-lcl-036-cwreyvhcx', 'stat_lcl', 'English text', 36, 'English text',
    'English text，English text。'),
  ('law-lcl-038-dcs4qbtqx', 'stat_lcl', 'English text', 38, 'English text',
    'English text、English text、English text，English text。'),
  ('law-lcl-039-so63r3rex', 'stat_lcl', 'English text', 39, 'English text（English text）',
    'English text、English text、English text，English text。'),
  ('law-lcl-040-n3s2ei6mx', 'stat_lcl', 'English text',   40, 'English text',
    'English text，English text，English text：English text；English text；English text。'),
  ('law-lcl-046-jtbn7kdsx', 'stat_lcl', 'English text', 46, 'English text',
    'English text，English text：English text；English text；English text、English text；English text。'),
  ('law-lcl-047-jfewut5kx', 'stat_lcl', 'English text', 47, 'English text',
    'English text，English text。English text，English text；English text，English text。'),
  ('law-lcl-048-sib27mx5x', 'stat_lcl', 'English text', 48, 'English text',
    'English text，English text，English text；English text，English text。'),
  ('law-lcl-082-bkp4xk6vx', 'stat_lcl', 'English text', 82, 'English text',
    'English text，English text。'),
  ('law-lcl-087-ugz2y7vjx', 'stat_lcl', 'English text', 87, 'English text',
    'English text，English text。');

-- English text key articles
INSERT INTO statute_articles (article_id, statute_id, article_no, seq, heading, text) VALUES
  ('art_ll_036', 'stat_ll', 'English text', 36, 'English text',
    'English text、English text。'),
  ('art_ll_041', 'stat_ll', 'English text', 41, 'English text',
    'English text，English text，English text；English text，English text。'),
  ('art_ll_044', 'stat_ll', 'English text', 44, 'English text',
    'English text，English text；English text，English text；English text，English text。'),
  ('art_ll_050', 'stat_ll', 'English text', 50, 'English text',
    'English text，English text。');

-- ── Cases (anonymized judgments) ────────────────────────────────────
INSERT INTO cases (case_id, case_number, title, court_id, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords) VALUES
  ('case_001', '(2025)English text0115English text12001English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2025-11-18',
    'English text：English text（English text）；English text：English text',
    'English text"English text"English text，English text，English text，English text。',
    'English text2019English text3English text，English text25000English text。2025English text6English text，English text，English text。English text，English text2NEnglish text。',
    'English text，English text，English text，English text，English text，English text、English text。',
    'English text"English text"English text，English text，English text，English text。',
    'English text、English text325000English text（25000English text×6.5English text×2）；English text、English text。',
    'English text', 'English text,English text,2N,English text,English text'),

  ('case_002', '(2025)English text0112English text08842English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-09-22',
    'English text：English text（English text）；English text：English text',
    'English text，English text，English text。',
    'English text2022English text，English text9000English text，English text。English text2024English text52English text，English text。',
    'English text，English text，English text。English text，English text。',
    'English text，English text；English text，English text。',
    'English text、English text2024English text43034English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_003', '(2025)English text0115English text09931English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2025-08-30',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2024English text9English text1English text，English text。English text2025English text5English text，English text12000English text。English text2024English text10English text1English text。',
    'English text、English text，English text，English text。English text，English text。',
    'English text，English text，English text。',
    'English text、English text2024English text10English text1English text2025English text5English text96000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_004', '(2025)English text0112English text07765English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-07-15',
    'English text：English text（English text）；English text：English text',
    'English text，English text，English text。',
    'English text2017English text，English text8000English text。English text2023English text。2025English text3English text，English text。',
    'English text，English text，English text；English text、English text，English text，English text。',
    'English text，English text，English text（N），English text。',
    'English text、English text64000English text（8000English text×8English text）；English text、English text。',
    'English text', 'English text,N,English text,English text,English text'),

  ('case_005', '(2025)English text01English text04421English text', 'English text', 'court_sh_no1', 'English text', 'English text', '2025-10-09',
    'English text：English text；English text：English text（English text）',
    'English text"English text"English text，English text，English text，English text。',
    'English text2020English text，English text18000English text。2025English text"English text"English text。English text《English text》English text。English text，English text。',
    'English text，English text。English text，English text，English text，English text。',
    'English text"English text"English text，English text，English text。',
    'English text、English text，English text（English text180000English text）；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text,English text'),

  ('case_006', '(2025)English text0115English text10210English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2025-06-28',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2021English text，English text20000English text，English text。English text2023-2024English text260English text，English text。',
    'English text，English text；English text，English text。English text。',
    'English text，English text；English text，English text。',
    'English text、English text43103English text；English text、English text22069English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_007', '(2025)English text0105English text15580English text', 'English text（English text）English text', 'court_bj_chaoyang', 'English text', 'English text', '2025-12-03',
    'English text：English text（English text）；English text：English text',
    'English text"English text"English text，English text，English text。',
    'English text2022English text，English text15000English text。2025English text，English text"English text"English text。English text。',
    'English text，English text；English text，English text。English text，English text，English text。',
    'English text、English text、English text，English text；English text，English text。',
    'English text、English text；English text、English text，English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_008', '(2025)English text0112English text06012English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-05-19',
    'English text：English text（English text）；English text：English text',
    'English text，English text，English text。',
    'English text2023English text，English text7500English text。English text2025English text1English text。English text。',
    'English text，English text，English text，English text。English text。',
    'English text，English text，English text。',
    'English text、English text22500English text；English text、English text15000English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_009', '(2025)English text0115English text11876English text', 'English text', 'court_sh_pudong', 'English text', 'noncompete restriction', '2025-10-27',
    'English text：English text（English text）；English text：English text',
    'English text，English text，English text。',
    'English text2021English text，English text30000English text，English text。English text，English text。',
    'English text；English text，English text，English text。',
    'English text，English text。',
    'English text、English text108000English text（30000English text×30%×12English text）；English text、English text。',
    'English text', 'noncompete restriction,English text,English text,English text,English text'),

  ('case_010', '(2025)English text0112English text05533English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-04-11',
    'English text：English text（English text）；English text：English text',
    'English text"English text"English text，English text，English text。',
    'English text2025English text1English text，English text。English text"English text"English text，English text，English text。',
    'English text，English text，English text。English text，English text。',
    'English text，English text。',
    'English text、English text6000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_011', '(2024)English text0115English text21344English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2024-12-20',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2023English text6English text，English text14000English text，English text2024English text6English text。English text。',
    'English text，English text，English text。',
    'English text，English text。',
    'English text、English text154000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_012', '(2025)English text0112English text06890English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-06-05',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2018English text，English text16000English text，English text。2025English text，English text。English text。',
    'English text，English text，English text、English text。',
    'English text，English text、English text，English text。',
    'English text、English text28000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_013', '(2025)English text0115English text10044English text', 'English text（English text）', 'court_sh_pudong', 'English text', 'English text', '2025-09-08',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2022English text，English text13000English text。English text，English text。',
    'English text。English text，English text。',
    'English text，English text。',
    'English text、English text31494English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_014', '(2025)English text0105English text12233English text', 'English text（"English text"）English text', 'court_bj_chaoyang', 'English text', 'English text', '2025-08-14',
    'English text：English text（English text）；English text：English text',
    'English text"English text"English text，English text，English text。',
    'English text2020English text，English text28000English text。2025English text。English text，English text。',
    '"English text"English text。English text，English text，English text。',
    'English text"English text"English text，English text，English text，English text。',
    'English text、English text280000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_015', '(2025)English text0112English text07120English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-07-02',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2020English text，English text6500English text。2024English text，English text。',
    'English text，English text，English text。',
    'English text，English text，English text。',
    'English text、English text39000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_016', '(2025)English text0115English text09015English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2025-05-26',
    'English text：English text（English text）；English text：English text',
    'English text"English text"English text，English text。',
    'English text2016English text，English text32000English text。2025English text"English text"English text，English text。',
    'English text，English text，English text。English text，English text。',
    'English text"English text"English text，English text，English text。',
    'English text、English text608000English text（32000English text×9.5English text×2）；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_017', '(2024)English text0115English text19922English text', 'English text（English text）', 'court_sh_pudong', 'English text', 'English text', '2024-11-30',
    'English text：English text（English text）；English text：English text',
    'English text，English text。',
    'English text2015English text，English text，English text22000English text。2024English text，English text，English text。',
    'English text，English text，English text。English text，English text。',
    'English text，English text，English text。',
    'English text、English text418000English text；English text、English text。',
    'English text', 'English text,English text,English text,English text,English text'),

  ('case_018', '(2025)English text01English text05012English text', 'English text', 'court_sh_no1', 'English text', 'noncompete restriction', '2025-11-05',
    'English text：English text；English text：English text（English text）',
    'English text，English text。',
    'English text2019English text，English text180English text。English text。English text。English text。',
    'English text，English text。English text、English text，English text。',
    'English text，English text。',
    'English text、English text，English text（English text360000English text）；English text、English text。',
    'English text', 'noncompete restriction,English text,English text,English text,English text');

-- ── Citations (case → statute article / case) ──────────────────────
INSERT INTO citations (citation_id, case_id, target_type, target_id, label) VALUES
  ('cite-qpkqfr52v2kzx', 'case_001', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-tvuazzb3butgx', 'case_001', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-7cowyzm7cexex', 'case_001', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-jvqqwjmjzxajx', 'case_002', 'article', 'art_ll_044',  'English text'),
  ('cite-xegxqydzzxjkx', 'case_003', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-vcmpu3ahlk2ox', 'case_003', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-ptdulwgmad47x', 'case_004', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-c2w22qykmlghx', 'case_004', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-ckpmi2w4ch3dx', 'case_004', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-kpucc75lns5sx', 'case_005', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-2vf6y7bkronex', 'case_005', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-6wxuxtzcf6gjx', 'case_006', 'article', 'art_ll_044',  'English text'),
  ('cite-go3yc6f3kqzrx', 'case_007', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-k27kg2ttcwhdx', 'case_007', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-paekqgdyrw45x', 'case_008', 'article', 'art_ll_050',  'English text'),
  ('cite-zrgim2pmjwulx', 'case_008', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-mfj26mpvrezvx', 'case_010', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-mhivugf2ukwsx', 'case_011', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-2t4lwojxsudlx', 'case_012', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-ya75mxthppazx', 'case_013', 'article', 'art_ll_036',  'English text'),
  ('cite-tk2n66grvp4qx', 'case_013', 'article', 'art_ll_044',  'English text'),
  ('cite-5goykghu4e2yx', 'case_014', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-uwuktrirpkcjx', 'case_014', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-gunbkirfo3nqx', 'case_016', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-ec76e5cbf5pgx', 'case_016', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-wipxyxx6cr2fx', 'case_017', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-zgtph42sro2dx', 'case_005', 'case',    'case_001',    'English text'),
  ('cite-a2xm7ah7vj7fx', 'case_014', 'case',    'case_001',    'English text'),
  ('cite-4itqtusweapjx', 'case_016', 'case',    'case_017',    'English text');

-- ── Task-specific saved-case library: usr_feng_yi ────────────────────
-- Evan Feng（Feng Yi） saved twoEnglish text cases for compensation and procedure cross-checking.
INSERT INTO saved_cases (saved_id, user_id, case_id, note, saved_at) VALUES
  ('saved_fy_001', 'usr_feng_yi', 'case_001',
    'English text，English text，English text。', '2026-05-12T09:15:00Z'),
  ('saved_fy_002', 'usr_feng_yi', 'case_016',
    'English text，English text。', '2026-05-14T20:40:00Z');

-- ══ Additional labor-dispute courts ══
INSERT INTO courts (court_id, name, level, region) VALUES
  ('court_sh_xuhui', 'English text', 'English text', 'English text'),
  ('court_sh_jingan', 'English text', 'English text', 'English text'),
  ('court_bj_haidian', 'English text', 'English text', 'English text'),
  ('arb_bj_chaoyang', 'English text', 'English text', 'English text');

-- ══ Additional published labor-dispute cases ══
INSERT INTO cases (case_id, case_number, title, court_id, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords) VALUES
  ('judg-2023-qi5pqsboo77kx', '(2023)English text0104English text5821English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2023-12-15', 'English text：English text（English text）；English text：English text', 'English text，English text；English text，English text。', 'English text，English text。English text，English text。English text。', 'English text。English text，English text；English text，English text。', 'English text，English text，English text。', 'English text，English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-sr7v2teijzc5x', '(2023)English text0106English text13466English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2023-11-22', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text；English text。', 'English text，English text。English text，English text。', 'English text，English text、English text。', 'English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-mvahzmlfnke2x', '(2023)English text0108English text907English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2023-10-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text，English text。', 'English text；English text。', 'English text，English text；English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-lbm5o6bc2o4rx', '(2023)English text21843English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2023-09-08', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text，English text。', 'English text，English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-d2lftw2odrbvx', '(2023)English text0115English text7612English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2023-08-15', 'English text：English text（English text）；English text：English text', 'English text，English text；English text。', 'English text，English text。English text，English text。', 'English text，English text；English text，English text，English text。', 'English text；English text。', 'English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-ygqrkdmlntx7x', '(2023)English text0112English text19035English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2023-07-22', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text。English text、English text，English text；English text。', 'English text，English text，English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text'),

  ('judg-2023-ntwdmm3aspchx', '(2023)English text0105English text4468English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2023-06-01', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-4odtu2pzarvbx', '(2023)English text0104English text15379English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2023-05-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English textIPEnglish text。English text，English text。', 'English text，English text。English text。', 'English text、English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-inb7z4fisprpx', '(2023)English text0106English text2861English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2023-04-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text、English text，English text。English text，English text。', 'English text；English text，English text，English text。', 'English text、English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-lyjjpifktzcwx', '(2023)English text0108English text11204English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2023-03-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-m7ee5d77xhxvx', '(2023)English text23917English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2023-02-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text，English text。', 'English text、English text。English text，English text。', 'English text，English text，English text。', 'English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2023-6zftlfsft6rlx', '(2023)English text0115English text6755English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2023-01-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text。English text，English text。', 'English text，English text；English text。', 'English text、English text，English text。', 'English text。', 'English text', 'English text,English text,English text'),

  ('judg-2022-dix3rihzbp7sx', '(2022)English text0112English text1472English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2022-12-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text。English text，English text。English text。', 'English text，English text。English text；English text，English text，English text。', 'English text，English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-oseihvvc3p44x', '(2022)English text0105English text20831English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2022-11-22', 'English text：English text（English text）；English text：English text', 'English text，English text；English text。', 'English text，English text。English text，English text。', 'English text；English text。English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text'),

  ('judg-2022-643ywgx2qfmyx', '(2022)English text0104English text9346English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2022-10-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text。English text，English text。English text。', 'English text。English text，English text。', 'English text，English text；English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-hrcgoj6gjsu7x', '(2022)English text0106English text17509English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2022-09-08', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text，English text。English text，English text。', 'English text，English text。English text，English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-qq5t5qdmbfocx', '(2022)English text0108English text3218English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2022-08-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text、English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text；English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-fgtqb5vwkwuvx', '(2022)English text12467English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2022-07-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-wfetri7bnwxvx', '(2022)English text0115English text22106English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2022-06-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text。English text，English text。', 'English text，English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-4khiq74u7sxox', '(2022)English text0112English text814English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2022-05-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text、English text。', 'English text，English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-b2gqwt66qsrrx', '(2022)English text0105English text16953English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2022-04-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-s3pdfrklkswgx', '(2022)English text0104English text5032English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2022-03-22', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-x6ulrgs634d4x', '(2022)English text0106English text18640English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2022-02-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text、English text。English text，English text。', 'English text，English text。English text，English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2022-omdrol2w3kd2x', '(2022)English text0108English text2715English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2022-01-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text，English text；English text。', 'English text。', 'English text，English text。', 'English text', 'English text,English text,English text'),

  ('judg-2021-dyvcgmtowdr7x', '(2021)English text14208English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2021-12-15', 'English text：English text（English text）；English text：English text', 'English text，English text；English text。', 'English text，English text。English text，English text，English text。', 'English text。English text；English text，English text。English text，English text。', 'English text，English text。', 'English text，English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-h3wdogd3znfix', '(2021)English text0115English text9981English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2021-11-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text。English text，English text。', 'English text，English text。English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-v5v2mqwgntvsx', '(2021)English text0112English text23164English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2021-10-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English textCEnglish text。English text，English text。English text。', 'English text，English text，English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-gmulivxyhefdx', '(2021)English text0105English text547English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2021-09-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-46tcmqhdhgh2x', '(2021)English text0104English text11736English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2021-08-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text；English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-o6xlkfngjrmax', '(2021)English text0106English text20495English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2021-07-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-bcljev4ziedgx', '(2021)English text0108English text3874English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2021-06-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text，English text。English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text、English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-qhzvqnsxryopx', '(2021)English text15902English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2021-05-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text。', 'English text，English text；English text，English text。', 'English text、English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-gnc4vzjws5spx', '(2021)English text0115English text7261English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2021-04-15', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text、English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-273xuwwjkgq5x', '(2021)English text0112English text19438English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2021-03-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text，English text。English text。', 'English text。English text，English text。', 'English text，English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-f2qoukpkic5ux', '(2021)English text0105English text2560English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2021-02-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2021-e3p5lzh34oi6x', '(2021)English text0104English text13179English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2021-01-08', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text、English text。English text，English text。', 'English text；English text，English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-7h3immu5djppx', '(2020)English text0106English text8826English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2020-12-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。English text。', 'English text，English text。English text；English text，English text。', 'English text，English text，English text。', 'English text，English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-j5d4gau77f4gx', '(2020)English text0108English text21607English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2020-11-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text、English text，English text。English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-hhoffravhovpx', '(2020)English text6134English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2020-10-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text；English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-6sz7wuahx366x', '(2020)English text0115English text17350English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2020-09-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text，English text。', 'English text；English text，English text。English text。', 'English text，English text，English text。', 'English text、English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-cen2yzmj5viwx', '(2020)English text0112English text1049English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2020-08-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text。English text，English text，English text。', 'English text，English text。English text，English text；English text，English text。', 'English text，English text、English text。', 'English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-dabebivv3fj3x', '(2020)English text0105English text14983English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2020-07-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-yzmkrq2ne5y5x', '(2020)English text0104English text4685English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2020-06-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text，English text。English text。', 'English text，English text。English text，English text。', 'English text，English text，English text。', 'English text、English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-f7ditgdozmywx', '(2020)English text0106English text22574English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2020-05-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text、English text，English text，English text。', 'English text，English text，English text。English text。', 'English text、English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-qtkbvwznwr5jx', '(2020)English text0108English text7903English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2020-04-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text。English text，English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-gpyrcacxlzhwx', '(2020)English text18126English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2020-03-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text、English text，English text。English text。', 'English text。English text。', 'English text，English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-7qb2mxpjhavwx', '(2020)English text0115English text3375English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2020-02-01', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text。English text，English text，English text；English text。', 'English text。English text，English text。', 'English text，English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2020-ekkerdrjhg3ox', '(2020)English text0112English text12642English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2020-01-08', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text、English text、English text。English text，English text。', 'English text，English text。English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-bzvkaxray6c4x', '(2019)English text0105English text9608English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2019-12-15', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text，English text。', 'English text、English text。English text，English text。English text，English text。', 'English text，English text。', 'English text、English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-yz2s27m67gb2x', '(2019)English text0104English text21357English text', 'English text', 'court_sh_xuhui', 'English text', 'English text', '2019-11-22', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text。', 'English text，English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-2xm44tmjmkfvx', '(2019)English text0106English text5194English text', 'English text', 'court_sh_jingan', 'English text', 'English text', '2019-10-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text；English text。', 'English text，English text。English text，English text。', 'English text，English text；English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-4wwnjlxavcqjx', '(2019)English text0108English text16580English text', 'English text', 'court_bj_haidian', 'English text', 'English text', '2019-09-08', 'English text：English text（English text）；English text：English text', 'English text，English text；English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text、English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-bovcbe27u7asx', '(2019)English text2421English text', 'English text', 'arb_bj_chaoyang', 'English text', 'English text', '2019-08-15', 'English text：English text（English text）；English text：English text', 'English text，English text，English text。', 'English text，English text。English text，English text，English text。', 'English text、English text，English text，English text。English text。', 'English text，English text，English text。', 'English text；English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-sowive7ncnqnx', '(2019)English text0115English text13895English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2019-07-22', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text。', 'English text', 'English text,English text,English text,English text'),

  ('judg-2019-cr6v2737cglqx', '(2019)English text0112English text8467English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2019-06-01', 'English text：English text（English text）；English text：English text', 'English text，English text。', 'English text，English text，English text。English text，English text。', 'English text，English text。English text，English text。', 'English text，English text。', 'English text，English text。', 'English text', 'English text,English text,English text,English text');

-- ══ Article citations for additional cases ══
INSERT INTO citations (citation_id, case_id, target_type, target_id, label) VALUES
  ('cite-fsxvohagnnlgx', 'judg-2023-qi5pqsboo77kx', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-7zyhqc74qzeox', 'judg-2023-qi5pqsboo77kx', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-awkk64onfkxrx', 'judg-2023-sr7v2teijzc5x', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-kn3zlq5v62qzx', 'judg-2023-mvahzmlfnke2x', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-yka75khwqiisx', 'judg-2023-mvahzmlfnke2x', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-pbkqxbreyd3zx', 'judg-2023-lbm5o6bc2o4rx', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-ksitzqyfvzqzx', 'judg-2023-d2lftw2odrbvx', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-kwpdszcnccqhx', 'judg-2023-d2lftw2odrbvx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-ldrksoulcwf4x', 'judg-2023-ygqrkdmlntx7x', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-ytbnet2agxlux', 'judg-2023-ntwdmm3aspchx', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-nfzwwytdzdf4x', 'judg-2023-ntwdmm3aspchx', 'article', 'art_ll_050', 'English text'),
  ('cite-l5j5zk2kaqeox', 'judg-2023-4odtu2pzarvbx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-zlmsk37pvn73x', 'judg-2023-inb7z4fisprpx', 'article', 'art_ll_044', 'English text'),
  ('cite-5ls7jkj6cynqx', 'judg-2023-inb7z4fisprpx', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-vuk7oknh6wz4x', 'judg-2023-lyjjpifktzcwx', 'article', 'art_ll_050', 'English text'),
  ('cite-ebugeewh57ibx', 'judg-2023-m7ee5d77xhxvx', 'article', 'art_ll_036', 'English text'),
  ('cite-3ko7ycrwk7irx', 'judg-2023-m7ee5d77xhxvx', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-u2wvce3nfqxgx', 'judg-2023-6zftlfsft6rlx', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-oiqkrbir4jirx', 'judg-2022-dix3rihzbp7sx', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-dexgznvgempxx', 'judg-2022-dix3rihzbp7sx', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-ub5kdvsa6oc4x', 'judg-2022-oseihvvc3p44x', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-f6zmfgboly7sx', 'judg-2022-643ywgx2qfmyx', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-cuqs5uxfdgc4x', 'judg-2022-643ywgx2qfmyx', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-6xrhp7vkdkfnx', 'judg-2022-hrcgoj6gjsu7x', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-j2465uzns5yyx', 'judg-2022-qq5t5qdmbfocx', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-ubgj52y6qp6ix', 'judg-2022-qq5t5qdmbfocx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-zjuvsxihpn72x', 'judg-2022-fgtqb5vwkwuvx', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-say7g4yy6p6ex', 'judg-2022-wfetri7bnwxvx', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-paz4djndlfzcx', 'judg-2022-wfetri7bnwxvx', 'article', 'art_ll_050', 'English text'),
  ('cite-zcwnfvqohroxx', 'judg-2022-4khiq74u7sxox', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-j6cxsekip6qax', 'judg-2022-b2gqwt66qsrrx', 'article', 'art_ll_044', 'English text'),
  ('cite-u7z5yx7f3jlix', 'judg-2022-b2gqwt66qsrrx', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-ocmzugonoo3fx', 'judg-2022-s3pdfrklkswgx', 'article', 'art_ll_050', 'English text'),
  ('cite-3aqrr66fuajqx', 'judg-2022-x6ulrgs634d4x', 'article', 'art_ll_036', 'English text'),
  ('cite-3lbaeu6rbwv5x', 'judg-2022-x6ulrgs634d4x', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-mqul34cp2i5fx', 'judg-2022-omdrol2w3kd2x', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-g3ql67v2cpqmx', 'judg-2021-dyvcgmtowdr7x', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-sw7vxx43usw7x', 'judg-2021-dyvcgmtowdr7x', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-dyjjkthxjk6px', 'judg-2021-h3wdogd3znfix', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-eiomt4klsrn4x', 'judg-2021-v5v2mqwgntvsx', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-3hn4jzoyjiywx', 'judg-2021-v5v2mqwgntvsx', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-pzffax3e4dfdx', 'judg-2021-gmulivxyhefdx', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-3eudzxuef7vrx', 'judg-2021-46tcmqhdhgh2x', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-moed2l2z77gfx', 'judg-2021-46tcmqhdhgh2x', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-ioycrkhtjogxx', 'judg-2021-o6xlkfngjrmax', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-e46jqrbpkohmx', 'judg-2021-bcljev4ziedgx', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-qmlblx5a45yrx', 'judg-2021-bcljev4ziedgx', 'article', 'art_ll_050', 'English text'),
  ('cite-6ctmtlrowiujx', 'judg-2021-qhzvqnsxryopx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-oznhbh7cbtyox', 'judg-2021-gnc4vzjws5spx', 'article', 'art_ll_044', 'English text'),
  ('cite-ac7h76fjl5s2x', 'judg-2021-gnc4vzjws5spx', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-ywmbrbc62nikx', 'judg-2021-273xuwwjkgq5x', 'article', 'art_ll_050', 'English text'),
  ('cite-6vf32rzpffavx', 'judg-2021-f2qoukpkic5ux', 'article', 'art_ll_036', 'English text'),
  ('cite-rgfiqiq3bezgx', 'judg-2021-f2qoukpkic5ux', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-67xnxrghxtixx', 'judg-2021-e3p5lzh34oi6x', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-f2pmkkxmnwj6x', 'judg-2020-7h3immu5djppx', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-gbq5qc3bt2fwx', 'judg-2020-7h3immu5djppx', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-scu3vuq7xovtx', 'judg-2020-j5d4gau77f4gx', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-on4vlf65dp3ox', 'judg-2020-hhoffravhovpx', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-mshhwj2me3gnx', 'judg-2020-hhoffravhovpx', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-ym76mleglq5lx', 'judg-2020-6sz7wuahx366x', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-qrdntp4txp6nx', 'judg-2020-cen2yzmj5viwx', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-itu464jm2zyjx', 'judg-2020-cen2yzmj5viwx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-w3fmalj7hsuvx', 'judg-2020-dabebivv3fj3x', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-yx4l52abpbfkx', 'judg-2020-yzmkrq2ne5y5x', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-e5bqhv5pxunvx', 'judg-2020-yzmkrq2ne5y5x', 'article', 'art_ll_050', 'English text'),
  ('cite-u24vv5bpgfvvx', 'judg-2020-f7ditgdozmywx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-notqxsvgbb7fx', 'judg-2020-qtkbvwznwr5jx', 'article', 'art_ll_044', 'English text'),
  ('cite-gsu24v3fee5sx', 'judg-2020-qtkbvwznwr5jx', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-4gkzfil3syhtx', 'judg-2020-gpyrcacxlzhwx', 'article', 'art_ll_050', 'English text'),
  ('cite-wzwohufa6ngtx', 'judg-2020-7qb2mxpjhavwx', 'article', 'art_ll_036', 'English text'),
  ('cite-fjme62r6ytnvx', 'judg-2020-7qb2mxpjhavwx', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-mrvui75pnmxrx', 'judg-2020-ekkerdrjhg3ox', 'article', 'law-lcl-010-6sqxqt7ax', 'English text'),
  ('cite-rd5r3tgrunuzx', 'judg-2019-bzvkaxray6c4x', 'article', 'law-lcl-040-n3s2ei6mx', 'English text'),
  ('cite-svcipzo2smunx', 'judg-2019-bzvkaxray6c4x', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-qs2r6dxh3glnx', 'judg-2019-yz2s27m67gb2x', 'article', 'law-lcl-046-jtbn7kdsx', 'English text'),
  ('cite-24yyp6q3fxmwx', 'judg-2019-2xm44tmjmkfvx', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-pstwxtgf7hyrx', 'judg-2019-2xm44tmjmkfvx', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-c4psh44z4t6nx', 'judg-2019-4wwnjlxavcqjx', 'article', 'law-lcl-048-sib27mx5x', 'English text'),
  ('cite-7uei3qxtzmjzx', 'judg-2019-bovcbe27u7asx', 'article', 'law-lcl-082-bkp4xk6vx', 'English text'),
  ('cite-6nrncdosq74mx', 'judg-2019-bovcbe27u7asx', 'article', 'law-lcl-039-so63r3rex', 'English text'),
  ('cite-cu2ggbgjx7vfx', 'judg-2019-sowive7ncnqnx', 'article', 'law-lcl-087-ugz2y7vjx', 'English text'),
  ('cite-w6lzxh3lowfyx', 'judg-2019-cr6v2737cglqx', 'article', 'law-lcl-038-dcs4qbtqx', 'English text'),
  ('cite-ipvasymx34dex', 'judg-2019-cr6v2737cglqx', 'article', 'art_ll_050', 'English text');

-- ── Counters (seed so newly-issued IDs don't collide with seed IDs) ──


-- ── Task-specific authority corpus: compensation basis + recruitment privacy ──
-- The statutes/articles below are simplified public-law text. The four cases are
-- original synthetic benchmark materials, not representations of real judgments.
INSERT INTO statutes (statute_id, name, short_name, issuer, effective_date, status, summary) VALUES
  ('stat_lcl_reg', 'English text', 'English text', 'English text', '2008-09-18', 'English text',
    'English text；English text，English text、English text。'),
  ('stat_pipl', 'English text', 'English text', 'English text', '2021-11-01', 'English text',
    'English text、English text、English text、English text、English text。');

INSERT INTO statute_articles (article_id, statute_id, article_no, seq, heading, text) VALUES
  ('law-lcl-008-rzx7666nx', 'stat_lcl', 'English text', 8, 'English text',
    'English text，English text、English text、English text、English text、English text、English text，English text；English text，English text。'),
  ('art_lcl_reg_027', 'stat_lcl_reg', 'English text', 27, 'English text',
    'English text，English text，English text、English text。English text，English text；English text，English text。'),
  ('art_pipl_006', 'stat_pipl', 'English text', 6, 'English text',
    'English text、English text，English text，English text。English text，English text，English text。'),
  ('art_pipl_013', 'stat_pipl', 'English text', 13, 'English text',
    'English text、English text、English text、English text，English text；English text，English text。'),
  ('art_pipl_014', 'stat_pipl', 'English text', 14, 'English text、English text、English text',
    'English text，English text、English text。English text、English text，English text；English text、English text，English text。'),
  ('art_pipl_028', 'stat_pipl', 'English text', 28, 'English text',
    'English text，English text、English text，English text、English text、English text、English text、English text、English text。English text，English text，English text。'),
  ('art_pipl_029', 'stat_pipl', 'English text', 29, 'English text',
    'English text；English text、English text，English text。');

INSERT INTO cases (case_id, case_number, title, court_id, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords) VALUES
  ('judg-2025-2nx6fcq7lw3ax', '(2025)English text01English text9123English text', 'English text', 'court_sh_no1', 'English text', 'English text', '2025-11-20',
    'English text；English text',
    'English text，English text。English text。',
    'English text，English text。English text。',
    'English text。English text、English text，English text。',
    'English text；English text，English text。',
    'English text。', 'English text',
    'English text,English text,English text,English text,English text,English text'),
  ('judg-2025-6jpk3v7m2q9dx', '(2025)English text0115English text41880English text', 'English text', 'court_sh_pudong', 'English text', 'English text', '2025-10-16',
    'English text；English text',
    'English text，English text、English text，English text。',
    'English text、English text。English text、English text。',
    'English text。English text；English text、English text，English text。',
    'English text；English text。',
    'English text、English text。', 'English text',
    'English text,English text,English text,English text,English text,English text'),
  ('judg-2025-y4t8n2c6pw5rx', '(2025)English text0112English text33771English text', 'English text', 'court_sh_minhang', 'English text', 'English text', '2025-08-28',
    'English text；English text',
    'English text，English text，English text。',
    'English text、English text。English text，English text。',
    'English text、English text，English text。English text，English text。',
    'English text；English text。',
    'English text，English text。', 'English text',
    'English text,English text,English text,English text,English text,English text'),
  ('judg-2025-k9m3q7v2xd6lx', '(2025)English text0105English text28664English text', 'English text', 'court_bj_chaoyang', 'English text', 'English text', '2025-06-12',
    'English text；English text',
    'English text、English text，English text。',
    'English text，English text。English text、English text。',
    'English text、English text。English text、English text，English text。',
    'English text。',
    'English text。', 'English text',
    'English text,English text,English text,English text,English text,English text');

INSERT INTO citations (citation_id, case_id, target_type, target_id, label) VALUES
  ('cite-2x6m9q4v7k3dx', 'judg-2025-2nx6fcq7lw3ax', 'article', 'law-lcl-047-jfewut5kx', 'English text'),
  ('cite-7n3q5v2m8k4rx', 'judg-2025-2nx6fcq7lw3ax', 'article', 'art_lcl_reg_027', 'English text'),
  ('cite-4m7q2x9k6v3dx', 'judg-2025-6jpk3v7m2q9dx', 'article', 'art_pipl_006', 'English text'),
  ('cite-8v3n6q2m5k7rx', 'judg-2025-6jpk3v7m2q9dx', 'article', 'art_pipl_028', 'English text'),
  ('cite-5k9x3m7q2v6dx', 'judg-2025-6jpk3v7m2q9dx', 'article', 'art_pipl_029', 'English text'),
  ('cite-3q7v5n2x8m4rx', 'judg-2025-y4t8n2c6pw5rx', 'article', 'law-lcl-008-rzx7666nx', 'English text'),
  ('cite-9m2k6v4q7x3dx', 'judg-2025-y4t8n2c6pw5rx', 'article', 'art_pipl_013', 'English text'),
  ('cite-6x4q8m3v2k7rx', 'judg-2025-y4t8n2c6pw5rx', 'article', 'art_pipl_014', 'English text'),
  ('cite-2v8n5k9q3m6dx', 'judg-2025-y4t8n2c6pw5rx', 'article', 'art_pipl_028', 'English text'),
  ('cite-7q3x6m2k9v4rx', 'judg-2025-y4t8n2c6pw5rx', 'article', 'art_pipl_029', 'English text'),
  ('cite-4k8v2q7m5x3dx', 'judg-2025-k9m3q7v2xd6lx', 'article', 'art_pipl_006', 'English text'),
  ('cite-8m5x3v6q2k7rx', 'judg-2025-k9m3q7v2xd6lx', 'article', 'art_pipl_028', 'English text'),
  ('cite-3x7k9m4v6q2dx', 'judg-2025-k9m3q7v2xd6lx', 'article', 'art_pipl_029', 'English text');

INSERT INTO _counters (key, value) VALUES
  ('saved_seq', 2),
  ('citation_seq', 29);

COMMIT;
