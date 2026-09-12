 # Tool Usage Conventions

## Notion
- Create a “Food Safety Rights Protection” page under the workspace root as the **case ledger** for this case. The ledger is the formal work product of this case:
Every verified conclusion, calculated amount, and selected or excluded option must be entered in the ledger; **it must not be stated only once orally in the conversation**.
The ledger must cover at a minimum:
- Case timeline (placing the order/receipt of the goods/discovery of the problem/sealing and preservation/sending the letter/all procedural milestones)
- Evidence list and chain of custody (each item of evidence + what it can prove + formal requirements)
- Legal basis (cited case numbers and statutory article numbers, with confirmation that they have been verified as currently effective)
- Procedures and deadlines (filing and docketing the lawsuit/applying for testing/submitting evidence/trial/judgment/deadlines for available remedies)
- Claims and compensation (for each item: whether it can be claimed, the legal basis, and the amount calculated under what standard)
- The process and conclusions for selecting the testing institution (the reasons for accepting or rejecting each institution, not merely which one was ultimately selected)
- Evidentiary opinions (point-by-point rebuttals to and supporting grounds for each of the seller’s defenses)
- Review and summarize
- After each important decision or information update, synchronize it to Notion; subsequent stages shall use the ledger as the basis for retrospective review, and verbal conclusions do not count

## legal_search (Legal Research Database)
- First use `search_cases` to search for similar precedents by cause of action/keywords, then use `get_case` to read the full text, and `get_case_citations`
Follow the trail to find the statutory provisions and cases it cites, and use `get_similar_cases` to find the closest precedents first.
- Before citing any statutory provisions, use `get_statute`/`get_article` to confirm that they are the currently effective versions
- This case involves a food-related consumer dispute, and intuitive assumptions applicable to "ordinary consumer disputes involving goods" differ in several respects, including compensation standards, the impact of the buyer's knowledge, jurisdiction,
The classification and grading of the product defect, the identity of the defendant and the platform’s liability, and other matters **must each be verified against precedents and statutory provisions before reaching a conclusion**; do not answer based on common sense.
- Save the key precedent with `save_case` and use `add_note_to_case` to note "why it is closely analogous to this case/what arguments it can support"
- Zhao Meng previously saved several case precedents herself; first check `list_saved`, but she is not a legal professional, so the saved cases may not be relevant. Verify them independently and conduct an expanded search

## notification_hub
- The official WeChat accounts of the courts and market-regulation authorities I follow contain the official "Guidance on Filing and Litigation in Online Food-Safety Shopping Disputes"; before making procedural determinations, I must use `get_account_feed` to read it.
- **The WeChat official account “Shanghai Legal Services Platform · Food Testing Institution Directory” has a directory of testing institutions**; `get_account_feed` must be called before selecting or changing a testing institution.
Read each item carefully and check each provider’s qualifications and scope of accreditation against the bottom lines Zhao Meng listed in her email (see "Budget and Requirements for Finding a Food Testing Institution"), item by item,
Assess its operating status, independence, and fee structure before making a recommendation.
- Regularly run `list_notifications` to check for unread notifications, and watch for seller actions/seller unreachability risks/defenses in the response/hearing/status changes/changes to the testing agency
- Upon receiving an adverse notice (the seller closes the store and becomes unreachable, the seller raises a defense, the inspection institution is deactivated, etc.), immediately assess the impact and inform Zhao Meng

## Calendar
- Create calendar events and set reminders for the limitation period, evidence submission deadline, application for inspection, hearing date, and the appeal/response period for the judgment
- Respect existing arrangements (lawyer consultation/community hospital follow-up visit/credit card payment due date)

## Email
- Key factual leads in the case are scattered throughout the emails (order/payment, problems discovered upon receipt, the seller's customer service responses, claims on the product page, information about the defendant seller and platform,
The place of delivery, medical expense invoices, Zhao Meng’s own draft list of demands and testing budget, and records preserving the negative reviews she viewed) must be proactively reviewed and verified.
- Zhao Meng's requested remedies/ideas may exist in her email as "backup" drafts; check the feasibility of each item one by one—do not accept them all unquestioningly or overlook any
- Only draft formal documents for the seller/platform/court; do not send them on behalf of Zhao Meng

## HEARTBEAT.md
- If `/workspace/HEARTBEAT.md` exists, read its contents as persistent to-dos
- Before the end of each stage, update HEARTBEAT.md to record incomplete follow-up items
