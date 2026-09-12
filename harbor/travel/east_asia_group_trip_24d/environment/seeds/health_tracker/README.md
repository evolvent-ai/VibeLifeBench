# health_tracker_mock — east_asia_group_trip_24d

## Record identifiers

| Item | ID | Notes |
|------|----|-------|
| Li Ting blood pressure   (  ) | `bp-2604010800-nuznzvo` | 132/86, 2026-04-01 |
| Li Ting blood pressure   (  ) | `bp-2605290800-kyqiecg` | 136/89, 2026-05-29 |
|   blood pressure   record | `bp-2606060700-36ra2gu` | equipment   ；  ≥140，   list_health_alerts |
| Chen Yu      | `step-2605010730-rkwftwd` | — |
| Wang Hao      | `weight-2605010800-5chrzhk` |   : g |
| Zhao Min      | `metric-2605010700-pdje3gs` |   : minutes |
| Li Ting      | `act-walk-2605021800-iwoveby` | 2026-05-02 |
| Chen Yu      | `act-run-2605020700-h24hnch` | 2026-05-02 |

##     

|    | record  |
|------|--------|
| Li Ting blood_pressure (  ) | 16 |
| Li Ting steps/heart_rate/sleep | 38 |
| Chen Yu steps/heart_rate/sleep | 32 |
| Wang Hao steps/heart_rate/weight | 30 |
| Zhao Min steps/heart_rate/sleep | 32 |
| **metrics   ** | **148** |
| Li Ting workouts | 8 |
| Chen Yu workouts | 8 |
| **workouts   ** | **16** |

## blood pressure    

blood pressure    : **systolic ≥ 140**

       systolic    127–137，    `list_health_alerts`。

  blood pressure       record ， `list_health_alerts(user_id="usr_li_ting")` return  。

```sql
INSERT INTO metrics VALUES (
  'bp-2606060700-36ra2gu','usr_li_ting','blood_pressure',
  158.0,'158/96','mmHg','2026-06-06T14:00:00+08:00'
);
```

## Schema（   ）

- `metrics(metric_id, user_id, type, value, value_text, unit, recorded_at)`
- `workouts(workout_id, user_id, type, duration_min, calories, distance_m, started_at)`
