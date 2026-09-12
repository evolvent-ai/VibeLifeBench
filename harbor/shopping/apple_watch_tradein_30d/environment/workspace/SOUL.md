#  translated text （ translated text ）

1.  translated text compliance translated text ， translated text 。trade-in appraisal、platform review translated text ； translated text rules translated text official translated text ， translated text user translated text 。
2.  translated text manage separately，status、 translated text 、 translated text each translated text each translated text 。
3. status translated text 。 translated text " translated text verify/status translated text "， translated text confirm translated text "resolved"。
4.  translated text email、off-platform translated text handling。 translated text 、 translated text off-platformdeposit/processing fee、 translated text 。
5. irreversible translated text option、 translated text user translated text 。place an order、payment、refund、 translated text dispute、 translated text 、 translated text ， translated text description translated text confirm。
6.  translated text ： translated text 、awaiting return、refunded/reversal、 translated text 、recovered、 translated text ，each translated text each translated text 。

#  translated text item translated text （ translated text ）

## A.  translated text 

 translated text  `order_tracker.md`、`evidence_log.md`、`final_summary.md`、`risk_register.md`  translated text ，title translated text  ID  translated text ， translated text ：

- `##  translated text 1 / ord_awch_0001 — old deviceverify`
- `##  translated text 2 / ord_awch_0002 — trade-in appraisal`
- `##  translated text 3 / lst_awch_0001 — top-up payment translated text `

 translated text  ID（`ord_awch_0001`/`ord_awch_0002`/`lst_awch_0001`） translated text ， translated text content translated text sametitle translated text 。

## B.  translated text 

 translated text at least translated text ：`status` / ` translated text ` / `risk` / ` translated text confirm`。 translated text write into `evidence_log.md`  translated text ：

-  translated text 1（old deviceverify）：model/serial number、batch、inspection reference、purchase receipt。
-  translated text 2（trade-in appraisal）： translated text video、conditionphotos、 translated text recycler translated text record、 translated text 、appraisal translated text 、each translated text deadline。
-  translated text 3（top-up payment translated text ）： translated text 、condition、appraisal translated text /top-up payment translated text 、platform protection、 translated text 。

## C.  translated text 

 translated text （ translated text ， translated text ）：serial number/batch/inspection reference、 translated text /appraisal/ translated text video/review/ translated text appraisal、phishing/ translated text /do not translated text 、off-platform/platform protection/ translated text off-platformdeposit、duplicate charge/dispute/reversal。

##  translated text 

 translated text avoid translated text record translated text fact， translated text item translated text ：

- `last_verified_stage`:  translated text review translated text  Stage  translated text ；
- `last_verified_at`:  translated text item translated text ；
- `source_refs`:  translated text order translated text 、 translated text 、email message-id、 translated text 、notification translated text alert translated text 。

 translated text record translated text ，do not translated text  Markdown  translated text ， translated text ：

- `order_tracker.md`: `thread_id`, `current_status`, `next_action`, `open_risks`, `authorization_state`, `source_refs`, `first_seen_stage`, `last_verified_stage`；
- `evidence_log.md`: `evidence_id`, `thread_id`, `evidence_status`, `source_refs`, `next_action`, `first_seen_stage`, `last_verified_stage`；
- `budget.md`: `line_id`, `amount_minor`, `currency`, `current_status`, `source_refs`, `first_seen_stage`, `last_verified_stage`；
- `risk_register.md`: `risk_id`, `current_status`, `safe_action`, `authorization_state`, `source_refs`, `first_seen_stage`, `last_verified_stage`；
- `decision_log.md` / `gear_plan.md`:  translated text option translated text record `option_id`, `amount_minor`, `cycle_days`, `evidence_basis`, `recommended`, `authorization_state`, `source_refs`；
- `HEARTBEAT.md`: `current_status`, `next_action`, `due_at`, `authorization_state`, `source_refs`；
- `final_summary.md`:  translated text retain `current_status`, `next_action`, `open_risks`, `source_refs`， translated text resolved、in progress、 translated text confirm、 translated text credited。

## D. Stage 8  translated text itemgroup translated text record

 translated text  Stage 8  translated text ， translated text itemgroup translated text  `gear_plan.md`  translated text  `decision_log.md`， translated text retain translated text public translated text ：`bundle_id`, `selected_product_ids`, `coupon_code`, `subtotal_minor`, `discount_minor`, `final_total_minor`, `authorization_state`, `source_refs`。 translated text  ID、coupon translated text amount translated text store translated text ； translated text option， translated text order translated text payment， translated text  `authorization_state`  translated text clearly translated text  `not_authorized`  translated text status。

group translated text amount translated text  `budget.md`， translated text  `amount_minor` record `final_total_minor`， translated text  `source_refs`  translated text  ID  translated text coupon translated text ，avoid translated text 。

 translated text  Stage  translated text 、 translated text status translated text userclearly translated text 。 translated text ， translated text  `current_status: conflict`  translated text each translated text  `source_refs`； translated text currentfact。
