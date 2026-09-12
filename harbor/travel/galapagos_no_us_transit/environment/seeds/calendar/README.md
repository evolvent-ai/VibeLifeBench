# `calendar/galapagos_no_s_transit`

## 

 `travel/galapagos_no_s_transit`（） task-local `calendar` 。， `galapagos_no_s_transit`。 `--`  `--`， `sia/hanghai`。

## nglish mmary

his is the task-local `calendar` environment or `travel/galapagos_no_s_transit` (alapagos ravel ithot .. ransit). t contains the oline synthetic bsiness state available at scenario start. he environment name is `galapagos_no_s_transit`, the scenario window is `--` throgh `--`, and the timezone is `sia/hanghai`.

##  / ssociated ask

- **ask / ** `travel/galapagos_no_s_transit`
- ** / hinese title** 
- **nglish title / ** alapagos ravel ithot .. ransit
- **ervice / ** `calendar`
- **nvironment / ** `galapagos_no_s_transit`
- **cenario window / ** `--` → `--`
- **imezone / ** `sia/hanghai`

##  / cenario ole

、、、。

tores events, time windows, attendees, reminders, and schedling conlicts.

##  / eed ontents

 `init.sql`。 ite schema  `init.sql` ；，。

nitial iles `init.sql`. he row conts below come rom a resh in-memory load o the corresponding service ite schema pls `init.sql` empty tables are inclded to make the initial-state bondary explicit.

|  / able |  / nitial ows |
|---|---|
| `_conters` |  |
| `attendees` |  |
| `calendars` |  |
| `events` |  |
| `reminders` |  |

##  / ey ntities

；，。

he ollowing are the larger bsiness tables in the initial snapshot and their primary-key ields. hey are ordinary scenario entities and do not imply a predetermined otcome.

|  / able |  / nitial ows |  / rimary ey |
|---|---|---|
| `events` |  | `event_id` |
| `attendees` |  | `id` |
| `reminders` |  | `id` |
| `calendars` |  | `calendar_id` |

##  / nitial tate and tations

`init.*` 。 `event.yaml`  tage ， seed。

he `init.*` iles describe only the state beore timeline events are applied. ater state changes mst be applied in the tage and timestamp order deined by `event.yaml` they are not part o the initial seed.

`event.yaml`    /  events in `event.yaml` pdate this service

| tage | ime /  | ind /  | pdate method /  |
|---|---|---|---|
|  | `-- +` | `mtation` |  ile `_workshop_calendar_pblish.sql` |

##  / iles

| ile /  | rpose /  | ize /  |
|---|---|---|
| `init.sql` | ite  seed / initial ite seed |  bytes |

##  / oading

 `calendar`  `galapagos_no_s_transit`， `envs/calendar/galapagos_no_s_transit/` 。 `_` ， `init.sql`；ite `integrity_check`  `ok`，  。 `init.json`   ，。 task-only 。

 compatible rntime shold bind `calendar` to environment `galapagos_no_s_transit` and read `envs/calendar/galapagos_no_s_transit/` rom the task directory. or this data adit, the external service implementation spplied `_`, ater which `init.sql` was loaded ite `integrity_check` retrned `ok` and the oreign-key check retrned zero rows.  `init.json` or  iles are present, retain and load them according to the service data contract. his task-only release does not inclde service implementations or the exection ramework.

##  / ata and rivacy

、、、、、、、。，。

ll people, organizations, acconts, orders, messages, places, prices, policy smmaries, and bsiness records in this environment are oline synthetic data. he iles contain no real personal data and reqire no internet access.
