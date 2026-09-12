# `email/galapagos_no_s_transit`

## 

 `travel/galapagos_no_s_transit`（） task-local `email` 。， `galapagos_no_s_transit`。 `--`  `--`， `sia/hanghai`。

## nglish mmary

his is the task-local `email` environment or `travel/galapagos_no_s_transit` (alapagos ravel ithot .. ransit). t contains the oline synthetic bsiness state available at scenario start. he environment name is `galapagos_no_s_transit`, the scenario window is `--` throgh `--`, and the timezone is `sia/hanghai`.

##  / ssociated ask

- **ask / ** `travel/galapagos_no_s_transit`
- ** / hinese title** 
- **nglish title / ** alapagos ravel ithot .. ransit
- **ervice / ** `email`
- **nvironment / ** `galapagos_no_s_transit`
- **cenario window / ** `--` → `--`
- **imezone / ** `sia/hanghai`

##  / cenario ole

、、、。

tores mail olders, messages, threads, attachments, and drats.

##  / eed ontents

 `init.sql`。 ite schema  `init.sql` ；，。

nitial iles `init.sql`. he row conts below come rom a resh in-memory load o the corresponding service ite schema pls `init.sql` empty tables are inclded to make the initial-state bondary explicit.

|  / able |  / nitial ows |
|---|---|
| `_conters` |  |
| `accont_conig` |  |
| `attachments` |  |
| `drats` |  |
| `olders` |  |
| `messages` |  |
| `sent_log` |  |

##  / ey ntities

；，。

he ollowing are the larger bsiness tables in the initial snapshot and their primary-key ields. hey are ordinary scenario entities and do not imply a predetermined otcome.

|  / able |  / nitial ows |  / rimary ey |
|---|---|---|
| `messages` |  | `id` |
| `attachments` |  | `id` |
| `sent_log` |  | `id` |
| `olders` |  | `id` |
| `accont_conig` |  | `id` |

##  / nitial tate and tations

`init.*` 。 `event.yaml`  tage ， seed。

he `init.*` iles describe only the state beore timeline events are applied. ater state changes mst be applied in the tage and timestamp order deined by `event.yaml` they are not part o the initial seed.

`event.yaml`    /  events in `event.yaml` pdate this service

| tage | ime /  | ind /  | pdate method /  |
|---|---|---|---|
|  | `-- +` | `mtation` |  ile `_organizer_logistics_packet.sql` |
|  | `-- +` | `mtation` |  ile `_airline_weather_waiver_email.sql` |
|  | `-- +` | `mtation` |  ile `_reimbrsement_scope_email.sql` |
|  | `-- +` | `mtation` |  ile `_loyalty_name_mismatch.sql` |
|  | `-- +` | `mtation` |  ile `_entry_ee_notice_email.sql` |
|  | `-- +` | `mtation` |  ile `_payment_veriication_email.sql` |
|  | `-- -` | `mtation` |  ile `_hotel_prearrival_note.sql` |
|  | `-- -` | `mtation` |  ile `_workshop_schedle_shit_email.sql` |
|  | `-- -` | `mtation` |  ile `_receipt_bndle_email.sql` |

##  / iles

| ile /  | rpose /  | ize /  |
|---|---|---|
| `init.sql` | ite  seed / initial ite seed |  bytes |

##  / oading

 `email`  `galapagos_no_s_transit`， `envs/email/galapagos_no_s_transit/` 。 `_` ， `init.sql`；ite `integrity_check`  `ok`，  。 `init.json`   ，。 task-only 。

 compatible rntime shold bind `email` to environment `galapagos_no_s_transit` and read `envs/email/galapagos_no_s_transit/` rom the task directory. or this data adit, the external service implementation spplied `_`, ater which `init.sql` was loaded ite `integrity_check` retrned `ok` and the oreign-key check retrned zero rows.  `init.json` or  iles are present, retain and load them according to the service data contract. his task-only release does not inclde service implementations or the exection ramework.

##  / ata and rivacy

、、、、、、、。，。

ll people, organizations, acconts, orders, messages, places, prices, policy smmaries, and bsiness records in this environment are oline synthetic data. he iles contain no real personal data and reqire no internet access.
