# li_wei_may

Personal + Work calendar snapshot for the benchmark.

## What this env represents

- **User**: `usr_li_wei` (Li Wei, a Shanghai-based individual customer).
- **Reference date**: 2026-04-17. Events created after this cutoff are
  delivered by the world-controller when their source event fires.
- **Timezone**: `Asia/Shanghai` (`+08:00`) throughout.

## Calendars

| calendar_id    | name      | color   | is_primary |
| -------------- | --------- | ------- | ---------- |
| `cal_000001`   | Personal  | #4285F4 | yes        |
| `cal_000002`   | Work      | #0B8043 | no         |

## Highlights (15 seeded events)

### Family / personal (Personal)

| event_id        | when           | summary                                    |
| --------------- | -------------- | ------------------------------------------ |
| `evt_00000001`  | 5/8 18:30      | Momtranslated content (Mom's birthday dinner)           |
| `evt_00000002`  | 5/12 09:00     | translated contentDadtranslated content (Cardiology follow-up)        |
| `evt_00000003`  | 4/22 19:00     | translated content                             |
| `evt_00000004`  | 4/18 09:00     | translated content                                     |
| `evt_00000015`  | 4/10 08:00     | translated content (already past)                    |

### Recurring (Personal)

| event_id        | rule                                       | starts on  | first occurrence |
| --------------- | ------------------------------------------ | ---------- | ---------------- |
| `evt_00000005`  | `FREQ=WEEKLY;BYDAY=TH;UNTIL=20261231`      | 2026-04-02 | Thu 19:00 yoga   |
| `evt_00000006`  | `FREQ=WEEKLY;BYDAY=WE;UNTIL=20260831`      | 2026-04-01 | Wed 07:00 swim   |

### Recurring (Work)

| event_id        | rule                                       | starts on  | first occurrence |
| --------------- | ------------------------------------------ | ---------- | ---------------- |
| `evt_00000007`  | `FREQ=WEEKLY;BYDAY=MO;UNTIL=20261231`      | 2026-04-06 | Mon 09:00 sync   |
| `evt_00000008`  | `FREQ=WEEKLY;BYDAY=FR;UNTIL=20261231`      | 2026-04-03 | Fri 16:00 1:1    |

### One-off work events

| event_id        | when            | summary                          |
| --------------- | --------------- | -------------------------------- |
| `evt_00000009`  | 4/21 14:00      | Q2 Planning Review               |
| `evt_00000010`  | 4/29 10:00      | Customer Interview - Acme        |
| `evt_00000011`  | 5/6 15:00       | Internal All-Hands               |

### Japan trip block

| event_id        | when                        | summary                          |
| --------------- | --------------------------- | -------------------------------- |
| `evt_00000012`  | 2026-05-15 → 2026-06-04     | Japan20translated content (Personal cal)  |
| `evt_00000013`  | 2026-05-15 → 2026-06-04     | OOO - Japan Trip (Work cal)      |
| `evt_00000014`  | 5/11 14:00                  | translated content / pick up Japan visa      |

Recurring weekly events are stored as a single parent row with an `RRULE`
in `recurrence_rule`. The current server does not materialize child rows;
`list_events` returns the parent row directly when the window overlaps its
`start_dt`.

## How to load

```bash
calendar-mock \
  --env ../../envs/calendar/li_wei_may \
  --host 0.0.0.0 --port 8000
```

Docker:

```bash
docker run --rm -p 8000:8000 \
  -v "$PWD/envs/calendar/li_wei_may:/env-seed:ro" \
  vibe-agent-benchmark/calendar_mock:latest
```
