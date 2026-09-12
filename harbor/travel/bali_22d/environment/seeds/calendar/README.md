# chen_yu_jun

Personal + Work calendar snapshot for the Bali 22-day benchmark task.

## What this env represents

- **User**: `usr_chen_yu` (Chen Yu, Shanghai-based backend engineer).
- **Reference date**: 2026-06-01. Events span May-Jul 2026.
- **Timezone**: `Asia/Shanghai` (`+08:00`) throughout.

## Calendars

| calendar_id | name | color | is_primary |
|-------------|------|-------|------------|
| cal_000001 | Personal | #4285F4 | yes |
| cal_000002 | Work | #0B8043 | no |

## Events (~14 seeded)

### Personal
- Wife's prenatal checkup (6/3)
- Anniversary dinner (5/30)
- Bali trip block (6/10 -> 7/1)
- Mother's flight arrival (6/22)

### Work (recurring)
- Weekly standup Mon 10:00
- Sprint review Fri 15:00
- Game launch deadline (6/8)

## How to load

```bash
calendar-mock \
  --env ../../envs/calendar/chen_yu_jun \
  --host 0.0.0.0 --port 8000
```
