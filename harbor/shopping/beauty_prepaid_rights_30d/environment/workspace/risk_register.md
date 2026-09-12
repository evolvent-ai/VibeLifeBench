# Risk register

template_state: uninitialized

- risk: contract_or_card_identity_mismatch
  status: open
  trigger: product, SKU, credentials, contract, or balance conflict
  mitigation: cross-check ecommerce details and original payment records
  owner: Nora Shen
  next_review_stage: 2
- risk: service_evidence_deadline
  status: open
  trigger: platform evidence deadline or merchant objection
  mitigation: retain visit video, problem photos, ticket, chat, and independent review
  owner: Nora Shen
  next_review_stage: 15
- risk: phishing_or_off_platform_deposit
  status: open
  trigger: refund-and-tax email, WeChat deposit, or platform bypass
  mitigation: do not click or pay; use official app and platform protection
  owner: Nora Shen
  next_review_stage: 12
