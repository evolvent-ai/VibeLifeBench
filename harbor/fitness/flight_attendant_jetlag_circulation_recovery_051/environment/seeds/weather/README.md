# weather env for flight_attendant_jetlag_circulation_recovery_051

## background note

background note“cabin attendantbackground notecross-time-zonebackground notelower-leg circulationmaintain”background note weather background notestatus。background note 2026-09-01 background note 2026-10-05，background note Asia/Shanghai。

## background note

- background noteLocation：Shanghai、Paris、NewYork、Singapore。
- mutation background noteShanghai 9 background note 17 background noteupdatebackground note、background note。
- background note：background noteweather。

## background note task/rubric background note

agent background note MCP background notefacts，background notetraining、background note、budget、privacybackground notereviewbackground notePersonal calendar、Notion background note workspace background note。mutation background note stage background note，checker background note、background noteevidencebackground note。

## statusbackground note

background note minor unit；calendarstatusbackground note confirmed/tentative/cancelled；background notestatusbackground note pending_payment/paid/shipped/delivered/completed/refund_requested/refunded/cancelled。

## background note smoke test

mock server background note init.sql。background note list/search/read background noteconfirmationbackground note。

## background notesource

background note，background note；background note，background note。

## background note

| background note | background note | background note | background note/check | background note | background note |
|---|---|---:|---|---|---|
| `daily_weather` | background note | 320 | background noteweather、background notereview / `chk_s17_weather_indoor_alt`, `chk_s27_delay_reschedule`, `chk_s29_final_review_complete` | background noteweatherbackground note，background noteindoor alternative | background note |
| `hourly_weather` | background note | 384 | background noteRest windowbackground note / `chk_s17_weather_indoor_alt`, `chk_s27_delay_reschedule` | background noteweatherbackground note，background notetrainingbackground note | background note |
| `daily_aqi` | background note | 320 | background noteindoor alternative / `chk_s17_weather_indoor_alt` | AQI background noteweatherbackground note，background note | background note |
| `locations` | background note | 4 | background note | background noteweatherbackground note，background note | background note |
| `climate_profiles` | background note | 4 | background note | background note，background note daily/hourly weather background note AQI background note | background note |
