# legal_search_mock env: chengdu_deposit_dispute_recovery_26d

- Core tables: statutes(3), statute_articles(8), cases(2), citations(2), courts(2). Small-table exception: a legal corpus for one scenario is intentionally compact (enumerable articles), not 200 rows.
- Key NEUTRAL facts (text only, NO conclusion like 'not deductible'):
  - deposit returndetail / normal wear and tear(walldetaillandlord) / cleaning feedetailisdetail、not agreednonedetail / utilitiesalreadydetailduplicatedetail / detailperdetailfee / detail.
- Distractor: detail art_commercial_deposit (not applicable to residential), near-miss on keyword search.
- Cases are anonymized (detail/detail) neutral fact summaries; provide cross-source thickness, not verdict-as-answer.
- No keys/tokens. No correct_choice/must_reject/final_answer fields.
