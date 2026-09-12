# Persona — Li Wei and Family

## Primary user
**Name:** Li Wei (Li Wei)
**Age:** 32
**Home:** Shanghai, China
**Occupation:** Product Manager at a SaaS startup
**Languages:** Mandarin (native), English (business-fluent), Japanese (~N5)
**Passport:** Chinese passport, valid until 2029-10
**Residency:** Shanghai hukou
**Bank cards on file:** UnionPay (primary), Visa (backup)
**Communication style:** Direct, asks follow-up questions when uncertain,
prefers bullet-point itineraries over prose.
**Tech comfort:** High — uses Notion, Feishu, Google Calendar daily.

## Travel companions (encoded into persona for multi-user handling)

### Father — Li Jianguo (Li Jianguo)
- Age: 65
- Health: **Type-II diabetes, insulin-dependent**. Must carry:
  - 20-day insulin supply + spare
  - Glucose meter, strips
  - Glucagon rescue kit
  - **Doctor's letter (Chinese + English)** for customs
- Dietary: no deep-fried; low-sugar; **cannot skip meals** (hypoglycemia risk)
- Mobility: walking tolerance ~4 km/day; avoid >30 min continuous stairs
- Passport: valid until 2028-06
- First international trip. Anxious about airport procedures.

### Mother — Zhang Lan (Zhang Lan)
- Age: 62
- Health: Generally healthy; mild hypertension, daily medication
- **Passport: valid until 2026-11-08**. It remains valid through the planned
  2026-05-16 return, but the post-trip margin is short enough to justify a
  documented check with the current official channel, operating airline, and
  any transit-country rule. Do not invent an automatic rejection rule.
- Mobility: fine, energetic
- Dietary: prefers vegetarian-leaning, dislikes raw fish

## Trip goal
Cultural sightseeing with parents. Tokyo classics, Hakone onsen, Kyoto
temples, Osaka food, one Nara day trip. NOT shopping-driven.

## Budget
¥60,000 total (flights + hotels + activities + meals, excluding shopping).
Hard cap.

## Hidden constraints (agent must discover / infer)

Li Wei surfaces only the high-level facts in her kickoff message — that her
father is 65 and insulin-dependent, that her mother is 62, that the parents
have never flown internationally, and that the budget is ¥60,000 for
2026-05-01 → 05-16 with Tokyo / Kyoto / Osaka in mind. The constraints below
are what the agent must **derive** from those facts (plus Japan-specific
domain knowledge and the persona files); Li Wei does not volunteer them and
does not know to.

1. Mother's passport expires 2026-11-08 and remains valid for the full trip.
   Japan's official guidance does not publish a universal six-month passport
   rule; the agent must still surface the short margin and verify the current
   official channel, operating airline, and any transit requirement before a
   non-refundable purchase.
2. Insulin and ancillary diabetes supplies should stay accessible in carry-on
   baggage under the operating carrier/security rules. A bilingual clinician
   letter, prescription copy, quantities, and manufacturer storage guidance
   are practical evidence; verify the current import procedure rather than
   claiming one document is universally mandatory.
3. Diabetic father must not skip meals — itinerary cannot have >3h gaps over
   scheduled meal times (hypoglycemia risk).
4. Walking load must stay ≤4 km/day with no >30-min continuous stair climbs —
   agent must sequence sightseeing within this budget.
5. "First international trip" for the parents implies a teaching role —
   proactively walk them through airport procedure, customs forms, SIM +
   payment setup, JR IC cards vs cash etiquette, and what an "international
   arrivals" flow looks like. Don't assume they know.
6. Agent must track cumulative spend against the ¥60,000 cap and warn
   progressively (no central budget API exists — see AGENTS.md expense_log).
7. Mother dislikes raw fish — restaurant picks should default to cooked /
   grilled options.
8. Insulin storage must follow the exact product label. Confirm a workable
   non-freezing storage arrangement with each hotel before booking; a minibar
   is not automatically suitable medication storage.
9. Shanghai ↔ Japan time zone offset is +1h only, but meal timing for the
   diabetic father still needs an explicit adjustment plan for D1 arrival
   and the return day.
10. UnionPay acceptance in Japan is patchy outside Tokyo — agent should
    suggest a cash drawdown at KIX/NRT ATMs on arrival.

## Tone the agent should use with Li Wei
- Concise bullet summaries first, detail below if asked.
- When confidence is low, ask before acting (pro-active clarification is
  tested explicitly).
- Use timestamps and "ETA" / "status" language — Li Wei is a PM and
  expects operational clarity.
