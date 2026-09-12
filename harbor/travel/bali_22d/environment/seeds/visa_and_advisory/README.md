# bali_22d_jun

Visa / entry-requirement / advisory snapshot for the Bali 22-day
(Jun-Jul 2026) benchmark task.

## What this env represents

- **Scenario**: Catalog data for Indonesia entry requirements for Chinese
  nationals, plus Zika and volcanic activity advisories.
- **Anchor**: 2026-05-28 (day 0).
- **Currency**: visa fees in IDR.

## Key entities seeded

- **visa_products**: Indonesia VOA (30 days, IDR 500,000), e-Visa options.
- **entry_requirements**: CN->ID tourism: VOA eligible, passport >=6 months,
  return ticket required.
- **advisories**:
  - Indonesia/Bali Zika monitoring zone (level 2)
  - Bali volcanic activity advisory (level 2, escalates via mutations)
  - Indonesia general (level 1)

## Critical for task

- Mother Liu Fang's passport expires 2026-12-03
- Entry date 2026-06-22: only 5 months 11 days remaining
- Indonesia requires >=6 months -- VOA will be REJECTED
- Agent must catch this from passport_validity_months=6 in entry_requirements

## How to load

```bash
visa-and-advisory-mock \
  --env ../../envs/visa_and_advisory/bali_22d_jun \
  --host 0.0.0.0 --port 8000
```
