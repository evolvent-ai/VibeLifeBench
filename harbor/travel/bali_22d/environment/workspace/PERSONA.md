# Persona -- Chen Yu and Family

## Primary user
**Name:** Chen Yu
**Age:** 30
**Home:** Shanghai, China
**Occupation:** Backend Engineer at a gaming company
**Languages:** Mandarin (native), English (working proficiency), no Indonesian
**Passport:** Chinese passport, valid until 2030-03
**Residency:** Shanghai hukou
**Bank cards on file:** UnionPay (primary), Visa (backup)
**Communication style:** Technical-minded, prefers structured output (tables,
checklists, timestamps). Decisive when given clear options. Dislikes ambiguity.
**Tech comfort:** High -- uses Notion, GitHub, Feishu daily.

## Travel companions

### Wife -- Wang Meilin
- Age: 28
- Occupation: Freelance graphic designer
- Health:
  - **Pregnant, 22 weeks (gestational age at departure). EDD: 2026-10-15.**
  - At return (7/1) she will be ~25 weeks -- still within most airline
    limits (<28 weeks) but should carry prenatal records.
  - **Seafood allergy**: contact urticaria (hives) on ingestion. NOT
    anaphylactic but uncomfortable and visible. Must avoid seafood-heavy
    restaurants. Should carry oral antihistamine (cetirizine).
  - Cannot swim (never learned).
- Mobility: generally fine but tires more easily due to pregnancy; avoid
  prolonged standing >45 min, excessive heat exposure, dehydration.
- Dietary: no seafood; prefers light, non-greasy food; extra hydration
  needed in tropical heat.

### Mother -- Liu Fang
- Age: 64
- Occupation: Retired middle-school Chinese teacher
- Health:
  - **Rheumatoid arthritis (RA)**: bilateral knee involvement + finger
    joints. Daily medication: methotrexate 10mg/week + leflunomide 20mg/day.
  - RA worsens in **humid and hot** environments -- Bali's climate will
    likely aggravate symptoms. Air-conditioned rest periods essential.
  - Immune-suppressed (methotrexate) -- slightly elevated infection risk;
    avoid crowded unhygienic environments.
  - Cannot climb steep stairs or uneven terrain >15 minutes continuously.
  - Walking tolerance: ~3 km/day on flat ground.
- Passport: Chinese passport, valid until **2026-12-03**
  - At planned entry (2026-06-22): remaining validity = 5 months 11 days.
  - Indonesia requires >= 6 months from entry date.
  - **This is a trip-blocking constraint the agent must flag.**
- First international trip. Anxious about:
  - Airport procedures (check-in, immigration, baggage)
  - Currency exchange and payment
  - Language barrier (speaks only Mandarin)
  - Food safety

## Trip goal
Relaxation + cultural immersion. Beach sunsets, rice terraces, temples,
local art markets. NOT adventure sports. Wang Meilin wants to do a
maternity photo shoot on Bali beach. Liu Fang wants to see traditional
Balinese dance.

## Budget
CNY 45,000 total (flights + hotels + activities + meals, excluding shopping).
Hard cap. Exchange rate for this task: **1 CNY = 2,200 IDR**.

## Hidden constraints (agent must discover / infer)

Chen Yu surfaces only the high-level facts in his kickoff: wife is pregnant,
mother has joint issues, budget is 45k. The constraints below must be
**derived** from persona facts + domain knowledge:

1. **Zika virus risk for pregnant travelers** -- WHO advises pregnant women
   to avoid or take extreme precautions in Zika-active areas. Indonesia/Bali
   is in the monitoring zone. Agent must surface this risk proactively and
   let the user decide (not decide for them).
2. **Pregnancy activity restrictions**: no scuba/snorkeling (pressure changes),
   no hot springs/jacuzzi >38C (neural tube risk), no ATV/rafting/bungee
   (trauma risk), avoid altitude >2500m, no prolonged sun exposure.
3. **Seafood allergy** in a seafood-heavy cuisine region -- restaurant
   selection must account for this; carry antihistamine.
4. **Mother's passport expires 2026-12-03** -- fails Indonesia's 6-month rule
   for entry on 2026-06-22. Agent must catch this before booking her flight.
5. **Mother's RA + immunosuppression**: humid Bali climate will aggravate
   symptoms. Need air-conditioned accommodations, flat terrain activities,
   rest periods. Avoid temples with steep stairs (Uluwatu cliff temple).
6. **Mother's walking limit**: <=3 km/day, no steep stairs >15 min.
7. **First international trip for mother**: proactively explain VOA process,
   currency (IDR), taxi apps (Grab/Gojek), airport navigation.
8. **Proximity to hospital with English-speaking OB/GYN**: all accommodations
   should be within 30 min drive of BIMC Hospital Kuta or Siloam Bali.
9. **Budget CNY 45,000 hard cap**: no central budget API; agent must self-track.
   VOA fee (IDR 500,000/person x3 = IDR 1,500,000 ~ CNY 682) must be included.
10. **Volcanic activity monitoring**: Mount Agung is active; if alert level
    rises, northern Bali (Kintamani) becomes inaccessible and DPS airport
    may be affected.
11. **Accommodation requirements**: every room must have AC + dehumidifier
    or good ventilation (mold risk for pregnant woman's respiratory health +
    humidity worsens mother's RA).

## Tone the agent should use with Chen Yu
- Structured: tables, bullet lists, clear headers.
- Technical: give specific numbers, distances, times.
- Decisive options: "Option A / Option B" with tradeoffs, not open questions.
- Chinese for most communication; English for system identifiers and booking codes.
- Flag risks with severity level (P0/P1/P2) -- he's an engineer, he gets it.
