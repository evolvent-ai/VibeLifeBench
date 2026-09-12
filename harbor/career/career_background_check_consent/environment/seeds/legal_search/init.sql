-- legal_search_mock career_background_check_consent — init.sql
-- translated textdisputetranslated textmaterialstranslated text：
--   • 6 courts/arbitrationtranslated text across Shanghai/translated text
--   • 4 statutes: Labor Contract Law + translated text + labor law + Personal Information Protection Law, with their key articles (statutetranslated text simplified, public-domain style)
--   • 77 translated textcasetranslated text，translated text、severance、translated texthealth informationtranslated textnoncompetetranslated textsubject
--   • citation links from cases → statute articles (and a few case→case references)
--   • Sang Wutranslated text 2 translated textrecord
-- translated textnametranslated text，casetranslated textmaterialstranslated text。
-- Reference date: 2026-05-20 (task-level only; the server has no clock).

BEGIN;

-- ── Courts / Arbitration Commission ─────────────────────────────────────────────
INSERT INTO courts (court_id, name, level, region) VALUES
  ('court_sh_pudong',   'Shanghaitranslated textPeople’s Court',       'translated text',   'Shanghaitranslated text'),
  ('court_sh_minhang',  'Shanghaitranslated textPeople’s Court',         'translated text',   'Shanghaitranslated text'),
  ('court_sh_no1',      'Shanghaitranslated textPeople’s Court',       'translated text',   'Shanghaitranslated text'),
  ('court_sh_high',     'Shanghaitranslated textseniorPeople’s Court',           'seniortranslated text',   'Shanghaitranslated text'),
  ('court_bj_chaoyang', 'translated textPeople’s Court',         'translated text',   'translated text'),
  ('arb_sh_pudong',     'Shanghaitranslated textdisputeArbitration Commission', 'Arbitration Commission', 'Shanghaitranslated text');

-- ── Statutes ───────────────────────────────────────────────────────
INSERT INTO statutes (statute_id, name, short_name, issuer, effective_date, status, summary) VALUES
  ('stat_lcl',  'translated textLabor Contract Law', 'Labor Contract Law', 'translated text', '2008-01-01', 'translated text',
    'translated text、translated text、translated text、translated text，translated text，translated textsalary、translated text、severancetranslated text。'),
  ('stat_ll',   'translated textlabor law', 'labor law', 'translated text', '1995-01-01', 'translated text',
    'translated text，translated textworktime、translated text、salary、translated textworktimetranslated textandtranslated textdisputetranslated text。');

-- ── Statute articles (statute) ─────────────────────────────────────────
-- Labor Contract Law key articles
INSERT INTO statute_articles (article_id, statute_id, article_no, seq, heading, text) VALUES
  ('law-lcl-010-ogk5vtnfx', 'stat_lcl', 'translated text',     10, 'translated text',
    'translated text，translated text。translated text，translated text，translated text。'),
  ('law-lcl-036-utedl76fx', 'stat_lcl', 'translated text', 36, 'translated text',
    'translated text，cantranslated text。'),
  ('law-lcl-038-yeazgq4ex', 'stat_lcl', 'translated text', 38, 'translated text',
    'translated textaccording totranslated textortranslated text、translated textpaymenttranslated text、translated text，translated textcantranslated text。'),
  ('law-lcl-039-ux5gjbrxx', 'stat_lcl', 'translated text', 39, 'translated text（translated text）',
    'translated text、translated text、translated text，translated textcantranslated text。'),
  ('law-lcl-040-blpnlbptx', 'stat_lcl', 'translated text',   40, 'translated text',
    'translated text，translated textnoticetranslated textortranslated textpaymenttranslated textmonthly wagestranslated text，cantranslated text：translated texthealthcaretranslated textcannottranslated textworktranslated text；cannottranslated textworktranslated textcannottranslated text；translated text。'),
  ('law-lcl-046-dvyxmanqx', 'stat_lcl', 'translated text', 46, 'severance',
    'translated text，translated textpaymentseverance：translated text；translated text；translated text、translated text；translated text。'),
  ('law-lcl-047-7nfprxbbx', 'stat_lcl', 'translated text', 47, 'severancecalculate',
    'severancetranslated textworktranslated textservice period，translated textpaymenttranslated textmonthly wagestranslated textpayment。translated text，translated textcalculate；translated text，translated textpaymenttranslated textmonthly wagestranslated textseverance。'),
  ('law-lcl-048-7qfuia53x', 'stat_lcl', 'translated text', 48, 'translated text',
    'translated textortranslated text，translated text，translated text；translated textdo nottranslated textortranslated textalreadycannottranslated text，translated textpaymenttranslated text。'),
  ('law-lcl-082-ysfbrkvxx', 'stat_lcl', 'translated text', 82, 'translated textsigntranslated textsalary',
    'translated text，translated textmonthlypaymenttranslated textsalary。'),
  ('law-lcl-087-a6lj7dyvx', 'stat_lcl', 'translated text', 87, 'translated text',
    'translated textortranslated text，translated textseverancetranslated textpaymenttranslated text。');

-- labor law key articles
INSERT INTO statute_articles (article_id, statute_id, article_no, seq, heading, text) VALUES
  ('art_ll_036', 'stat_ll', 'translated text', 36, 'translated text',
    'translated textworktimetranslated text、averagetranslated textweekworktimetranslated text。'),
  ('art_ll_041', 'stat_ll', 'translated text', 41, 'translated textworktimetranslated text',
    'translated textneed，translated textcantranslated textworktime，translated text；translated textreasontranslated text，monthlytranslated text。'),
  ('art_ll_044', 'stat_ll', 'translated text', 44, 'translated text',
    'translated textworktimetranslated text，paymenttranslated textsalarytranslated text；translated textworktranslated textcannottranslated text，paymenttranslated text；translated textworktranslated text，paymenttranslated text。'),
  ('art_ll_050', 'stat_ll', 'translated text', 50, 'salarypayment',
    'salarytranslated textpaymenttranslated text，translated textortranslated textsalary。');

-- ── Cases (anonymized judgments) ────────────────────────────────────
INSERT INTO cases (case_id, case_number, title, court_id, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords) VALUES
  ('case_001', '(2025)translated text0115translated text12001translated text', 'translated textcompanytranslated text', 'court_sh_pudong', 'translated textdispute', 'translated text', '2025-11-18',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated text"translated text"translated text，translated textbasis，translated text，translated textpaymenttranslated text。',
    'translated text2019translated text3translated textcompanytranslated text，monthly wages25000translated text。2025translated text6translated textcompanytranslated textnoticetranslated text，translated textnotice，translated textpaymenttranslated textnoticetranslated text。translated textclaimtranslated text，translated text2Npaymenttranslated text。',
    'translated textclaimbasistranslated text，translated text，translated textnoticetranslated textpaymenttranslated textmonthly wagestranslated text，translated text，translated text，translated text、translated textseverancetranslated textpaymenttranslated text。',
    'translated text"translated text"translated text，translated text，translated text，translated textpaymenttranslated text。',
    'translated text、translated textpaymenttranslated text325000translated text（25000translated text×6.5translated text×2）；translated text、translated text。',
    'translated text', 'translated text,translated text,2N,translated text,translated text'),

  ('case_002', '(2025)translated text0112translated text08842translated text', 'translated textcompanytranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2025-09-22',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'translated text，companytranslated textpaymenttranslated text，translated textbasistranslated textrecordtranslated text。',
    'translated text2022translated text，translated textmonthly salary9000translated text，translated text。translated textrecordtranslated text2024translated text52day，companytranslated textpaymenttranslated text。',
    'basislabor lawtranslated text，translated textworktranslated textcannottranslated text，translated textpaymenttranslated text。translated textpaymenttranslated text，translated textcannottranslated text。',
    'translated textcannottranslated text，translated textsalarytranslated textpaymenttranslated text；translated text，translated text。',
    'translated text、translated textpaymenttranslated text2024annualtranslated text43034translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,translated textsalary,translated text,translated text'),

  ('case_003', '(2025)translated text0115translated text09931translated text', 'translated textcompanytranslated textsigntranslated textsalarytranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textsigntranslated text', '2025-08-30',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated textsigntranslated text，translated textpaymenttranslated textsigntranslated textsalaryshortfall。',
    'translated text2024translated text9translated text1translated text，translated textsigntranslated text。translated textworktranslated text2025translated text5translated textdeparture，translated textmonthly wages12000translated text。translated textclaim2024translated text10translated text1translated textdeparturetranslated textsalary。',
    'basisLabor Contract Lawtranslated text、translated text，translated text，translated textmonthlypaymenttranslated textsalary。translated textsalarytranslated textarbitrationlimitation periodtranslated textclaimtranslated text，translated textlimitation period。',
    'translated text，translated textpaymenttranslated textsalary，translated text。',
    'translated text、translated textpaymenttranslated text2024translated text10translated text1translated text2025translated text5translated textsigntranslated textsalaryshortfalltranslated text96000translated text；translated text、translated text。',
    'translated text', 'translated textsigntranslated text,translated textsalary,translated text,arbitrationlimitation period,translated text'),

  ('case_004', '(2025)translated text0112translated text07765translated text', 'translated textcompanyseverancetranslated text', 'court_sh_minhang', 'translated textdispute', 'severance', '2025-07-15',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated text，translated textclaimseverance，translated text。',
    'translated text2017translated text，monthly wages8000translated text。translated text2023translated text。2025translated text3translated textnoticetranslated text，translated textclaimseverance。',
    'basisLabor Contract Lawtranslated text，translated text，translated textcantranslated text；basistranslated text、translated text，translated textpaymentseverance，workservice periodtranslated textcalculate。',
    'translated text，translated text，translated textbasistranslated textclaimseverance（N），translated text。',
    'translated text、translated textpaymenttranslated textseverancetranslated text64000translated text（8000translated text×8translated text）；translated text、translated text。',
    'translated text', 'severance,N,translated text,translated text,translated text'),

  ('case_005', '(2025)translated text01translated text04421translated text', 'translated textcompanytranslated text', 'court_sh_no1', 'translated textdispute', 'translated text', '2025-10-09',
    'translated text：translated textcompany；translated text：translated text（translated text）',
    'companytranslated text"translated text"translated text，translated text，translated text，translated text。',
    'translated text2020translated text，monthly wages18000translated text。2025translated textcompanytranslated text"translated text"translated text。companytranslated text《translated text》translated text。translated text，companytranslated text。',
    'basisLabor Contract Lawtranslated text，translated text。translated text，cannottranslated textbasis，translated text，translated textpaymenttranslated text。',
    'translated text"translated text"translated text，translated textbasistranslated text，translated textcannottranslated textbasis。',
    'translated text、translated text，translated text（translated textpaymenttranslated text180000translated text）；translated text、translated text。',
    'translated text', 'translated text,translated text,translated text,translated text,translated text,translated text'),

  ('case_006', '(2025)translated text0115translated text10210translated text', 'translated textcompanytranslated textsalarytranslated text', 'court_sh_pudong', 'translated textdispute', 'translated text', '2025-06-28',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'translated textworktranslated text，translated textpaymenttranslated textsalary。',
    'translated text2021translated text，monthly wages20000translated text，translated text。translated text2023-2024translated textpassedtranslated textrecordtranslated textworktranslated text260translated text，translated text。',
    'basislabor lawtranslated text，worktranslated textworktimetranslated textpaymenttranslated text；translated text，translated textsalarytranslated textpaymenttranslated textsalarytranslated text。translated textrecordtranslated text。',
    'translated textrecordtranslated text，translated textpaymenttranslated text；translated text，translated textpaymenttranslated textsalarytranslated text。',
    'translated text、translated textpaymenttranslated text43103translated text；translated text、translated textpaymenttranslated textsalarytranslated text22069translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,translated text,translated text,translated text'),

  ('case_007', '(2025)translated text0105translated text15580translated text', 'translated textcompanytranslated text（pregnancy）translated text', 'court_bj_chaoyang', 'translated textdispute', 'translated text', '2025-12-03',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated textpregnancytranslated text"translated textwork"translated text，translated text，translated text。',
    'translated text2022translated text，monthly wages15000translated text。2025translated textpregnancytranslated text，companytranslated text"translated textcannottranslated textwork"translated text。companytranslated textworkroletranslated text。',
    'basisLabor Contract Lawtranslated text，translated textcannottranslated textworktranslated textcannottranslated text；translated textpregnancytranslated text，translated text。translated text，translated text，translated text。',
    'translated textpregnancy、translated text、translated text，translated textbasiscannottranslated textworktranslated text；translated text，translated text。',
    'translated text、confirmtranslated text；translated text、translated text，translated textpaymenttranslated textsalary。',
    'translated text', 'translated text,pregnancy,translated text,translated text,translated textwork'),

  ('case_008', '(2025)translated text0112translated text06012translated text', 'weektranslated textlogisticscompanytranslated textsalarytranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2025-05-19',
    'translated text：weektranslated text（translated text）；translated text：translated textlogisticscompany',
    'companytranslated textsalary，translated textclaimpaymenttranslated textsalarytranslated textseverance，translated textsalarytranslated text。',
    'weektranslated text2023translated text，monthly wages7500translated text。translated text2025translated text1translated textpaymentsalary。weektranslated textclaimtranslated textsalarytranslated textseverance。',
    'basislabor lawtranslated textLabor Contract Lawtranslated text，translated textsalarytranslated text，translated text，translated textclaimseverance。translated text。',
    'translated text，translated textpayment，translated textclaimseverance。',
    'translated text、translated textpaymentweektranslated textsalarytranslated text22500translated text；translated text、translated textpaymentweektranslated textseverancetranslated text15000translated text。',
    'translated text', 'translated textsalary,translated text,translated text,severance,translated text'),

  ('case_009', '(2025)translated text0115translated text11876translated text', 'translated textcompanynoncompeteseverancetranslated text', 'court_sh_pudong', 'translated textdispute', 'noncompete', '2025-10-27',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'translated textnoncompetetranslated textcompanytranslated textpaymentseverance，translated textclaimseverancetranslated text，translated textpaymentnoncompeteseverance。',
    'translated text2021translated text，monthly wages30000translated text，departuretranslated textsigntranslated textnoncompetetranslated text。departuretranslated textnoncompetetranslated text，translated textpaymenttranslated textseverance。',
    'noncompetetranslated textpaymentseverance；translated textseverancetranslated text，translated textdeparturetranslated textaveragesalarytranslated textpayment，translated textsalarytranslated text。',
    'translated textnoncompetetranslated textseverancetranslated text，translated textclaimtranslated textdeparturetranslated textsalarytranslated textpaymentseverance。',
    'translated text、translated textpaymenttranslated textnoncompeteseverancetranslated text108000translated text（30000translated text×30%×12translated text）；translated text、translated text。',
    'translated text', 'noncompete,severancetranslated text,translated text,translated text,departure'),

  ('case_010', '(2025)translated text0112translated text05533translated text', 'translated textcompanytranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2025-04-11',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated text"translated text"translated text，translated textbasis，translated text。',
    'translated text2025translated text1translated text，translated text。translated textcompanytranslated text"translated text"translated text，translated text，translated textrecord。',
    'basisLabor Contract Lawtranslated text，translated text，translated textfirsttranslated text。translated textcannot，translated text。',
    'translated text，translated textfirsttranslated text。',
    'translated text、translated textpaymenttranslated text6000translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,translated text,translated text,translated text'),

  ('case_011', '(2024)translated text0115translated text21344translated text', 'translated textcompanytranslated textsigntranslated textsalarytranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textsigntranslated text', '2024-12-20',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated textsigntranslated text，translated textpaymenttranslated textsalaryshortfall。',
    'translated text2023translated text6translated text，monthly wages14000translated text，translated text2024translated text6translated textdeparturetranslated textsigntranslated text。translated textclaimtranslated textsigntranslated textsalary。',
    'basisLabor Contract Lawtranslated text，translated textsigntranslated textsalarytranslated textpaymenttranslated text，translated text。',
    'translated textsalarypaymenttranslated text，translated textcalculate。',
    'translated text、translated textpaymenttranslated textsigntranslated textsalaryshortfalltranslated text154000translated text；translated text、translated text。',
    'translated text', 'translated textsigntranslated text,translated textsalary,translated text,translated text,translated text'),

  ('case_012', '(2025)translated text0112translated text06890translated text', 'translated textcompanyseverancetranslated textcalculatebasistranslated text', 'court_sh_minhang', 'translated textdispute', 'severance', '2025-06-05',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'translated textseverancecalculatebasiswhethertranslated textdispute，translated textdeparturetranslated textaveragesalarytranslated text。',
    'translated text2018translated text，translated textmonthly salary16000translated text，translated textannualtranslated text。2025translated text，companytranslated textbase salarycalculateseverance。translated textclaimtranslated text。',
    'basisLabor Contract Lawtranslated text，severancemonthly wagestranslated textaveragesalary，translated text、translated text。',
    'severancetranslated textmonthly wagescalculatebasistranslated textaveragetranslated textsalary，translated text、translated text，translated textbase salary。',
    'translated text、translated textseverancetranslated textshortfalltranslated text28000translated text；translated text、translated text。',
    'translated text', 'severance,calculatebasis,averagesalary,translated text,translated text'),

  ('case_013', '(2025)translated text0115translated text10044translated text', 'translated textcompanytranslated text（translated text）', 'court_sh_pudong', 'translated textdispute', 'translated text', '2025-09-08',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companyclaimtranslated textcalculatetranslated text，translated text。',
    'translated text2022translated text，monthly wages13000translated text。companyclaimtranslated textcalculatetranslated textpaymenttranslated text，translated text。',
    'translated textcalculatetranslated textworktranslated text。translated text，translated textcalculatetranslated textpaymenttranslated text。',
    'translated textclaimtranslated textcalculatetranslated text，translated textcalculatetranslated textpaymenttranslated text。',
    'translated text、translated textpaymenttranslated text31494translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,translated text,translated text,translated text'),

  ('case_014', '(2025)translated text0105translated text12233translated text', 'translated textinternetcompanytranslated text（"translated text"）translated text', 'court_bj_chaoyang', 'translated textdispute', 'translated text', '2025-08-14',
    'translated text：translated text（translated text）；translated text：translated textinternetcompany',
    'companytranslated text"translated text"translated text，translated textcannottranslated textwork，translated text。',
    'translated text2020translated textengineer，monthly wages28000translated text。2025translated textcompanytranslated text。companytranslated textcannottranslated textwork，translated text。',
    '"translated text"translated text。translated textcannottranslated textwork，translated text，translated text。',
    'translated text"translated text"translated text，translated textcannottranslated textwork，translated text，translated textpaymenttranslated text。',
    'translated text、translated textpaymenttranslated text280000translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,cannottranslated textwork,translated text,engineer'),

  ('case_015', '(2025)translated text0112translated text07120translated text', 'translated textcompanytranslated textsalarytranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2025-07-02',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'translated textcompanytranslated textsalary，translated textsalarytranslated textsalary。',
    'translated text2020translated text，monthly wages6500translated text。2024translated textworktranslated text，translated textcompanytranslated textsalary。',
    'translated textneedtranslated textworkaccepttranslated text，translated textsalarytranslated text，translated textpayment。',
    'translated text，translated textsalarytranslated textpaymentsalary，translated text。',
    'translated text、translated textpaymenttranslated textsalarytranslated text39000translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,salary,translated textsalarytranslated text,translated text'),

  ('case_016', '(2025)translated text0115translated text09015translated text', 'translated textcompanytranslated text', 'court_sh_pudong', 'translated textdispute', 'translated text', '2025-05-26',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated text"translated text"translated text，translated text。',
    'translated text2016translated textseniorengineer，monthly wages32000translated text。2025translated textcompanytranslated text"translated text"translated text，translated textfirsttranslated textcontent。',
    'basisLabor Contract Lawtranslated text，translated text，translated textfirsttranslated text。translated text，translated text。',
    'translated text"translated text"translated text，translated textfirsttranslated text，translated text。',
    'translated text、translated textpaymenttranslated text608000translated text（32000translated text×9.5translated text×2）；translated text、translated text。',
    'translated text', 'translated text,translated text,translated text,translated text,seniorengineer'),

  ('case_017', '(2024)translated text0115translated text19922translated text', 'translated textcompanytranslated text（translated textfirsttranslated text）', 'court_sh_pudong', 'translated textdispute', 'translated text', '2024-11-30',
    'translated text：translated text（translated text）；translated text：translated textcompany',
    'companytranslated textfirsttranslated text，translated text。',
    'translated text2015translated textengineer，translated text，monthly wages22000translated text。2024translated textcompanytranslated text，translated textfirsttranslated text，translated textproposal。',
    'basisLabor Contract Lawtranslated text，translated textfirsttranslated text，translated text。translated text，translated text。',
    'translated textfirsttranslated text，translated text，translated text。',
    'translated text、translated textpaymenttranslated text418000translated text；translated text、translated text。',
    'translated text', 'translated text,translated text,translated textfirsttranslated text,translated text,translated text'),

  ('case_018', '(2025)translated text01translated text05012translated text', 'translated textcompanytranslated textnoncompetetranslated text', 'court_sh_no1', 'translated textdispute', 'noncompete', '2025-11-05',
    'translated text：translated textcompany；translated text：translated text（translated text）',
    'companyclaimtranslated textnoncompetetranslated textpaymenttranslated text，translated text。',
    'translated text2019translated textengineer，departuretranslated textnoncompetetranslated text180translated text。companyclaimtranslated textpaymenttranslated text。translated text。companytranslated text。',
    'noncompetetranslated textactualtranslated text，translated text。translated textseverancetranslated text、translated textactualtranslated text，translated text。',
    'noncompetetranslated textactualtranslated text，People’s Courtcantranslated text。',
    'translated text、translated text，translated text（translated textpaymentnoncompetetranslated text360000translated text）；translated text、translated text。',
    'translated text', 'noncompete,translated text,translated text,translated textengineer,actualtranslated text');

-- ── Citations (case → statute article / case) ──────────────────────
INSERT INTO citations (citation_id, case_id, target_type, target_id, label) VALUES
  ('cite-rx36zco66dsax', 'case_001', 'article', 'law-lcl-040-blpnlbptx', 'claimbasistranslated text'),
  ('cite-ia7iaijo5pfex', 'case_001', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-oi2dtu6mbyuqx', 'case_001', 'article', 'law-lcl-087-a6lj7dyvx', 'translated textbasis'),
  ('cite-vbqpuswtaco7x', 'case_002', 'article', 'art_ll_044',  'translated textbasis'),
  ('cite-kywfp2olurhwx', 'case_003', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-gcwswcmlodqrx', 'case_003', 'article', 'law-lcl-082-ysfbrkvxx', 'translated textsalarybasis'),
  ('cite-3bf3twa47cqbx', 'case_004', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-4gqtqpd6t7gsx', 'case_004', 'article', 'law-lcl-046-dvyxmanqx', 'severancetranslated text'),
  ('cite-mfl6br344r6jx', 'case_004', 'article', 'law-lcl-047-7nfprxbbx', 'severancecalculate'),
  ('cite-uiyudsehbgutx', 'case_005', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-ayypfysecdpsx', 'case_005', 'article', 'law-lcl-087-a6lj7dyvx', 'translated textbasis'),
  ('cite-huukvky2blxix', 'case_006', 'article', 'art_ll_044',  'translated textbasis'),
  ('cite-lr7zb6ymfivfx', 'case_007', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-u6m6zgo4arwmx', 'case_007', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-k5sjxrnmshucx', 'case_008', 'article', 'art_ll_050',  'salarypayment'),
  ('cite-i53fcr5empbfx', 'case_008', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-vislmykdda3xx', 'case_010', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-2anymhdxezmqx', 'case_011', 'article', 'law-lcl-082-ysfbrkvxx', 'translated textsalarybasis'),
  ('cite-b6knhh7ll5fhx', 'case_012', 'article', 'law-lcl-047-7nfprxbbx', 'severancecalculate'),
  ('cite-wrvjreh3ap3xx', 'case_013', 'article', 'art_ll_036',  'translated text'),
  ('cite-knlfogwij7wix', 'case_013', 'article', 'art_ll_044',  'translated textbasis'),
  ('cite-noklxmezv6qwx', 'case_014', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-cizkqqq7vnfsx', 'case_014', 'article', 'law-lcl-087-a6lj7dyvx', 'translated textbasis'),
  ('cite-25s6nfgp5kgxx', 'case_016', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-k3yy3yhgtihex', 'case_016', 'article', 'law-lcl-087-a6lj7dyvx', 'translated textbasis'),
  ('cite-2pme6r4trcukx', 'case_017', 'article', 'law-lcl-087-a6lj7dyvx', 'translated textbasis'),
  ('cite-bmba5m7q4viyx', 'case_005', 'case',    'case_001',    'translated text'),
  ('cite-nf5idwrulsnfx', 'case_014', 'case',    'case_001',    'translated text'),
  ('cite-ice2rvazjqigx', 'case_016', 'case',    'case_017',    'translated text');

-- ── Sang Wutranslated textcasetranslated textrecord ─────────────────────────────────────
-- translated textroletranslated textnoticebefore ，recordtranslated text。
INSERT INTO saved_cases (saved_id, user_id, case_id, note, saved_at) VALUES
  ('saved_sw_001', 'usr_sang_wu', 'case_001',
    '2025 translated textlabor lawtranslated text：translated textwhethertranslated textbasis，andnotice、translated textdo not。', '2026-05-12T09:15:00Z'),
  ('saved_sw_002', 'usr_sang_wu', 'case_016',
    '2025 translated textmaterials：translated textrolewhethertranslated text、whetherfirsttranslated textwhethertranslated text。', '2026-05-14T20:40:00Z');

-- ══ translated textdisputetranslated text ══
INSERT INTO courts (court_id, name, level, region) VALUES
  ('court_sh_xuhui', 'Shanghaitranslated textPeople’s Court', 'translated text', 'Shanghaitranslated text'),
  ('court_sh_jingan', 'Shanghaitranslated textPeople’s Court', 'translated text', 'Shanghaitranslated text'),
  ('court_bj_haidian', 'translated textPeople’s Court', 'translated text', 'translated text'),
  ('arb_bj_chaoyang', 'translated textdisputeArbitration Commission', 'Arbitration Commission', 'translated text');

-- ══ translated text ══
INSERT INTO cases (case_id, case_number, title, court_id, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords) VALUES
  ('judg-2023-q36mikmywxv4x', '(2023)translated text0104translated text5821translated text', 'translated textcompanyhealthcaretranslated textdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'healthcaretranslated text', '2023-12-15', 'translated text：translated text（translated textengineer）；translated text：translated textcompany', 'healthcaretranslated text，companytranslated text；translated text，disputetranslated textrolewhethertranslated text。', 'translated text，translated textrole。companytranslated textdaytranslated textcannottranslated textworktranslated text，translated textworktranslated textrecord。translated textroletranslated text。', 'healthcaretranslated textfirsttranslated textworktranslated textwork。companyincompletetranslated text，translated textLabor Contract Lawtranslated text；roletranslated text，translated text。', 'translated textcannottranslated textwork，translated text，translated text。', 'translated textnotice，translated text；companytranslated textsalarytranslated text。', 'translated text', 'healthcaretranslated text,translated text,translated text,translated text'),

  ('judg-2023-zzsljcxcreq2x', '(2023)translated text0106translated text13466translated text', 'translated texte-commercecompanytranslated textseverancedisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated textseverance', '2023-11-22', 'translated text：translated text（platformtranslated text）；translated text：translated texte-commercecompany', 'translated textagreetranslated text，translated textseverance，translated textmeetingtranslated text。', 'translated textmeetingtranslated textconfirmcompanytranslated text，translated text。signtranslated textsalarytranslated text，translated textseverance；translated textmeetingtranslated text。', 'translated text，Labor Contract Lawtranslated textpaymentseverance。translated text，translated text。', 'translated textcompany，translated text、specifictranslated textseverancetranslated text。', 'translated texte-commercecompanytranslated textpaymenttranslated textseverancetranslated text；translated text。', 'translated text', 'translated text,severance,translated text,translated text'),

  ('judg-2023-dylu2owo2qhlx', '(2023)translated text0108translated text907translated text', 'translated textcompanytranslated textcalculatedisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated textcalculate', '2023-10-01', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textdisputetranslated textwhethertranslated textwage basis。', 'translated text，salarytranslated textquarterlytranslated text。companytranslated text，translated textseverance，translated textcalculatetranslated textactualtranslated text。', 'translated textseverancetranslated textpaymenttranslated text；translated textwage basistranslated textsalarytranslated textworkservice periodtranslated text。', 'quarterlytranslated textdirectlyrelevant，translated textcalculate；companytranslated textbasis，translated textwage basis。', 'translated textcompanypaymenttranslated textshortfalltranslated text。', 'translated text', 'translated text,translated text,translated textwage basis,translated text'),

  ('judg-2023-puzo4eop2tq2x', '(2023)translated text21843translated text', 'translated textcompanytranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated text', '2023-09-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textrole，translated text。', 'translated textsecuritytranslated text，translated text。companytranslated text，translated textoutsourced roletranslated textwork。', 'translated textsecuritytranslated text，translated textbasis。translated textroletranslated text，translated textcantranslated text，translated text。', 'companytranslated textsecuritytranslated text，translated textroletranslated text，translated text。', 'translated textcompanytranslated text，translated textsalary。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2023-hmr46qifodqbx', '(2023)translated text0115translated text7612translated text', 'translated textlogisticscompanytranslated textsigntranslated textdisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textsigntranslated text', '2023-08-15', 'translated text：translated text（translated text）；translated text：translated textlogisticscompany', 'translated textsigntranslated text，translated text；translated textsalarytranslated textdo nottranslated text。', 'translated textpassedtranslated textpayroll-account transactionstranslated text，companytranslated text。translated textsystemtranslated text，translated texttransactiontranslated textsigntranslated text。', 'translated text，translated textsalarytranslated text；translated text，translated texttransactiontranslated text，translated text。', 'translated textsigntranslated text；companytranslated text。', 'translated textlogisticscompanypaymenttranslated textsigntranslated textsalaryshortfall；translated text。', 'translated text', 'translated textsigntranslated text,translated textsalary,translated text,translated text'),

  ('judg-2023-zwgcbdluhq62x', '(2023)translated text0112translated text19035translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2023-07-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textsystemtranslated text，companytranslated textpaymenttranslated text。', 'translated textnoticetranslated textdaytranslated textsystem。translated text、translated text，translated text；companytranslated text。', 'translated text，companytranslated textbasis，translated text，translated textLabor Contract Lawtranslated textpaymenttranslated text。', 'translated text，translated textsystemtranslated textcannottranslated text。', 'translated textcompanypaymenttranslated text。', 'translated text', 'translated textwork,translated text,translated text'),

  ('judg-2023-5eimaw52kscwx', '(2023)translated text0105translated text4468translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'translated text', '2023-06-01', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textsalary，translated textdeparture，translated textweektranslated text。', 'translated text，salarytranslated textshortfalltranslated text。translated textsendtranslated textpaymentnotice，companyreplytranslated text。', 'salarytranslated textpayment，labor lawtranslated text。translated text。', 'translated textcannottranslated textsalarypaymenttranslated text，translated textnoticetranslated text。', 'translated textcompanytranslated textsalarytranslated text，translated textpaymenttranslated textseverance。', 'translated text', 'translated textsalary,salarypayment,translated text,translated text'),

  ('judg-2023-enjavsfusi6px', '(2023)translated text0104translated text15379translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'translated text', '2023-05-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textsigntranslated text，translated textbasistranslated text。', 'translated textsigntranslated text，systemIPtranslated text。translated text，translated text。', 'translated textrecordtranslated text，translated text。translated textbasis。', 'translated text、translated textsigntranslated text，translated text。', 'translated text。', 'translated text', 'translated textsigntranslated text,translated text,translated text,translated text'),

  ('judg-2023-hervlahfsd2fx', '(2023)translated text0106translated text2861translated text', 'translated textcompanytranslated textsigntranslated textdisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated textsigntranslated text', '2023-04-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated text，translated text。', 'translated text、payroll-account transactionstranslated textsystemtranslated textrecordtranslated text，translated textdaytranslated text。companytranslated textpaymenttranslated text，translated textsigntranslated text。', 'translated text；translated textworktranslated text，translated textlabor lawtranslated textpaymenttranslated text，translated textcannottranslated text。', 'translated text、translated textsigntranslated text，companytranslated text。', 'translated textcompanypaymenttranslated textsigntranslated text。', 'translated text', 'translated text,translated text,translated text,systemtranslated text'),

  ('judg-2023-ek263n22aslxx', '(2023)translated text0108translated text11204translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated text', '2023-03-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textdeparturetranslated textsalary，companytranslated text。', 'translated textalltranslated text，departuretranslated textconfirmtranslated textsalarytranslated text。companytranslated text，translated textpayment。', 'salarypaymenttranslated text。labor lawtranslated textpayment，departuretranslated text。', 'translated textamountalreadytranslated textconfirm，companytranslated textriskcannottranslated text。', 'translated textcompanypaymenttranslated textsalarytranslated textconfirmtranslated text。', 'translated text', 'translated textsalary,salarypayment,departuretranslated text,translated text'),

  ('judg-2023-etr6yfiad44ax', '(2023)translated text23917translated text', 'translated textcompanytranslated textseverancedisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated textseverance', '2023-02-01', 'translated text：translated text（platformengineer）；translated text：translated textcompany', 'platformtranslated text，engineertranslated textnewtranslated textcompanytranslated text。', 'translated text，translated textweektranslated textday。translated text，companytranslated text，translated textpaymentseverance。', 'labor lawtranslated text、averagetranslated textweektranslated text。companytranslated text，translated textseverancetranslated text。', 'translated text，translated textcompany，severancetranslated textcannottranslated textsigntranslated text。', 'translated textcompanypaymenttranslated textseverancetranslated text；translated textdisputetranslated text。', 'translated text', 'translated text,translated textweektranslated text,translated text,severance'),

  ('judg-2023-2yzgin2idkymx', '(2023)translated text0115translated text6755translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated text', '2023-01-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textnoticetranslated textsalaryconfirm，translated textsigntranslated text。', 'translated textcompanytranslated textworktranslated text。translated textfirsttranslated text，translated textsigntranslated text。', 'translated textalreadytranslated text，translated textLabor Contract Lawtranslated text；translated textcannottranslated textsign。', 'translated text、translated textpayroll-account transactionstranslated textactualtranslated text，companytranslated text。', 'translated textcompanytranslated textsigntranslated text。', 'translated text', 'translated text,translated text,actualtranslated text'),

  ('judg-2022-xec3xxwtpqnix', '(2022)translated text0112translated text1472translated text', 'translated textcompanycannottranslated textworktranslated textdisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'cannottranslated textworktranslated text', '2022-12-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated text，translated text。', 'translated text。translated text，translated textdaytranslated textdirectlytranslated textcannottranslated textnotice。translated textrecordtranslated textroletranslated text。', 'translated textcannottranslated textworktranslated text，needtranslated textortranslated textroletranslated textcannottranslated text。translated textLabor Contract Lawtranslated text；translated text，translated textcannot，translated text。', 'companytranslated text，translated textfirsttranslated text，cannottranslated text。', 'translated textcompanytranslated text，translated textsalarytranslated textmake updisputetranslated text。', 'translated text', 'cannottranslated text,translated text,translated text,translated text'),

  ('judg-2022-addrebp3kyowx', '(2022)translated text0105translated text20831translated text', 'translated textcompanytranslated textseverancedisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'translated textseverance', '2022-11-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textsigntranslated text；translated textseverance。', 'translated textsigntranslated text，base salarytranslated text。translated textsign，companytranslated textdeparture。', 'translated textortranslated text；translated text。translated textLabor Contract Lawtranslated textseverancetranslated text。', 'translated textsign，companycannottranslated textsigntranslated textseverancetranslated text。', 'translated textcompanypaymenttranslated textseverancetranslated text，translated text。', 'translated text', 'translated text,translated textsigntranslated text,severance'),

  ('judg-2022-subuyi4svqzbx', '(2022)translated text0104translated text9346translated text', 'translated textcompanypregnancytranslated textdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'pregnancytranslated text', '2022-10-01', 'translated text：translated text（translated textplatformtranslated text）；translated text：translated textcompany', 'pregnancyplatformtranslated textroletranslated text，translated textaveragesalarytranslated text。', 'translated textweektranslated textroletranslated textnotice。companytranslated text，translated text。payroll-account transactionstranslated textaveragetranslated textbase salary。', 'translated text。translated textworkservice periodtranslated textwage basiscalculate，stabletranslated textcannottranslated textbasistranslated text。', 'roletranslated text，translated text；translated textsalarytranslated textcalculate。', 'translated textcompanytranslated textpaymenttranslated text。', 'translated text', 'pregnancy,translated text,workservice period,translated textcalculate'),

  ('judg-2022-oi6gzk2a2rdsx', '(2022)translated text0106translated text17509translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated text', '2022-09-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated text，translated text。', 'translated text，companytranslated textdaytranslated text，translated textrecord。translated text，translated textretaintranslated text。', 'companytranslated text，translated text。translated text，translated text，translated text。', 'translated text，translated textroletranslated text。', 'confirmtranslated text，translated textcompanytranslated textroletranslated textsalary。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2022-u23rt4by43cvx', '(2022)translated text0108translated text3218translated text', 'translated textcompanytranslated textsigntranslated textdisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated textsigntranslated text', '2022-08-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textworktranslated text，translated text，translated textdisputetranslated textsalarytranslated text。', 'translated text、translated textsalaryrecordtranslated text，translated textcompanytranslated text。translated textsystemtranslated textdeletetranslated textrecordtranslated text，translated textdatatranslated text。', 'translated text，translated text。translated textdatatranslated text，translated text。', 'translated textsigntranslated textcantranslated text；companytranslated text。', 'translated textcompanypaymenttranslated textsalaryshortfall，translated text。', 'translated text', 'translated text,translated textsalary,datatranslated text,translated text'),

  ('judg-2022-wwidckfjzvnfx', '(2022)translated text12467translated text', 'translated textcompanytranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated text', '2022-07-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textrecordtranslated textalreadytranslated text。', 'translated textsystemtranslated text。translated textviewtranslated textrecord，translated textsendtranslated text。', 'translated texthealthcaretranslated textcannottranslated text，companytranslated textbasis。translated text，translated textseverancetranslated text。', 'translated textrecordtranslated text，companytranslated text。', 'translated textcompanypaymenttranslated text。', 'translated text', 'healthcaretranslated text,translated text,translated text,translated text'),

  ('judg-2022-uwjorxvks3ndx', '(2022)translated text0115translated text22106translated text', 'translated textservicecompanytranslated textsalarytranslated textdisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textsalarytranslated text', '2022-06-01', 'translated text：translated text（translated text）；translated text：translated textservicecompany', 'companytranslated text，translated text。', 'translated textmonthly salarytranslated text，companytranslated textalltranslated text。translated text，translated textdirectlytranslated text。', 'translated textbasistranslated textsalarytranslated textlabor lawtranslated textpaymenttranslated text。translated text，translated textpaymenttranslated text。', 'translated textcalculatetranslated text，translated textsalary，translated text。', 'translated textservicecompanytranslated textsalarytranslated textpaymenttranslated textseverance。', 'translated text', 'translated textsalary,translated textpayment,translated text,translated text'),

  ('judg-2022-lcd3lk2dumitx', '(2022)translated text0112translated text814translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2022-05-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textreconciletranslated textdatetranslated text，disputetranslated textwhethertranslated text。', 'translated textupdatetranslated text，translated text。companytranslated textroletranslated text、emailremindertranslated textactualtranslated text。', 'translated text，translated text，translated text。', 'translated text，translated text。', 'confirmtranslated textcompanytranslated text，translated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2022-tuut356rv2fkx', '(2022)translated text0105translated text16953translated text', 'translated textcompanytranslated textsigntranslated textdisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'translated textsigntranslated text', '2022-04-15', 'translated text：translated text（systemtranslated text）；translated text：translated textcompany', 'systemtranslated textsigntranslated text，translated textweektranslated text，translated textdisputetranslated textrecordtranslated text。', 'translated textemail，translated textsigntranslated text。translated textplatformtranslated textweektranslated text，companytranslated textdatetranslated text。', 'translated text，translated textsigntranslated text。translated textworktranslated text，translated textpaymenttranslated text。', 'translated textrecordtranslated text，translated textdatetranslated textalreadytranslated text。', 'translated textcompanytranslated textsigntranslated text，translated text。', 'translated text', 'translated textsigntranslated text,translated text,translated text,translated text'),

  ('judg-2022-tctprnwdtdwtx', '(2022)translated text0104translated text5032translated text', 'translated texte-commercecompanytranslated textpaymentdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'translated textpayment', '2022-03-22', 'translated text：translated text（translated text）；translated text：translated texte-commercecompany', 'platformtranslated text，translated textdeparturetranslated text，translated text。', 'translated textsigntranslated texttransaction，systemtranslated textamount。translated textdeparturetranslated textcompanytranslated text，translated text。', 'completedtranslated text，labor lawtranslated textpayment。departuretranslated textcannottranslated textsalary。', 'translated textdeparturetranslated textalreadytranslated text，companytranslated textidentitytranslated text。', 'translated texte-commercecompanytranslated textpaymenttranslated text。', 'translated text', 'translated text,salarypayment,translated textpayment,translated text'),

  ('judg-2022-bqe6yhzidtfox', '(2022)translated text0106translated text18640translated text', 'translated textcompanytranslated textseverancedisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated textseverance', '2022-02-01', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textdayworktranslated textdaytranslated text，translated textseverance。', 'translated textweektranslated textweektranslated textwork，companytranslated textdaytranslated text、translated textweektranslated text。translated text，translated text。', 'translated text，translated text。companytranslated text，translated textseverance，cannottranslated textdeparture。', 'translated text，departurereasontranslated textcompanytranslated text。', 'translated textcompanypaymenttranslated textseverancetranslated text。', 'translated text', 'translated text,translated text,severance,translated text'),

  ('judg-2022-wvve5kpup5ezx', '(2022)translated text0108translated text2715translated text', 'translated textservicecompanytranslated textdisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated text', '2022-01-08', 'translated text：translated text（compliancetranslated text）；translated text：translated textservicecompany', 'compliancetranslated textsigntranslated textcompanytranslated textretaintranslated text，translated text。', 'translated textsigntranslated text，translated textalltranslated text。emailrecordtranslated text，companytranslated textsigntranslated text。', 'translated text，translated textconfirmtranslated textspecifictranslated text；companycannottranslated text。', 'companytranslated textrecordtranslated textsigntranslated text。', 'translated textservicecompanytranslated text，translated text。', 'translated text', 'translated text,translated text,translated text'),

  ('judg-2021-wqlxromfia2bx', '(2021)translated text14208translated text', 'translated textcompanytranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated text', '2021-12-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，companytranslated textroletranslated textimmediatelytranslated text；translated textclaimtranslated text。', 'translated textresponsible fortranslated text，translated textcompanytranslated text。translated textsendtranslated textproposal，translated text，translated text。', 'translated textlocationtranslated text。Labor Contract Lawtranslated textfirsttranslated text；companytranslated textrole，translated text。translated text，translated text。', 'translated textroletranslated text，translated text。', 'confirmtranslated text，companytranslated textrole；translated textsalarytranslated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2021-rt7altizxhojx', '(2021)translated text0115translated text9981translated text', 'translated textcompanytranslated textseverancedisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textseverance', '2021-11-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textclaimseverance。', 'translated textsalarytranslated text。translated textreplytranslated text，translated textnotice。', 'translated textpaymenttranslated text，Labor Contract Lawtranslated textpaymentseverance。translated textcannottranslated textsalarytranslated text。', 'translated text，translated textdirectlytranslated text。', 'translated textcompanytranslated text，translated textseverancetranslated text。', 'translated text', 'translated text,translated text,severance,translated text'),

  ('judg-2021-poh357mkycawx', '(2021)translated text0112translated text23164translated text', 'translated textcompanytranslated textcalculatedisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated textcalculate', '2021-10-01', 'translated text：translated text（translated textengineer）；translated text：translated textcompany', 'translated textcompanybasistranslated textengineer，translated textbasistranslated text。', 'translated textCtranslated text。translated text，translated textrelevanttranslated text。companymonthlytranslated textpaymenttranslated text。', 'translated textcannottranslated text，translated text，translated text。translated textsalarytranslated text，translated textwage basis。', 'companytranslated textcannottranslated text，translated textsalarytranslated textrecordtranslated text。', 'translated textcompanypaymenttranslated text。', 'translated text', 'translated text,translated text,translated textwage basis,translated text'),

  ('judg-2021-7bv4huf4fojnx', '(2021)translated text0105translated text547translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'translated text', '2021-09-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated text。', 'translated textgrouptranslated text，translated text。translated text，translated textlocationtranslated text。', 'grouptranslated textcontenttranslated textcompanytranslated text，translated textcompanytranslated text。translated textroletranslated text，translated textalreadytranslated textcannottranslated text。', 'translated text，translated textroletranslated textrecordtranslated text。', 'translated textcompanytranslated text，translated textpaymenttranslated textsalary。', 'translated text', 'translated text,translated text,translated text,translated textrecord'),

  ('judg-2021-vosoz2otxzczx', '(2021)translated text0104translated text11736translated text', 'translated textservicecompanytranslated textsigntranslated textdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'translated textsigntranslated text', '2021-08-15', 'translated text：translated text（translated text）；translated text：translated textservicecompany', 'translated textworktranslated text，translated text，translated text。', 'translated textaccepttranslated text，companytranslated textsigntranslated text。departuretranslated textsendtranslated text，securitytranslated text。', 'actualtranslated text，companytranslated textsigntranslated textsalary。translated text，translated textbasis。', 'translated text，translated text；translated text。', 'translated textservicecompanypaymenttranslated textsalaryshortfall，translated text。', 'translated text', 'translated text,translated textsalary,translated text,translated text'),

  ('judg-2021-pytevehz7nixx', '(2021)translated text0106translated text20495translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated text', '2021-07-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textdeparturetranslated textsigntranslated text，translated text。', 'translated text，translated textsigntranslated textdeparturetranslated text。translated text，companytranslated text，translated textnoticetranslated textthentranslated text。', 'translated textallworktranslated text，translated textcompanytranslated text。translated textbasistranslated text，translated text。', 'translated textconfirmtranslated text，companyagreetranslated textseverancetranslated textdispute。', 'translated textcompanytranslated textpaymenttranslated text，translated text。', 'translated text', 'translated textdeparturetranslated text,translated text,translated text,translated text'),

  ('judg-2021-t7qn75lyphosx', '(2021)translated text0108translated text3874translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated text', '2021-06-01', 'translated text：translated text（translated textengineer）；translated text：translated textcompany', 'translated textcompanytranslated textthentranslated text，translated textengineertranslated text。', 'translated textmonthlytranslated text，actualreceivedtranslated text，translated textpayment。companytranslated text。', 'translated textagree，translated textpaymentsalarytranslated text。translated text，translated text。', 'translated text，companytranslated text。', 'translated textcompanypaymentalltranslated text、translated textshortfalltranslated textseverance。', 'translated text', 'translated text,salarypayment,translated text,translated text'),

  ('judg-2021-mknusneyk7bnx', '(2021)translated text15902translated text', 'translated texte-commercecompanytranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated text', '2021-05-08', 'translated text：translated text（translated text）；translated text：translated texte-commercecompany', 'translated text，companytranslated text。', 'translated textannualtranslated text，translated text。translated textdayrecordtranslated text。', 'translated text，translated textcompanytranslated text；translated textalreadytranslated text，translated textcantranslated text。', 'translated text、translated textrecord，companytranslated text。', 'translated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2021-odhwm5ccs746x', '(2021)translated text0115translated text7261translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated text', '2021-04-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textdaytranslated textcompanyworktranslated text。', 'translated textcompanytranslated text、translated textaccepttranslated text，translated textweektranslated text。translated text，translated textcontent。', 'actualtranslated text，translated textsigntranslated text。translated textworktimetranslated textcompanytranslated text，translated textpaymenttranslated text。', 'translated text，servicetranslated texttimetranslated textwork。', 'translated textcompanypaymenttranslated textsigntranslated textworktimetranslated text。', 'translated text', 'translated text,signtranslated text,translated textworktime,translated text'),

  ('judg-2021-qzcjkshtki62x', '(2021)translated text0112translated text19438translated text', 'translated textcompanytranslated textsalarydisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated textsalary', '2021-03-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textsalary，companytranslated text。', 'translated textrecordtranslated text，translated textsystemtranslated text，translated textrecordtranslated text。companydirectlytranslated textmonthly wagestranslated textalltranslated text。', 'salarytranslated textcalculatebasis。cannottranslated text，translated textsalarytranslated textpaymenttranslated text。', 'translated textalreadyconfirm，translated textrecordcannottranslated text，companytranslated text。', 'translated textcompanytranslated textsalarytranslated text。', 'translated text', 'translated textsalary,translated textsalary,translated textpayment,translated text'),

  ('judg-2021-lcdbebavxelix', '(2021)translated text0105translated text2560translated text', 'translated textlogisticscompanytranslated textseverancedisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'translated textseverance', '2021-02-01', 'translated text：translated text（translated text）；translated text：translated textlogisticscompany', 'logisticscompanytranslated text，translated text。', 'translated textaveragetranslated textweektranslated text，companytranslated textcalculatetranslated text。translated text，translated textnoticetranslated textmonthly wages。', 'translated textcannottranslated text。translated textcompanytranslated text，translated textpaymentseverancetranslated text。', 'translated textrecordtranslated textweektranslated text，companytranslated textpaymentseverance。', 'translated textlogisticscompanypaymenttranslated textseverancetranslated textsalary。', 'translated text', 'translated text,translated textweektranslated text,severance,translated text'),

  ('judg-2021-hkfehbgpfshax', '(2021)translated text0104translated text13179translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'translated text', '2021-01-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textfirsttranslated text，translated textsigntranslated text，translated textdatetranslated text。', 'translated textcompanytranslated text、accepttranslated text。translated textsigntranslated text，companytranslated text。', 'whethertranslated textbasisactualtranslated textpaymenttranslated text；translated textactualtranslated text，translated text，cannotpassedtranslated textsigntranslated text。', 'translated text，translated textactualtranslated text。', 'confirmtranslated textdatetranslated text，translated textcompanytranslated textsigntranslated text。', 'translated text', 'translated text,signtranslated text,actualtranslated text,translated textdate'),

  ('judg-2020-3zhrv2rxnhzlx', '(2020)translated text0106translated text8826translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated text', '2020-12-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textweektranslated text，translated text。', 'translated textcompanytranslated textroletranslated text，translated textnotice。translated textcompanytranslated textinterviewinvitation，translated text。translated text。', 'roletranslated text，translated textmaytranslated text。translated textroletranslated textclaim；translated text，translated textfirsttranslated text。', 'translated text，translated text，translated text。', 'translated text，translated textcompanytranslated text，translated textpaymenttranslated textsalaryshortfall。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2020-zylgxik43asux', '(2020)translated text0108translated text21607translated text', 'translated textseverancedisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated textseverance', '2020-11-22', 'translated text：translated text（translated text）；translated text：translated text', 'translated text，translated textseverance。', 'translated text，translated textnoticetranslated text。translated textsalary，translated textseverance。', 'translated text、translated textortranslated text，translated textseverancetranslated text。translated textcannottranslated text。', 'translated text，translated textsalarytranslated textseverancetranslated text。', 'confirmtranslated textseverancetranslated text，translated textfirsttranslated text。', 'translated text', 'translated text,translated text,severance,translated text'),

  ('judg-2020-nmaowp5ntndrx', '(2020)translated text6134translated text', 'translated textservicecompanytranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated text', '2020-10-01', 'translated text：translated text（compliancetranslated text）；translated text：translated textservicecompany', 'translated textcompliancetranslated text，translated textbasistranslated textaveragesalarytranslated text。', 'companytranslated texttransaction，translated text。translated textannualtranslated textaveragesalarytranslated text，translated textbasistranslated textcalculateservice periodtranslated text。', 'translated textcannottranslated text，translated text。translated textseverancecalculatetranslated text，translated textsalarytranslated textwage basistranslated textservice periodtranslated text。', 'translated text；translated textcalculatetranslated textalltranslated text。', 'translated textservicecompanytranslated textbasistranslated textpaymenttranslated text。', 'translated text', 'translated text,translated text,salarytranslated text,translated textcalculate'),

  ('judg-2020-tib24aou4nrtx', '(2020)translated text0115translated text17350translated text', 'translated textcompanytranslated textdisputetranslated textdisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textdisputetranslated text', '2020-09-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated textmaytranslated textproposal。', 'translated text，companytranslated textroletranslated text。translated textpurposetranslated text，companytranslated text，translated textlocation。', 'translated textdirectlytranslated text；translated textrole，translated text。translated text。', 'translated textconfirmtranslated text，translated textcalculate，translated textagreetranslated textscopetranslated textaccepttranslated text。', 'translated textconfirmtranslated textcompanytranslated text、translated textmonthly wages，translated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2020-ahslwiejocxax', '(2020)translated text0112translated text1049translated text', 'translated textcompanytranslated textsigntranslated textdisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated textsigntranslated text', '2020-08-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，translated text，translated text。', 'translated textsigntranslated textsigntranslated textcompanycannottranslated text。translated text，translated text，translated textconfirmactualtranslated text。', 'cannottranslated textsigntranslated text，translated textsalarytranslated text。translated text，translated text；translated text，cannottranslated text。', 'companytranslated text，translated text、translated text。', 'translated textcompanypaymenttranslated textsigntranslated textsalaryshortfall；translated text。', 'translated text', 'translated text,translated textsalary,translated text,translated text'),

  ('judg-2020-nn3lytpaqezix', '(2020)translated text0105translated text14983translated text', 'translated texte-commercecompanytranslated textdisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'translated text', '2020-07-22', 'translated text：translated text（translated text）；translated text：translated texte-commercecompany', 'translated textdatatranslated text，companytranslated text。', 'translated textresponsible fortranslated textplatformtranslated text，translated text。companytranslated text，translated text，directlytranslated text。', 'translated textdatatranslated text，companytranslated text。translated text，translated textpaymenttranslated text。', 'translated textreason，translated textnoticetranslated textcannottranslated text。', 'translated texte-commercecompanytranslated textpaymenttranslated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2020-pl3mvlcrwfi2x', '(2020)translated text0104translated text4685translated text', 'translated textcompanytranslated textsalarytranslated textdisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'translated textsalarytranslated text', '2020-06-01', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textallsalary，translated textworktranslated text。', 'companytranslated text，translated textonlinesigntranslated text，translated textpaymenttranslated textsalary。translated textsalarytranslated text。', 'translated textaccepttranslated text，companycannottranslated text。translated textsalarytranslated text，translated textbasis。', 'translated textcompanytranslated text，translated textwork，translated textsalarytranslated textpayment。', 'translated textcompanypaymenttranslated textsalary、translated textseverance。', 'translated text', 'translated textsalary,translated textpayment,translated text,salarytranslated text'),

  ('judg-2020-lq6anxxa7at7x', '(2020)translated text0106translated text22574translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated text', '2020-05-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，companytranslated text。', 'translated textworktranslated text，translated text。translated textpassedtranslated text、translated text，translated textreplytranslated text，translated textmemotranslated texttime。', 'translated text，translated text，translated text。companytranslated text。', 'translated text、translated textsigntranslated text，translated text。', 'confirmtranslated textcompanytranslated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2020-qkilmnwpegx2x', '(2020)translated text0108translated text7903translated text', 'translated textlogisticscompanytranslated textsigntranslated textdisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated textsigntranslated text', '2020-04-15', 'translated text：translated text（translated text）；translated text：translated textlogisticscompany', 'translated text，translated text，translated textcalculatetranslated text。', 'translated text，translated text。companytranslated text，salarytranslated text。', 'companytranslated text。translated text，translated textworktime，translated textaccording totranslated textpaymenttranslated text。', 'translated textrecordtranslated text，companycannottranslated textactualtranslated text。', 'translated textlogisticscompanypaymenttranslated textsigntranslated text，translated text。', 'translated text', 'translated textsigntranslated text,translated text,translated textworktime,translated text'),

  ('judg-2020-bzcfwrmqpp4yx', '(2020)translated text18126translated text', 'translated textcompanysalarytranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'salarytranslated text', '2020-03-22', 'translated text：translated text（translated textassistant）；translated text：translated textcompany', 'translated textassistanttranslated text，companytranslated textmonthly wagestranslated text。', 'translated text、translated textdatatranslated textaccepttranslated text，companytranslated textmonthly wages。translated textemailtranslated text。', 'actualtranslated textworktranslated textpaymentsalary。labor lawtranslated textpaymenttranslated text。', 'translated textworktranslated text，translated text，companytranslated textsalary。', 'translated textcompanypaymenttranslated textmonthly wagestranslated text。', 'translated text', 'salarytranslated text,translated text,salarypayment,translated text'),

  ('judg-2020-i2zu7l37uvd6x', '(2020)translated text0115translated text3375translated text', 'translated textcompanytranslated textseverancedisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated textseverance', '2020-02-01', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，companytranslated textaccepttranslated text，translated textdeparturetranslated text。', 'translated text。translated text，companytranslated text，translated textrole；translated textnotice。', 'translated text。translated text，companytranslated textpaymentseverance。', 'translated textnoticetranslated textcompanytranslated text，translated text，translated text。', 'translated textcompanypaymenttranslated textseverancetranslated text。', 'translated text', 'translated text,translated text,translated text,severance'),

  ('judg-2020-ng6jl76ox3p2x', '(2020)translated text0112translated text12642translated text', 'translated textcompanytranslated textwhethertranslated textdisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated textwhethertranslated text', '2020-01-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textagreetranslated text，companyclaimtranslated textalreadytranslated text。', 'translated text，translated textworklocation、salary、translated textcontent。translated text，companytranslated textconfirmtranslated text。', 'translated textcantranslated text，translated text。translated textconfirmtranslated text。', 'translated text，cannottranslated textsigntranslated text。', 'translated textcompanytranslated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2019-5c5zxpklyrccx', '(2019)translated text0105translated text9608translated text', 'translated textcompanycannottranslated textworktranslated textdisputetranslated text', 'court_bj_chaoyang', 'translated textdispute', 'cannottranslated textworktranslated text', '2019-12-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated text，companytranslated textrole。', 'translated text，translated textsystemtranslated textdatatranslated text。companytranslated textrecord，translated text，directlytranslated text。', 'cannottranslated text、translated text。companytranslated textsystemreason，translated text。translated textroletranslated text，translated text。', 'translated text，companytranslated text。', 'translated text、translated text，translated textdisputetranslated textbase salarytranslated textposition allowance。', 'translated text', 'translated text,cannottranslated text,translated text,translated text'),

  ('judg-2019-4r2lb5skmqrxx', '(2019)translated text0104translated text21357translated text', 'translated textcompanytranslated textseverancedisputetranslated text', 'court_sh_xuhui', 'translated textdispute', 'translated textseverance', '2019-11-22', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textcompanytranslated text，translated textmonthly wagestranslated textalltranslated text，translated textmake up。', 'translated text，companytranslated textmemotranslated text。departuretranslated textmonthly wagestranslated text，translated textdo nottranslated text。', 'translated text，translated textpaymentseverance。translated textcannottranslated textworkservice periodcalculatetranslated text。', 'companytranslated text，translated textdo nottranslated textcannottranslated textseverance，paidtranslated text。', 'translated textcompanytranslated textseveranceshortfalltranslated text。', 'translated text', 'translated text,workservice period,severance,shortfall'),

  ('judg-2019-t3fergnpjd2jx', '(2019)translated text0106translated text5194translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_jingan', 'translated textdispute', 'translated text', '2019-10-01', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textdaytranslated text，translated textbasistranslated textamount。', 'translated text，afternoontranslated text。companytranslated textmemo，translated textrecordtranslated text；monthlytranslated textsalarytranslated text。', 'translated text，translated text。translated textsalarytranslated text，translated textwage basistranslated textcalculate。', 'translated texttimetranslated text，companytranslated text；translated textbasistranslated text。', 'translated textcompanypaymenttranslated text，translated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2019-zbwb4crhgo36x', '(2019)translated text0108translated text16580translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_bj_haidian', 'translated textdispute', 'translated text', '2019-09-08', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textdeletetranslated text，companyclaimtranslated text；translated textwhethertranslated text。', 'translated textcompletedtranslated textretaintranslated text，responsible fortranslated textsendtranslated textemail。companytranslated text，translated text。', 'translated textbasis，translated text。translated textcannottranslated text，translated text。', 'translated text、worktranslated text，translated text。', 'translated textcompanytranslated text，translated textsalarytranslated text。', 'translated text', 'translated textdispute,translated text,translated text,translated text'),

  ('judg-2019-lpaqh5zxfxycx', '(2019)translated text2421translated text', 'translated textcompanytranslated textsigntranslated textdisputetranslated text', 'arb_bj_chaoyang', 'translated textdispute', 'translated textsigntranslated text', '2019-08-15', 'translated text：translated text（translated text）；translated text：translated textcompany', 'translated textsigntranslated text，translated text，arbitrationtranslated text。', 'translated textworktranslated text，companytranslated textconfirmroletranslated textsalary。translated textdatetranslated text，translated textaccount，translated text。', 'translated textroleconfirmtranslated text、worktimetranslated text，translated text，translated text。translated text。', 'companytranslated textsigntranslated text，translated text，translated text。', 'translated textcompanypaymenttranslated textsalaryshortfall；translated text。', 'translated text', 'translated textsigntranslated text,translated textsalary,translated text,translated text'),

  ('judg-2019-hk3lrmmyufelx', '(2019)translated text0115translated text13895translated text', 'translated textcompanytranslated textdisputetranslated text', 'court_sh_pudong', 'translated textdispute', 'translated text', '2019-07-22', 'translated text：translated text（datatranslated text）；translated text：translated textcompany', 'datatranslated text，emailtranslated textreason。', 'translated textreconciletranslated textrecord，translated textnotice。translated textemailtranslated textclaimtranslated textstable，companytranslated text。', 'translated textclaimtranslated text，translated text。companytranslated text，translated text。', 'translated textdirectlyrelevant，translated textcannottranslated text。', 'translated textcompanypaymenttranslated text。', 'translated text', 'translated text,translated text,translated text,translated text'),

  ('judg-2019-mgr5rggzmojqx', '(2019)translated text0112translated text8467translated text', 'translated textlogisticscompanytranslated textdisputetranslated text', 'court_sh_minhang', 'translated textdispute', 'translated text', '2019-06-01', 'translated text：translated text（translated text）；translated text：translated textlogisticscompany', 'logisticstranslated textfixed salary，translated textsalaryproposaltranslated text。', 'translated textmonthly salary，companypassedgrouptranslated text，translated text。translated text，translated textsigntranslated text。', 'salarytranslated textcontent，translated text。translated textlabor lawtranslated text，translated textbasistranslated textpaymenttranslated text。', 'grouptranslated textcannottranslated textdo nottranslated text，translated textsalarytranslated textaccepttranslated text。', 'translated textlogisticscompanymake upsalaryshortfall，translated textpaymenttranslated textseverance。', 'translated text', 'translated text,translated textpayment,translated text,salarypayment');

-- ══ Article citations for additional cases (dis_*) ══
INSERT INTO citations (citation_id, case_id, target_type, target_id, label) VALUES
  ('cite-yjqpx2kbp5rcx', 'judg-2023-q36mikmywxv4x', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-5kmsixmynu2ax', 'judg-2023-q36mikmywxv4x', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-h4qgrfasexk3x', 'judg-2023-zzsljcxcreq2x', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-5ygjcjc75qsqx', 'judg-2023-dylu2owo2qhlx', 'article', 'law-lcl-047-7nfprxbbx', 'translated text'),
  ('cite-k5kciwhnvj46x', 'judg-2023-dylu2owo2qhlx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-pgjzy47jckodx', 'judg-2023-puzo4eop2tq2x', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-r6gqijopctvnx', 'judg-2023-hmr46qifodqbx', 'article', 'law-lcl-082-ysfbrkvxx', 'translated text'),
  ('cite-xynqj7vwmp4ex', 'judg-2023-hmr46qifodqbx', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-5uj5nt4lssuex', 'judg-2023-zwgcbdluhq62x', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-op43shspupz6x', 'judg-2023-5eimaw52kscwx', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-5n7qpnmltk24x', 'judg-2023-5eimaw52kscwx', 'article', 'art_ll_050', 'translated text'),
  ('cite-3b6b6nlpbbfxx', 'judg-2023-enjavsfusi6px', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-rqwzilrnn3zcx', 'judg-2023-hervlahfsd2fx', 'article', 'art_ll_044', 'translated text'),
  ('cite-kztmv4ctrj65x', 'judg-2023-hervlahfsd2fx', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-7252x2vyosmjx', 'judg-2023-ek263n22aslxx', 'article', 'art_ll_050', 'translated text'),
  ('cite-rpgqtqyk43amx', 'judg-2023-etr6yfiad44ax', 'article', 'art_ll_036', 'translated text'),
  ('cite-3bmc3lougyjjx', 'judg-2023-etr6yfiad44ax', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-mdeca7sjoaqcx', 'judg-2023-2yzgin2idkymx', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-5kfcdunqjy7mx', 'judg-2022-xec3xxwtpqnix', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-oe3nbl2ujrnlx', 'judg-2022-xec3xxwtpqnix', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-7mg3zrxp52vlx', 'judg-2022-addrebp3kyowx', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-lgqe7jfg7yrsx', 'judg-2022-subuyi4svqzbx', 'article', 'law-lcl-047-7nfprxbbx', 'translated text'),
  ('cite-6ekgj2dr72ngx', 'judg-2022-subuyi4svqzbx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-zixn5rmrph6zx', 'judg-2022-oi6gzk2a2rdsx', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-cjvsoiowrrk6x', 'judg-2022-u23rt4by43cvx', 'article', 'law-lcl-082-ysfbrkvxx', 'translated text'),
  ('cite-x3alsfz6ot27x', 'judg-2022-u23rt4by43cvx', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-p3ri2i2zoe7lx', 'judg-2022-wwidckfjzvnfx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-d52pwsk2pgtqx', 'judg-2022-uwjorxvks3ndx', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-n4yzkh6fj7gqx', 'judg-2022-uwjorxvks3ndx', 'article', 'art_ll_050', 'translated text'),
  ('cite-zjmnzjb2a7lqx', 'judg-2022-lcd3lk2dumitx', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-otxqacjv27xgx', 'judg-2022-tuut356rv2fkx', 'article', 'art_ll_044', 'translated text'),
  ('cite-vw2yv6l777n6x', 'judg-2022-tuut356rv2fkx', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-pv2skt6synzvx', 'judg-2022-tctprnwdtdwtx', 'article', 'art_ll_050', 'translated text'),
  ('cite-aoc3b5fadsl5x', 'judg-2022-bqe6yhzidtfox', 'article', 'art_ll_036', 'translated text'),
  ('cite-idhfsw2noenrx', 'judg-2022-bqe6yhzidtfox', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-icvxhyiyoj22x', 'judg-2022-wvve5kpup5ezx', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-uf7rezlxvvwox', 'judg-2021-wqlxromfia2bx', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-m7hfywo3lv24x', 'judg-2021-wqlxromfia2bx', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-t67by4kbjz4yx', 'judg-2021-rt7altizxhojx', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-id533ibndptgx', 'judg-2021-poh357mkycawx', 'article', 'law-lcl-047-7nfprxbbx', 'translated text'),
  ('cite-z7rzztmkn2ogx', 'judg-2021-poh357mkycawx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-6iskjltxz3pqx', 'judg-2021-7bv4huf4fojnx', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-ccgs7id22udkx', 'judg-2021-vosoz2otxzczx', 'article', 'law-lcl-082-ysfbrkvxx', 'translated text'),
  ('cite-6wnl4bz64453x', 'judg-2021-vosoz2otxzczx', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-ydho2m2ueu2xx', 'judg-2021-pytevehz7nixx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-wdzlfc73kqbrx', 'judg-2021-t7qn75lyphosx', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-v64f2floz7ztx', 'judg-2021-t7qn75lyphosx', 'article', 'art_ll_050', 'translated text'),
  ('cite-35map6lyrnowx', 'judg-2021-mknusneyk7bnx', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-thwnv2jlfo5zx', 'judg-2021-odhwm5ccs746x', 'article', 'art_ll_044', 'translated text'),
  ('cite-oeznv7l24dozx', 'judg-2021-odhwm5ccs746x', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-ayjobmawahoox', 'judg-2021-qzcjkshtki62x', 'article', 'art_ll_050', 'translated text'),
  ('cite-baktiy2uaus5x', 'judg-2021-lcdbebavxelix', 'article', 'art_ll_036', 'translated text'),
  ('cite-aldoiidaqys2x', 'judg-2021-lcdbebavxelix', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-b4ihooij65gox', 'judg-2021-hkfehbgpfshax', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-k62zxyclapdix', 'judg-2020-3zhrv2rxnhzlx', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-kv5hskcmpnlqx', 'judg-2020-3zhrv2rxnhzlx', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-pxqx2dnatewex', 'judg-2020-zylgxik43asux', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-jtclue62mv25x', 'judg-2020-nmaowp5ntndrx', 'article', 'law-lcl-047-7nfprxbbx', 'translated text'),
  ('cite-7hti5adh76y3x', 'judg-2020-nmaowp5ntndrx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-gqfdaknxhuijx', 'judg-2020-tib24aou4nrtx', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-pgtfotmlzmmbx', 'judg-2020-ahslwiejocxax', 'article', 'law-lcl-082-ysfbrkvxx', 'translated text'),
  ('cite-bajlnvtsqu4qx', 'judg-2020-ahslwiejocxax', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-q42vga2z36kyx', 'judg-2020-nn3lytpaqezix', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-q5tzz4iu7pvmx', 'judg-2020-pl3mvlcrwfi2x', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-upvkno2fhrnmx', 'judg-2020-pl3mvlcrwfi2x', 'article', 'art_ll_050', 'translated text'),
  ('cite-k3ukf437lwuqx', 'judg-2020-lq6anxxa7at7x', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-scblbps7ebrmx', 'judg-2020-qkilmnwpegx2x', 'article', 'art_ll_044', 'translated text'),
  ('cite-qgz4wwbnby5fx', 'judg-2020-qkilmnwpegx2x', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-5xqmfcikbncvx', 'judg-2020-bzcfwrmqpp4yx', 'article', 'art_ll_050', 'translated text'),
  ('cite-xeqxnz7iv4h5x', 'judg-2020-i2zu7l37uvd6x', 'article', 'art_ll_036', 'translated text'),
  ('cite-4axydmccqsoux', 'judg-2020-i2zu7l37uvd6x', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-wamybbvrx7kjx', 'judg-2020-ng6jl76ox3p2x', 'article', 'law-lcl-010-ogk5vtnfx', 'translated text'),
  ('cite-ialxnm6xysiox', 'judg-2019-5c5zxpklyrccx', 'article', 'law-lcl-040-blpnlbptx', 'translated text'),
  ('cite-azcsraewecawx', 'judg-2019-5c5zxpklyrccx', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-pvhod6xswle5x', 'judg-2019-4r2lb5skmqrxx', 'article', 'law-lcl-046-dvyxmanqx', 'translated text'),
  ('cite-zc6u63qzxca6x', 'judg-2019-t3fergnpjd2jx', 'article', 'law-lcl-047-7nfprxbbx', 'translated text'),
  ('cite-7atsfqgcqufsx', 'judg-2019-t3fergnpjd2jx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-gbgkzyep5vvrx', 'judg-2019-zbwb4crhgo36x', 'article', 'law-lcl-048-7qfuia53x', 'translated text'),
  ('cite-cxt43i2pbmpbx', 'judg-2019-lpaqh5zxfxycx', 'article', 'law-lcl-082-ysfbrkvxx', 'translated text'),
  ('cite-rpae5lf7qol5x', 'judg-2019-lpaqh5zxfxycx', 'article', 'law-lcl-039-ux5gjbrxx', 'translated text'),
  ('cite-pguyw5c24la7x', 'judg-2019-hk3lrmmyufelx', 'article', 'law-lcl-087-a6lj7dyvx', 'translated text'),
  ('cite-blee2y4ss463x', 'judg-2019-mgr5rggzmojqx', 'article', 'law-lcl-038-yeazgq4ex', 'translated text'),
  ('cite-zeaowatahrftx', 'judg-2019-mgr5rggzmojqx', 'article', 'art_ll_050', 'translated text');

-- ── Counters (seed so newly-issued IDs don't collide with seed IDs) ──


-- ── Task-specific authority corpus: compensation basis + recruitment privacy ──
-- The statutes/articles below are simplified public-law text. The four cases are
-- translated textcasetranslated textdisputetranslated textarticle，translated text。
INSERT INTO statutes (statute_id, name, short_name, issuer, effective_date, status, summary) VALUES
  ('stat_lcl_reg', 'translated textLabor Contract Lawtranslated text', 'Labor Contract Lawtranslated text', 'translated text', '2008-09-18', 'translated text',
    'translated textLabor Contract Lawtranslated text；translated textseverancemonthly wagestranslated textsalarycalculate，translated text、translated text。'),
  ('stat_pipl', 'translated textPersonal Information Protection Law', 'Personal Information Protection Law', 'translated text', '2021-11-01', 'translated text',
    'translated text、translated textagree、minimum necessitytranslated textsensitive personal informationtranslated textpurpose、translated text、translated textseparate consenttranslated text。');

INSERT INTO statute_articles (article_id, statute_id, article_no, seq, heading, text) VALUES
  ('law-lcl-008-4gmmlabjx', 'stat_lcl', 'translated text', 8, 'translated textmemotranslated text',
    'translated text，translated textworkcontent、worktranslated text、worklocation、translated text、securitytranslated text、translated text，andtranslated textunderstandtranslated text；translated textunderstandtranslated textdirectlyrelevanttranslated text，translated textmemo。'),
  ('art_lcl_reg_027', 'stat_lcl_reg', 'translated text', 27, 'severancemonthly wagestranslated text',
    'Labor Contract Lawtranslated textseverancemonthly wages，according totranslated textsalarycalculate，translated textsalaryortranslated textsalaryandtranslated text、translated text。translated textortranslated textaveragesalarytranslated textsalarytranslated text，according totranslated textsalarytranslated textcalculate；worktranslated text，according toactualworktranslated textcalculateaveragesalary。'),
  ('art_pipl_006', 'stat_pipl', 'translated text', 6, 'purposetranslated textminimum necessity',
    'translated text、translated textpurpose，translated textpurposedirectlyrelevant，translated text。translated text，translated textpurposetranslated textscope，translated text。'),
  ('art_pipl_013', 'stat_pipl', 'translated text', 13, 'translated text',
    'translated textagree、translated textortranslated text、translated text、translated textortranslated text，translated text；translated text，translated text。'),
  ('art_pipl_014', 'stat_pipl', 'translated text', 14, 'translated text、translated text、translated textagree',
    'translated textagreetranslated text，translated textagreetranslated text、translated text。translated textpurpose、translated text，translated textagree；translated text、translated textseparate consentortranslated textagreetranslated text，translated text。'),
  ('art_pipl_028', 'stat_pipl', 'translated text', 28, 'sensitive personal information',
    'sensitive personal informationtranslated textortranslated text，translated textortranslated text、translated textsecuritytranslated text，translated textdo not、translated text、translated textidentity、healthcarehealth、translated textaccount、translated text。translated textpurposetranslated text，translated text，translated textsensitive personal information。'),
  ('art_pipl_029', 'stat_pipl', 'translated text', 29, 'sensitive personal informationtranslated textseparate consent',
    'translated textsensitive personal informationtranslated textseparate consent；translated text、translated textsensitive personal informationtranslated textagreetranslated text，translated text。');

INSERT INTO cases (case_id, case_number, title, court_id, case_type, cause, judgment_date, parties, summary, facts, reasoning, holding, ruling, outcome, keywords) VALUES
  ('judg-2025-q7m4v2c6t3knx', '(2025)translated text01translated text9123translated text', 'weektranslated textplatformcompanyseverancemonthly wagestranslated text', 'court_sh_no1', 'translated textdispute', 'severancetranslated text', '2025-11-20',
    'translated textweektranslated text；translated textplatformcompany',
    'companytranslated textbase salarycalculateseverance，weektranslated textclaimtranslated textsalaryaverage。translated textsalarytranslated text。',
    'weektranslated textfixed salarytranslated text，translated textposition allowancetranslated textquarterlytranslated text。companyproposaltranslated textfixed salarytranslated textbasis。',
    'severancemonthly wagestranslated textsalarycalculate。translated text、translated text，translated textweektranslated text。',
    'translated textsalaryaveragetranslated textseverancemonthly wages；translated text，cannottranslated textbase salary。',
    'translated textcompanytranslated textwage basismake upseveranceshortfall。', 'translated text',
    'severance,translated textaverage,translated textsalary,translated text,translated text,base salary'),
  ('judg-2025-r5p2w7d4h6jsx', '(2025)translated text0115translated text41880translated text', 'translated textbackground checkcompanyhealthmaterialstranslated textscopetranslated text', 'court_sh_pudong', 'translated text', 'translated text', '2025-10-16',
    'translated text；translated textbackground checkcompany',
    'background checkcompanybasistranslated textauthorizationtranslated textphysical examinationtranslated textmedical history，translated textmemohealth informationtranslated textpurpose、translated text，translated textseparate consent。',
    'translated textauthorizationtranslated textidentity、translated text。background checkcompanytranslated textphysical examinationtranslated text、translated textrecordtranslated textmedical history。',
    'healthcarehealth informationtranslated textsensitive personal information。translated textbackground-check authorizationcannottranslated texthealth information；translated textpurposedirectlyrelevant、translated textminimum necessityscope，translated textsensitive personal informationtranslated textseparate consent。',
    'translated textbackground checktranslated texthealth informationtranslated textpurposetranslated text；translated textauthorizationtranslated texthealthmaterialsauthorization。',
    'translated textscopehealthmaterials、deletetranslated text。', 'translated text',
    'health information,background check,sensitive personal information,minimum necessity,separate consent,authorizationscope'),
  ('judg-2025-t6n3y5f2k7qmx', '(2025)translated text0112translated text33771translated text', 'translated textcompanytranslated texthealth informationpurposetranslated text', 'court_sh_minhang', 'translated text', 'translated text', '2025-08-28',
    'translated text；translated textcompany',
    'translated textidentitytranslated textphysical examinationtranslated text，translated textroletranslated text，translated textpurposetranslated textagree。',
    'translated textauthorizationtranslated textidentity、translated textworktranslated text。translated textphysical examinationtranslated text，translated textdatatranslated text。',
    'translated textpurpose、translated text，translated textagreetranslated text。healthcarehealth informationtranslated textsensitive personal informationtranslated text，translated textpurposetranslated text。',
    'identitytranslated textauthorizationtranslated texthealthtranslated textauthorization；purposetranslated texthealth informationtranslated text。',
    'confirmtranslated textscopetranslated text，translated textdeleterelevanthealth information。', 'translated text',
    'health information,translated text,purposetranslated text,translated textagree,sensitive personal information,translated text'),
  ('judg-2025-v4c7r2m6p5ldx', '(2025)translated text0105translated text28664translated text', 'translated textcompanytranslated textmaterialstranslated text', 'court_bj_chaoyang', 'translated text', 'translated text', '2025-06-12',
    'translated text；translated textcompany',
    'translated textcompanytranslated textroletranslated textdirectlytranslated text、translated textmedical historytranslated textphysical examinationmaterials，translated textpurposetranslated textscope。',
    'translated textroletranslated textdevelopmenttranslated text，translated texthealthtranslated text。companytranslated text、translated textmedical historytranslated textphysical examinationtranslated text。',
    'translated textscopetranslated text、translated textpurposedirectlyrelevanttranslated textminimum necessity。translated texthealthcarehealth informationtranslated textpurpose、translated textseparate consent，translated textcannottranslated textmemo。',
    'translated textprocesstranslated textroletranslated textdirectlytranslated texthealthmaterials。',
    'translated textdeletetranslated textscopetranslated texthealthmaterials。', 'translated text',
    'health information,translated text,translated text,minimum necessity,separate consent,translated text');

INSERT INTO citations (citation_id, case_id, target_type, target_id, label) VALUES
  ('cite-q2v5m7c4k6rnx', 'judg-2025-q7m4v2c6t3knx', 'article', 'law-lcl-047-7nfprxbbx', 'translated textaveragesalary'),
  ('cite-r3w6n2d5p7jsx', 'judg-2025-q7m4v2c6t3knx', 'article', 'art_lcl_reg_027', 'translated textsalarytranslated text'),
  ('cite-s4x2q6v5m7cnx', 'judg-2025-r5p2w7d4h6jsx', 'article', 'art_pipl_006', 'purposetranslated textminimum necessity'),
  ('cite-t5k3r7w2n6dpx', 'judg-2025-r5p2w7d4h6jsx', 'article', 'art_pipl_028', 'health informationtranslated textsensitive personal information'),
  ('cite-v6m4s2y7q5fhx', 'judg-2025-r5p2w7d4h6jsx', 'article', 'art_pipl_029', 'separate consent'),
  ('cite-w2n5t3c6r7kqx', 'judg-2025-t6n3y5f2k7qmx', 'article', 'law-lcl-008-4gmmlabjx', 'translated textdirectlyrelevanttranslated text'),
  ('cite-x3p6v4d2m5sjx', 'judg-2025-t6n3y5f2k7qmx', 'article', 'art_pipl_013', 'translated text'),
  ('cite-y4q7w5f3n2tlx', 'judg-2025-t6n3y5f2k7qmx', 'article', 'art_pipl_014', 'purposetranslated textagree'),
  ('cite-z5r2x6h4p3vmx', 'judg-2025-t6n3y5f2k7qmx', 'article', 'art_pipl_028', 'sensitive personal informationtranslated text'),
  ('cite-c6s3y7k5q2wnx', 'judg-2025-t6n3y5f2k7qmx', 'article', 'art_pipl_029', 'translated textseparate consent'),
  ('cite-d7t4z2m6r5pxx', 'judg-2025-v4c7r2m6p5ldx', 'article', 'art_pipl_006', 'translated textscopetranslated text'),
  ('cite-f2v5c3n7s4qmx', 'judg-2025-v4c7r2m6p5ldx', 'article', 'art_pipl_028', 'healthcarehealth informationtranslated text'),
  ('cite-g3w6d4p2t5rnx', 'judg-2025-v4c7r2m6p5ldx', 'article', 'art_pipl_029', 'separate consent');

INSERT INTO _counters (key, value) VALUES
  ('saved_seq', 2),
  ('citation_seq', 29);

COMMIT;
