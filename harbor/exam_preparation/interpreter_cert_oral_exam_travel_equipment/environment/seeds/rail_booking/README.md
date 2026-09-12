# rail_booking env

## sessiontranslated business text

translated business text `interpreter_cert_oral_exam_travel_equipment` of Hangzhoutranslated business textNanjinghigh-speed railcandidateandremaining seatschange。date rangefor 2026-08-01 translated business text 2026-08-22，translated business textarea Asia/Shanghai。

## keyobject

keyobjecttranslated business textreviewerverify，includingofficialregistration/changeemail、equipmentproduct、equipmentdelivery logistics、exam siteplace、refundableaccommodation、high-speed railcandidate、health metricandauthorizationmaterials。agent translated business textfromthis README readtranslated business text，translated business text MCP toolquery。

## and task/rubric ofrelationship

rubric translated business textreadtooltranslated business text、mock aftertranslated business textstatus、workspace JSON、emailtranslated business text/calendar/Notion translated business textpersistentevidence；translated business text README translated business text agent translated business text。

## status and amount conventions

amountaccording to minor unit orservicetranslated business textfieldprevails；datetranslated business textfor ISO or YYYY-MM-DD；order、bookingandticketingtranslated business textstatusunauthorizedbeforetranslated business textkeepemptyor pending。

## translated business text row count translated business text

| table | istranslated business textcore | initial row count | dependency/check/check | interference strategy | meets target |
|---|---|---:|---|---|---|
| `train_offers` | is | 225 | translated business textcandidate、refundabletranslated business text、remaining seats mutation andunauthorizedticketingtranslated business textline | similardate、similarobject、old/new status、ad noiseandpolicy-violating candidate；correct evidencestilltranslated business textofficial/authorization/statusuniquely determined by cross-check | is |
| `student_profiles` | translated business text | 1 | supportingconfiguration/foreign key/statustranslated business text | similardate、similarobject、old/new status、ad noiseandpolicy-violating candidate；correct evidencestilltranslated business textofficial/authorization/statusuniquely determined by cross-check | is |
| `train_status` | is | 225 | translated business textbeforetranslated business textrefreshtraintranslated business textstatus | similardate、similarobject、old/new status、ad noiseandpolicy-violating candidate；correct evidencestilltranslated business textofficial/authorization/statusuniquely determined by cross-check | is |

## this roundtranslated business text

2026-07-03 translated business textnot yetadjustmentthis env of `init.sql`。translated business textof row count andtranslated business text；coretranslated business textstilltranslated business textordertranslated business text，translated business text。keytraintranslated business textretainsimilartranslated business text、remaining seatschange、refundable/nonrefundable、arrivaltranslated business textandstatustranslated business text，correct evidencestill needstranslated business textuserrefundablerequirement、exam sitetranslated business text、aftertranslated business text offer/status and agent authorizationpending confirmationrecordjointly established。

## loadingand smoke test

servercold starttranslated business textloading init.sql；availabletranslated business text list/search/get toolreadkeyobject，translated business textsilent mutation attranslated business textstatus。

## data source

allforsyntheticdata，withouttranslated business textpersonaltranslated business text、translated business textortranslated business textclienttranslated business text。
