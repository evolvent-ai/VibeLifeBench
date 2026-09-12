# japan_20d_may

Visa / entry-requirement / advisory snapshot for the Japan 20-day
(May 2026) benchmark task.

## What this env represents

- **Scenario**: Catalog data for the visa-and-advisory service used by
  Li Wei's 20-day Japan trip 2026-04-28 to 2026-05-22, plus two
  staged changes seeded inactive.
- **Anchor**: 2026-04-17 (day_index = 0). Catalogue `updated_at`
  timestamps fall within 30 days of this anchor.
- **Currency**: visa fees stored in MAJOR units in their respective
  currencies (CNY / USD / GBP / EUR).

## Key entities seeded

- **visa_products**: 18 rows — Japan transit / business / eVisa / single
  / multi visas for CN nationals, plus equivalent products for US / GB
  / EU / KR / SG / TH / VN / AU / NZ / IN / MX / BR / ZA passport
  holders covering the most common 2026-Q2 routes.
- **entry_requirements**: 211 rows — 14 nationalities x 15 destinations
  covering tourism (primary), business, and select transit purposes.
  Rules reflect recalled 2024-2025 real-world policy extrapolated to
  2026-Q2 (visa-required flag, allowed_stay_days, passport_validity
  months, docs_needed JSON, notes).
- **advisories**: 27 rows — 2026-Q2 advisory snapshot.
  - level 1 (normal): most destinations.
  - level 2 (caution): a handful of regional flags.
  - level 3 (reconsider) / 4 (do not travel): a few hot-spots.
- **scripted_events**: 2 rows — pending staged changes (advisory level
  change, entry rule update). The current Terrarium task applies these
  through explicit `event.yaml` mutations.

No `visa_applications` rows are seeded — agent drives the full
draft → upload → submit flow at runtime.

## How to load

```bash
# direct, from servers/visa_and_advisory_mock/
visa-and-advisory-mock \
  --env ../../envs/visa_and_advisory/japan_20d_may \
  --host 0.0.0.0 --port 8000
```

```bash
# docker, from repo root after building vibe-agent-benchmark/visa_and_advisory_mock:latest
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/visa_and_advisory/japan_20d_may:/env-seed:ro" \
  vibe-agent-benchmark/visa_and_advisory_mock:latest
```

The Docker entrypoint copies `/env-seed` to `/env`; the server creates
`/env/runtime.db` and applies `/env/init.sql` on cold start.
