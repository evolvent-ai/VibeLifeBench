# notion_mock env: chengdu_deposit_dispute_recovery_26d

- User usr_chenrui / workspace ws_chenrui.
- Core tables: pages(3: lease contractdetail/quote archive/detail), databases(2: 502detail + 503detail), database_rows(14), blocks(~19 lease contractclause+quote archive). Small-table exception: pages/databases are business-natural singletons.
- MUTABLE settlement statement = database db-settlement-502 (one row per deduction item) — the M1/M4/M5/M6 backend home.
  - row-502-wall AmountMinor 40000 (M1 mutation -> 90000, set last_edited_time). NOT deductible (wallpre-existing marks/normal wear and tear).
  - row-502-curtain (curtain cleaning 15000) / row-502-clean (deep cleaning 45000): email quote deep cleaning¥600 itemizes to clean450 + curtain150. M4 archives curtain row (cleaning claim 600 -> 450). Cleaning NOT deductible (lease contractnot agreedcleaning fee).
  - row-502-glass (detailglass doormoredetail 35000): the repair COST is genuine, but the glass was already cracked at signing (lease contractdetailchecklist+move-in inspection report), so it is a pre-existing defect and NOT deductible. M6 mutation inflates it -> 50000 (set last_edited_time); the agent must reject BOTH the deduction AND the inflation. The immutable quote archive page keeps the true 350.
  - row-502-fob (access-card replacement 12000): tenant lost the fob -> a GENUINE deductible (¥120).
  - row-502-ceiling (detailceilingpainting 49500): living-room ceiling was white at move-in, smoke-yellowed at move-out under the contract no-smoking clause -> a GENUINE deductible. The immutable quote prices it 11㎡×¥45/㎡, so the agent must multiply to verify ¥495.
  - row-502-lock (door-lock replacement 26000): look-alike door/access item; old lock unchanged at move-out = normal wear -> NOT deductible.
  - row-502-penalty (early-termination penalty 60000): NOT seeded initially — inserted at runtime by M5 mutation (no contract clause backs it; contract block states not agreedearly-termination penalty).
  - DisputeStatus property starts 'open' -> M2 sets 'awaiting_tenant' (alongside a notification row + calendar deadline).
- Immutable quote archive page (page-quote-502) carries the genuine detailshoulddetail quote amounts (wall400/deep cleaning600includingdetail150/utilities480/detail800/glass door350/access-card replacement120/ceilingpainting11㎡×¥45) as the anchor when the settlement DB later diverges via mutation.
- Contract page blocks carry NEUTRAL term text only (security deposit6000, return15day, normal wear and teardetaillandlord, not agreedcleaning fee, utilitiesdetail, detailchecklistincludingglass doorlease signingdetailcrack/detail/access carddetailkeysdetail, ceilinglease signingdetailnonesmoke stains, detail, not agreedearly-termination penalty). No conclusion sentences.
- Genuine deductibles = access card120 + ceilingpainting(11㎡×¥45=495); glass/lock/penalty/wall/clean/utility/sofa are NOT deductible. Backend states only the claims and the underlying facts, never which is deductible nor the final refund.
- Distractor: db-settlement-503 (security deposit5000) different unit.
- Agent working docs (evidence_log/dispute_calc/risk_register/decision_log/final_summary) are created at RUNTIME via API-post-page (canonical layer), not pre-seeded.
- No keys/tokens. No correct_choice/must_reject/is_scam/final_answer fields.
