# visa_and_advisory_mock — east_asia_group_trip_24d

## Key IDs

| Item | ID | Notes |
|------|----|-------|
| Japan  visa（single entry）| `vp_jp_tourist_single` | fee ¥8,000 JPY，5 business days |
| Japan  visa（5 multiple entry）| `vp_jp_tourist_multi5yr` | — |
| South Korea  visa（single entry）| `vp_kr_tourist_single` | fee ₩60,000，5 business days |
| South Korea  visa（multiple entry）| `vp_kr_tourist_multi` | — |
| **S16   ** | `KR` advisory |    level=1，mutation→level=2 |

## S16 Mutation   

```sql
UPDATE advisories
SET level=2,
    text='note：Seoul  occurred          ，please    。',
    last_updated='2026-06-06T08:00:00Z'
WHERE country_code='KR';
```

Agent    `get_advisory('KR')`      level=2， update     recommend  /  itinerary。

##     （      ）

|    |    |   |
|------|------|-----|
| CN→JP tourism | passport_validity_months | **6** |
| CN→KR tourism | passport_validity_months | **6** |
| JP advisory | level | **1** (  ) |
| KR advisory | level | **1→2** (S16 ) |

>          entry_rule   return `"source":"default_fallback"`，  INSERT   return `"source":"seeded"`。        ，recommend rubric     source   。

## Schema（  ）

```sql
entry_rules(id, nationality, destination, purpose, visa_required,
            allowed_stay_days, passport_validity_months, docs_needed, notes)
advisories(country_code, level, text, last_updated)
visa_products(product_id, nationality, destination, product_name, fee_minor,
              fee_currency, processing_days, validity_days, max_stay_days,
              entry_type, description)
```
