# labor_dispute_2026/ — labordispute (labor dispute) research corpus

A synthesized Chinese legal-research corpus for a English text (litigation prep)
benchmark task. All party names are anonymized (English text/English text style); all judgment
text is original/synthesized and statute text is simplified public-domain-style
(Labor Contract Law / Labor Law are public domain). The server has **no clock** — the
reference date for the scenario is **2026-05-20** (task-level only). State
changes mid-task arrive as out-of-band SQL mutations.

## What it represents

`usr_li_wei` (li.wei@gmail.com) was dismissed by his employer citing
"English textadjustment" without 30-day written notice, and is researching precedent to
prepare a laborarbitration/litigation. He has already saved 2 cases with notes.

## Contents

- **6 courts / arbitrationEnglish text** (`courts`): ShanghaiEnglish text/English textcourt, ShanghaiEnglish text, ShanghaiEnglish text,
  BeijingEnglish textcourt, English textlaborarbitrationEnglish text.
- **2 statutes** (`statutes`):
  - `stat_lcl` — English textLabor Contract Law (Labor Contract Law), in force, 10 key articles.
  - `stat_ll` — English textLabor Law (Labor Law), in force, 4 key articles.
- **14 statute articles** (`statute_articles`), e.g. `art_lcl_082`
  (English textsalary), `art_lcl_087` (unlawful terminationEnglish text), `art_lcl_047`
  (English textcompensationEnglish text), `art_ll_044` (overtime pay).
- **18 judgments** (`cases`, `case_001`–`case_018`) spanning unlawful termination /
  overtime pay / double wage for no written contract / economic compensation / non-compete / English text etc.,
  each with English text(English text)/cause/facts/judgmentreasoning/judgmentEnglish text/rulingEnglish text/outcome/keywords.
- **29 citations** (`citations`) linking cases → statute articles, plus a few
  case → case references.
- **2 seeded saved cases** (`saved_cases`) for `usr_li_wei` with notes:
  `saved_seed_001` → `case_001`, `saved_seed_002` → `case_016`.

## Key object IDs

| What | ID |
|------|----|
| User | `usr_li_wei` |
| Closest precedent ("English textadjustment" unlawful termination, 2N) | `case_001` |
| Labor Contract Law statute | `stat_lcl` |
| English textsalary article | `art_lcl_082` |
| unlawful terminationEnglish text article | `art_lcl_087` |
| English textcourt | `court_sh_pudong` |
| English textlaborarbitrationEnglish text | `arb_sh_pudong` |

## Counters

`saved_seq=2`, `citation_seq=29` — so newly-issued IDs (`saved_000003`, …)
don't collide with seed IDs.

## How it's loaded

```
legal-search-mock --host 0.0.0.0 --port 8000 \
                  --env <repo>/envs/legal_search/labor_dispute_2026
```

The server creates `runtime.db`, applies the bundled schema, then runs this
`init.sql` (pure INSERTs). `runtime.db` is git-ignored and never written back
to the host.
