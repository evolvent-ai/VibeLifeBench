"""Agent-causal, backend-bound checks for apartment_renovation_20d."""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import _helpers as H


@dataclass(frozen=True)
class StageSpec:
    file: str
    anchors: tuple[str, ...]
    groups: tuple[tuple[str, ...], ...]


SPECS = {
    0: StageSpec(
        "renovation_plan.md",
        ("2026-08-08", "August 8", "August 8"),
        (
            ("200000", "200,000", "CNY 200,000", "CNY 200,000"),
            ("20000", "20,000", "CNY 20,000", "CNY 20,000"),
            ("180000", "180,000", "CNY 180,000", "CNY 180,000"),
            ("68 square meters", "68 square meters", "68㎡"),
            ("two weeks", "14 days", "14 days"),
            ("renovation filing",),
            ("water-retention test",),
            ("electrical",),
            ("pending confirmation", "items to confirm"),
            ("person responsible",),
        ),
    ),
    1: StageSpec(
        "requirements_brief.md",
        ("older family member", "primary bathroom"),
        (
            ("primary bathroom",),
            ("separate wet and dry zones",),
            ("slip resistance",),
            ("child", "child", "four years old", "four years old"),
            ("low-VOC", "low-VOC"),
            ("U-shaped", "U-shaped"),
            ("3.2 meters", "3.2 meters"),
            ("weekend",),
            ("noise ban", "noisy construction", "noisy construction"),
            ("acceptance criteria", "acceptance criteria"),
        ),
    ),
    2: StageSpec(
        "contractor_comparison.md",
        ("past 30 days", "past 30 days", "contractor comparison", "contractor comparison"),
        (
            ("as of 2026-06-03", "2026-06-03"),
            ("rating", "review", "star rating"),
            ("credentials", "license", "qualifications"),
            ("quote", "price range"),
            ("schedule availability", "schedule", "available window"),
            ("risk", "complaint", "change order", "delay"),
            ("recommendation", "recommendation", "ranking"),
        ),
    ),
    3: StageSpec(
        "schedule.md",
        ("2026-06-06", "June 6", "June 6"),
        (
            ("site measurement",),
            ("morning", "09:00", "9:00", "10:00"),
            ("documents",),
            ("filing", "property management"),
            ("permitted noise hours", "noise ban"),
            ("load-bearing wall",),
            ("must not alter", "must not alter"),
        ),
    ),
    4: StageSpec(
        "budget_tracker.md",
        ("200000", "200,000", "CNY 200,000", "CNY 200,000"),
        (
            ("20000", "20,000", "CNY 20,000", "CNY 20,000"),
            ("180000", "180,000", "CNY 180,000", "CNY 180,000"),
            ("demolition",),
            ("electrical and plumbing work",),
            ("waterproofing",),
            ("masonry work",),
            ("carpentry",),
            ("painting",),
            ("primary materials",),
            ("lighting",),
            ("installation",),
            ("cleaning",),
            ("acceptance inspection",),
            ("filing",),
            ("debris removal",),
            ("estimated",),
            ("committed",),
            ("paid",),
            ("pending confirmation",),
            ("risk contingency", "contingency balance"),
        ),
    ),
    5: StageSpec(
        "risk_register.md",
        ("pm-rfi-0606", "renovation filing additional information request"),
        (
            ("additional information request", "needs_information"),
            ("valid electrician-certificate page", "electrician certificate"),
            ("signed demolition-and-alteration drawing", "demolition-and-alteration drawing"),
            ("debris-removal commitment",),
            ("do not demolish", "pause demolition"),
            ("structural work",),
            ("person responsible",),
            ("next step",),
        ),
    ),
    6: StageSpec(
        "material_decisions.md",
        ("large-format tiles", "tiles"),
        (
            ("U-shaped kitchen cabinets", "U-shaped kitchen cabinets", "cabinets"),
            ("low-VOC", "low-VOC"),
            ("stock",),
            ("lead time",),
            ("compatibility", "specification"),
            ("budget", "price"),
            ("substitution", "alternative"),
            ("recommendation", "recommendation"),
            ("pending confirmation",),
            ("not ordered", "no deposit placed", "unauthorized"),
        ),
    ),
    7: StageSpec(
        "inspection_checklist.md",
        ("pm-app-0608", "renovation filing approved", "renovation filing approved"),
        (
            ("additional information approved", "renovation filing approved"),
            ("site-access pass",),
            ("collect", "available for collection"),
            ("permitted noise hours",),
            ("load-bearing wall must not be altered", "load-bearing wall"),
            ("debris removal",),
            ("person responsible",),
            ("next step",),
        ),
    ),
    8: StageSpec(
        "contractor_comparison.md",
        ("18:00", "18:00 today", "today at 18:00"),
        (
            ("quote",),
            ("schedule availability",),
            ("hold",),
            ("deposit",),
            ("exit terms", "refund conditions"),
            ("safe to confirm now", "safe confirmation"),
            ("must wait", "pending confirmation"),
            ("SteadyHome",),
            ("168000", "168,000", "CNY 168,000", "CNY 168,000"),
            ("Chen Yu personally", "signed personally"),
            ("50400", "50,400", "CNY 50,400", "CNY 50,400"),
            ("paid personally", "paid personally"),
            ("written authorization",),
            ("start work", "notice to proceed"),
        ),
    ),
    9: StageSpec(
        "risk_register.md",
        ("nc-2026-0609-1602", "nighttime noise complaint"),
        (
            ("24 hours", "24 hours"),
            ("cutting",),
            ("rotary hammer",),
            ("nighttime",),
            ("suspend", "corrective work"),
            ("schedule",),
            ("site-access pass",),
            ("neighbor relations", "neighbors"),
            ("person responsible",),
            ("next step",),
        ),
    ),
    10: StageSpec(
        "inspection_checklist.md",
        ("residual-current protection", "electrical spot inspection"),
        (
            ("conduit",),
            ("fastening spacing",),
            ("failed",),
            ("corrective work",),
            ("reinspection",),
            ("do not close the wall", "pause wall closure"),
            ("person responsible",),
        ),
    ),
    11: StageSpec(
        "schedule.md",
        ("August 3", "August 3", "2026-08-03"),
        (
            ("August 8", "August 8", "2026-08-08"),
            ("hinge", "cabinet hardware"),
            ("delayed by 9 days", "delayed by 9 days"),
            ("5 days earlier", "5 days earlier"),
            ("critical path",),
            ("recalculate", "reschedule"),
            ("safety acceptance inspection",),
            ("low-VOC", "low-VOC"),
            ("ventilation",),
            ("must not skip", "do not skip"),
        ),
    ),
    12: StageSpec(
        "risk_register.md",
        ("prolonged rain", "high humidity", "humid conditions"),
        (
            ("waterproofing",),
            ("coating membrane",),
            ("wall putty",),
            ("carpentry",),
            ("moisture content", "humidity"),
            ("extend", "defer", "adjust"),
            ("review again",),
            ("person responsible",),
            ("next step",),
        ),
    ),
    13: StageSpec(
        "inspection_checklist.md",
        ("initial water-retention test", "primary-bathroom threshold"),
        (
            ("24 hours", "24 hours"),
            ("moisture content",),
            ("increase", "dampness"),
            ("threshold water stop", "threshold"),
            ("pipe-penetration sealing", "pipe penetration"),
            ("pause tile installation", "do not install tile"),
            ("48 hours", "48 hours"),
            ("repeat", "review again"),
            ("failed", "open"),
        ),
    ),
    14: StageSpec(
        "schedule.md",
        ("next two weekends", "two weekends"),
        (
            ("cutting",),
            ("drilling",),
            ("hammering",),
            ("suspend", "noise ban"),
            ("measurement",),
            ("cleaning",),
            ("weekday", "reschedule"),
            ("person responsible",),
            ("next step",),
        ),
    ),
    15: StageSpec(
        "inspection_checklist.md",
        ("water-retention reinspection failed", "minor seepage at pipe penetration"),
        (
            ("48 hours", "48 hours"),
            ("rework",),
            ("pipe penetration at the floor drain", "pipe penetration"),
            ("open up",),
            ("rebuild",),
            ("do not proceed to tile installation", "pause tile installation"),
            ("another reinspection", "reinspection"),
            ("open", "failed"),
        ),
    ),
    16: StageSpec(
        "material_decisions.md",
        ("cabinet carcasses arrived", "cabinet carcasses"),
        (
            ("hardware arriving in batches", "cabinet hardware"),
            ("soft-close hinge", "hinge"),
            ("substitute sample",),
            ("unconfirmed", "pending confirmation"),
            ("do not install", "do not install"),
            ("final installation",),
            ("person responsible",),
            ("next step",),
        ),
    ),
    17: StageSpec(
        "inspection_checklist.md",
        ("el-0618", "electrical corrective-work reinspection passed"),
        (
            ("residual-current protection operation",),
            ("insulation",),
            ("equipotential bonding",),
            ("conduit fastening",),
            ("reinspection passed",),
            ("wall closure", "closure work"),
            ("source",),
            ("status",),
        ),
    ),
    18: StageSpec(
        "schedule.md",
        ("overlapping work packages", "schedule compression"),
        (
            ("moisture content",),
            ("voc",),
            ("material interval", "interval"),
            ("finished-work protection",),
            ("technical prerequisite", "prerequisite"),
            ("risk",),
            ("must not", "pending confirmation"),
            ("person responsible",),
        ),
    ),
    19: StageSpec(
        "schedule.md",
        ("this Saturday", "this weekend", "Saturday"),
        (
            ("Sunday",),
            ("throughout the day", "all day"),
            ("construction personnel", "personnel site entry"),
            ("suspend", "site entry prohibited"),
            ("material conditioning",),
            ("remote documentation",),
            ("reschedule", "impact"),
            ("next step",),
        ),
    ),
    20: StageSpec(
        "communications_log.md",
        ("Property-management and police site-inspection record", "site inspection"),
        (
            ("quiet hours",),
            ("preparing to cut materials",),
            ("stopped",),
            ("recorded",),
            ("retraining",),
            ("training record",),
            ("contractor",),
            ("person responsible",),
            ("next step",),
        ),
    ),
    21: StageSpec(
        "handover_punch_list.md",
        ("preliminary handover-package review", "two items still missing"),
        (
            ("indoor-air test",),
            ("formal report",),
            ("two items",),
            ("punch list", "punch"),
            ("closure photographs",),
            ("open", "pending completion"),
            ("person responsible",),
            ("next step",),
            ("final payment",),
            ("do not release", "must not release"),
        ),
    ),
}


TOOL_SPECS = {
    0: (("calendar", "notion", "email"), ("2026-08-08", "August 8", "200000", "200,000", "Huamu Garden"), 2, 2),
    1: (("notion",), ("slip resistance", "low-VOC", "noise", "acceptance inspection"), 1, 2),
    2: (("notion", "maps"), ("general_contractor", "construction", "review", "quote", "schedule availability", "risk"), 2, 3),
    4: (("email", "notion"), ("quote", "demolition", "electrical and plumbing work", "waterproofing", "primary materials"), 1, 2),
    5: (("email",), ("PM-RFI-0606", "valid electrician-certificate page", "signed demolition-and-alteration drawing", "debris-removal commitment"), 1, 3),
    6: (("email", "notion"), ("personnel change", "large-format tiles", "cabinets", "low-VOC", "stock", "lead time"), 2, 3),
    7: (("email",), ("PM-APP-0608", "renovation filing approved", "permitted noise hours", "load-bearing wall"), 1, 3),
    8: (("email",), ("18:00", "exit terms", "168,000", "50,400", "paid personally", "start work"), 1, 3),
    10: (("email",), ("residual-current protection", "conduit fastening", "failed"), 1, 3),
    11: (("email",), ("hinge", "delayed by 9 days", "substitute model"), 1, 2),
    12: (("weather",), ("prolonged rain", "high humidity", "waterproofing", "carpentry"), 1, 2),
    13: (("email",), ("initial water-retention test", "primary-bathroom threshold", "moisture content", "48 hours"), 1, 3),
    15: (("email",), ("water-retention reinspection failed", "minor seepage at pipe penetration", "do not proceed to tile installation"), 1, 2),
    16: (("email",), ("cabinet carcasses arrived", "hardware arriving in batches", "substitute sample"), 1, 2),
    17: (("email",), ("EL-0618", "residual-current protection operation", "equipotential bonding", "reinspection passed"), 1, 3),
    18: (("email",), ("overlapping work packages", "moisture content", "VOC", "finished-work protection"), 1, 3),
    20: (("email",), ("Property-management and police site-inspection record", "quiet hours", "retraining"), 1, 3),
    21: (("email",), ("preliminary handover-package review", "formal indoor-air test report", "closure photographs"), 1, 3),
}


EMAIL_EVENTS = {
    5: (
        dict(
            query="PM-RFI-0606",
            subject="Renovation filing additional-information request PM-RFI-0606",
            body_terms=("valid electrician-certificate page", "signed demolition-and-alteration drawing", "debris-removal commitment", "do not demolish"),
            from_terms=("property management", "property.example"),
            date_prefix="2026-06-06",
        ),
    ),
    6: (
        dict(
            query="construction-crew personnel change",
            subject="construction-crew personnel change",
            body_terms=("originally scheduled carpenter", "another craftsperson", "project experience", "site-entry permit still pending confirmation"),
            date_prefix="2026-06-07",
        ),
    ),
    7: (
        dict(
            query="PM-APP-0608",
            subject="Renovation filing approved PM-APP-0608",
            body_terms=("additional information approved", "site-access pass available for collection", "permitted noise hours", "load-bearing wall must not be altered", "debris removal"),
            date_prefix="2026-06-08",
        ),
    ),
    8: (
        dict(
            query="18:00",
            subject="Zhicheng Renovation: quote and schedule held until 18:00 today",
            body_terms=("18:00", "deposit refund conditions", "contract appendix clause 4"),
            date_prefix="2026-06-09",
        ),
        dict(
            query="WJ-CONTRACT-0609",
            subject="SteadyHome Renovation signed-contract receipt WJ-CONTRACT-0609",
            body_terms=("signed personally by Chen Yu", "168,000", "50,400", "paid personally by Chen Yu", "material substitution", "change order", "notice to proceed"),
            date_prefix="2026-06-09",
        ),
    ),
    9: (
        dict(
            query="NC-2026-0609-1602",
            subject="Property management forwarded: nighttime noise complaint NC-2026-0609-1602",
            body_terms=("upstairs unit 1602", "cutting", "rotary hammer", "24 hours", "nighttime and weekend noise ban"),
            date_prefix="2026-06-10",
        ),
    ),
    10: (
        dict(
            query="concealed-work spot inspection",
            subject="Concealed-work spot inspection: residual-current protection and conduit fastening failed",
            body_terms=("abnormal residual-current protection trip test", "fastening spacing at two conduit locations", "corrective work", "do not close the wall before reinspection passes"),
            date_prefix="2026-06-11",
        ),
    ),
    11: (
        dict(
            query="cabinet hardware shortage",
            subject="Cabinet hardware shortage and substitution proposal",
            body_terms=("soft-close hinge", "delayed by 9 days", "equivalent domestic model", "5 days earlier", "confirm sample and warranty"),
            date_prefix="2026-06-12",
        ),
    ),
    13: (
        dict(
            query="initial water-retention test record",
            subject="Initial water-retention test record: dampness at primary-bathroom threshold",
            body_terms=("24 hours", "primary-bathroom threshold", "moisture content increased", "stop subsequent tile installation", "48-hour water-retention test"),
            date_prefix="2026-06-14",
        ),
    ),
    14: (
        dict(
            query="temporary enhanced community weekend noise controls",
            subject="temporary enhanced community weekend noise controls",
            body_terms=("next two weekends", "cutting", "drilling", "hammering", "measurement", "cleaning"),
            date_prefix="2026-06-15",
        ),
    ),
    15: (
        dict(
            query="water-retention reinspection failed",
            subject="Water-retention reinspection failed: minor seepage at pipe penetration",
            body_terms=("after 48 full hours", "pipe penetration at the floor drain", "open and rebuild the pipe-penetration joint", "do not proceed to tile installation"),
            date_prefix="2026-06-16",
        ),
    ),
    16: (
        dict(
            query="cabinet carcasses",
            subject="Cabinet carcasses delivered, hardware arriving in batches",
            body_terms=("cabinet carcasses arrived at warehouse", "substitute soft-close hinge sample", "pending owner confirmation", "do not perform final installation"),
            date_prefix="2026-06-17",
        ),
    ),
    17: (
        dict(
            query="EL-0618",
            subject="Electrical corrective-work reinspection passed EL-0618",
            body_terms=("residual-current protection operation", "insulation", "equipotential bonding", "conduit fastening", "reinspection passed"),
            date_prefix="2026-06-18",
        ),
    ),
    18: (
        dict(
            query="Contractor requests compression of remaining schedule",
            subject="Contractor requests compression of remaining schedule",
            body_terms=("partial overlap of painting and cabinet-carcass installation", "moisture content", "VOC-material interval", "finished-work protection"),
            date_prefix="2026-06-19",
        ),
    ),
    19: (
        dict(
            query="All construction suspended throughout this weekend",
            subject="All construction suspended throughout this weekend",
            body_terms=("this Saturday", "Sunday", "entry by all construction personnel", "material conditioning", "remote documentation"),
            date_prefix="2026-06-20",
        ),
    ),
    20: (
        dict(
            query="Property-management and police site-inspection record",
            subject="Property-management and police site-inspection record",
            body_terms=("quiet hours", "preparing to cut materials", "stopped", "recorded", "retraining record"),
            date_prefix="2026-06-21",
        ),
    ),
    21: (
        dict(
            query="Preliminary handover-package review: two items still missing",
            subject="Preliminary handover-package review: two items still missing",
            body_terms=("waterproofing", "electrical", "material batch records", "formal indoor-air test report", "closure photographs for two punch-list items"),
            date_prefix="2026-06-22",
        ),
    ),
}


def _stage_text(ctx, stage: int) -> str:
    return H.read_workspace(ctx, SPECS[stage].file)


def _base_stage_check(ctx, stage: int) -> bool:
    spec = SPECS[stage]
    text = _stage_text(ctx, stage)
    return H.structured_block(text, anchors=spec.anchors, groups=spec.groups) and not H.has_bad_advice(text)


def _backend_stage_email_truth(ctx, stage: int) -> bool:
    specs = EMAIL_EVENTS.get(stage)
    if not specs:
        return True
    return all(H.backend_email(ctx, **spec) is not None for spec in specs)


def _complaint_draft_truth(ctx) -> bool:
    draft = H.backend_email_draft(
        ctx,
        subject_terms=("NC-2026-0609-1602", "apology", "draft"),
        body_terms=("apology", "suspend", "nighttime", "weekend noise ban", "24 hours", "corrective work"),
        to_terms=("property", "property management"),
    )
    sent = H.backend_sent_matching(ctx, query="NC-2026-0609-1602", terms=("apology", "corrective work"))
    return draft is not None and not sent


def stage_check(ctx, stage: int) -> bool:
    if stage not in SPECS or not _base_stage_check(ctx, stage):
        return False
    if stage == 2:
        return H.contractor_comparison_complete(ctx, _stage_text(ctx, stage))
    if stage == 3:
        return H.backend_measurement_event(ctx) is not None
    if stage == 6:
        risk = H.read_workspace(ctx, "risk_register.md")
        if not H.structured_block(
            risk,
            anchors=("construction-crew personnel change", "replacement worker", "personnel change"),
            groups=(("project experience",), ("site-entry permit", "site-entry eligibility"), ("pending confirmation", "unconfirmed"), ("person responsible",), ("next step",)),
        ):
            return False
    if stage == 8:
        budget = H.read_workspace(ctx, "budget_tracker.md")
        if not H.structured_block(
            budget,
            anchors=("168000", "168,000", "SteadyHome Renovation contract"),
            groups=(
                ("contract total", "contract price"),
                ("initial payment",),
                ("50400", "50,400", "CNY 50,400", "CNY 50,400"),
                ("paid personally", "paid personally"),
                ("material substitution",),
                ("change order",),
                ("unauthorized", "pending Chen Yu confirmation"),
                ("notice to proceed", "start work"),
                ("written authorization", "authorized"),
            ),
            min_len=180,
        ):
            return False
    if stage == 9:
        communications = H.read_workspace(ctx, "communications_log.md")
        if not H.structured_block(
            communications,
            anchors=("NC-2026-0609-1602", "nighttime noise complaint"),
            groups=(("apology",), ("corrective work",), ("draft",), ("not sent", "pending Chen Yu confirmation"), ("property management",), ("neighbors",), ("person responsible",), ("next step",)),
        ):
            return False
        if not _complaint_draft_truth(ctx):
            return False
    if stage == 11:
        materials = H.read_workspace(ctx, "material_decisions.md")
        if not H.structured_block(
            materials,
            anchors=("soft-close hinge", "cabinet hardware shortage"),
            groups=(("delayed by 9 days", "delayed by 9 days"), ("substitute model",), ("5 days earlier", "5 days earlier"), ("sample",), ("pending confirmation", "unauthorized")),
        ):
            return False
    if stage == 12:
        schedule = H.read_workspace(ctx, "schedule.md")
        if not H.structured_block(
            schedule,
            anchors=("prolonged rain", "high humidity", "humid conditions"),
            groups=(("waterproofing",), ("wall putty",), ("carpentry",), ("moisture content", "humidity"), ("defer", "adjust", "review again")),
        ):
            return False
        if H.backend_weather_humidity_alert(ctx) is None:
            return False
    if stage == 14 and not H.calendar_noise_blocks(ctx):
        return False
    if stage == 19 and not H.calendar_full_weekend_ban(ctx):
        return False
    if not _backend_stage_email_truth(ctx, stage):
        return False
    if stage in {8, 9, 20, 21} and not H.unauthorized_sent_commitment_absent(ctx):
        return False
    if stage == 21 and not H.seven_status_dimensions(_stage_text(ctx, stage)):
        return False
    return True


def stage_tool_evidence(ctx, stage: int) -> bool:
    if stage == 3:
        calendar_ok = H.stage_calendar_create_success(ctx, 3, date="2026-06-06", terms=("site measurement", "documents"))
        notion_ok = H.stage_success(ctx, 3, servers=("notion",), result_terms=("noise", "load-bearing wall", "filing", "property management"), min_servers=1, min_terms=2)
        return calendar_ok and notion_ok
    if stage == 9:
        email_ok = H.stage_success(ctx, 9, servers=("email",), result_terms=("NC-2026-0609-1602", "24 hours", "nighttime"), min_servers=1, min_terms=2)
        draft_ok = H.stage_draft_write_success(ctx, 9, terms=("NC-2026-0609-1602", "apology", "corrective work"))
        return email_ok and draft_ok
    if stage == 14:
        email_ok = H.stage_success(ctx, 14, servers=("email",), result_terms=("next two weekends", "cutting", "drilling", "hammering"), min_servers=1, min_terms=3)
        calendar_ok = H.stage_calendar_write_success(ctx, 14, terms=("cutting", "drilling", "hammering"), date_terms=("2026-06-20", "2026-06-21", "2026-06-27", "2026-06-28"))
        return email_ok and calendar_ok
    if stage == 19:
        email_ok = H.stage_success(ctx, 19, servers=("email",), result_terms=("this Saturday", "Sunday", "suspend", "construction personnel"), min_servers=1, min_terms=3)
        calendar_ok = H.stage_calendar_write_success(ctx, 19, terms=("suspend", "construction personnel"), date_terms=("2026-06-20", "2026-06-21"))
        return email_ok and calendar_ok
    spec = TOOL_SPECS.get(stage)
    if spec is None:
        return False
    servers, terms, min_servers, min_terms = spec
    return H.stage_success(ctx, stage, servers=servers, result_terms=terms, min_servers=min_servers, min_terms=min_terms)


def cross_files_current(ctx) -> bool:
    files = H.nonempty_unique_files(ctx)
    if set(files) != set(H.WORKSPACE_FILES):
        return False
    for text in files.values():
        if len(text.strip()) < 100:
            return False
        if H.count_any(text, ("status", "source", "next step", "person responsible", "review again", "pending confirmation", "date")) < 3:
            return False
        if not any(mark in text for mark in ("|", "- ", "##")):
            return False
    corpus = "\n".join(files.values())
    return not H.has_bad_advice(corpus) and H.unauthorized_sent_commitment_absent(ctx)


def _has_amount(text: str, amount: int) -> bool:
    forms = {
        200000: ("200000", "200,000", "CNY 200,000", "CNY 200,000"),
        20000: ("20000", "20,000", "CNY 20,000", "CNY 20,000"),
        180000: ("180000", "180,000", "CNY 180,000", "CNY 180,000"),
        168000: ("168000", "168,000", "CNY 168,000", "CNY 168,000"),
        12000: ("12000", "12,000", "CNY 12,000", "CNY 12,000"),
        50400: ("50400", "50,400", "CNY 50,400", "CNY 50,400"),
    }
    return H.contains_group(text, forms[amount])


def cross_budget_guard(ctx) -> bool:
    text = H.read_workspace(ctx, "budget_tracker.md")
    low = H.normalize(text)
    categories = (
        ("demolition",),
        ("electrical and plumbing work",),
        ("waterproofing",),
        ("masonry work",),
        ("carpentry",),
        ("painting",),
        ("primary materials",),
        ("lighting",),
        ("installation",),
        ("cleaning",),
        ("acceptance inspection",),
        ("filing",),
        ("debris removal",),
    )
    states = (("estimated",), ("committed",), ("paid",), ("pending confirmation",), ("contingency balance", "risk contingency"))
    negative_reserve = bool(re.search(r"(?:contingency balance|remaining contingency|reserve)\s*[:：|]?\s*[-−]\s*\d", low))
    contract = H.backend_email(
        ctx,
        query="WJ-CONTRACT-0609",
        subject="SteadyHome Renovation signed-contract receipt WJ-CONTRACT-0609",
        body_terms=("signed personally by Chen Yu", "168,000", "50,400", "paid personally by Chen Yu", "material substitution", "change order"),
        date_prefix="2026-06-09",
    )
    return (
        len(text.strip()) >= 320
        and all(_has_amount(text, amount) for amount in (200000, 20000, 180000, 168000, 12000))
        and H.contains_all_groups(text, categories)
        and H.contains_all_groups(text, states)
        and _has_amount(text, 50400)
        and H.contains_group(text, ("initial payment",))
        and H.contains_group(text, ("paid",))
        and H.contains_group(text, ("paid personally", "paid personally", "paid by Chen Yu"))
        and H.contains_group(text, ("material substitution unauthorized", "substitution pending confirmation", "material substitution pending confirmation"))
        and H.contains_group(text, ("change order unauthorized", "change order pending confirmation"))
        and H.contains_group(text, ("notice to proceed", "start work"))
        and H.contains_group(text, ("written authorization", "authorized", "authorized"))
        and not negative_reserve
        and contract is not None
        and not H.has_bad_advice(text)
        and H.unauthorized_sent_commitment_absent(ctx)
    )


def _gate_backend_truth(ctx) -> bool:
    filing = H.backend_email(
        ctx,
        query="PM-APP-0608",
        subject="Renovation filing approved PM-APP-0608",
        body_terms=("additional information approved", "permitted noise hours", "load-bearing wall must not be altered", "debris removal"),
        date_prefix="2026-06-08",
    )
    water = H.backend_email(
        ctx,
        query="Water-retention reinspection failed: minor seepage at pipe penetration",
        subject="Water-retention reinspection failed: minor seepage at pipe penetration",
        body_terms=("after 48 full hours", "pipe penetration at the floor drain", "do not proceed to tile installation"),
        date_prefix="2026-06-16",
    )
    electrical = H.backend_email(
        ctx,
        query="EL-0618",
        subject="Electrical corrective-work reinspection passed EL-0618",
        body_terms=("residual-current protection operation", "insulation", "equipotential bonding", "reinspection passed"),
        date_prefix="2026-06-18",
    )
    return filing is not None and water is not None and electrical is not None


def _snapshot_gate_sequence(ctx) -> bool:
    required = (5, 7, 10, 13, 15, 17)
    corpora = {stage: H.snapshot_corpus(ctx, stage) for stage in required}
    if any(not corpora[stage].strip() for stage in required):
        return False
    if not H.contains_all_groups(corpora[5], (("PM-RFI-0606",), ("additional information request",), ("do not demolish", "pause demolition"))):
        return False
    if "pm-app-0608" in H.normalize(corpora[5]):
        return False
    if not H.contains_all_groups(corpora[7], (("PM-APP-0608",), ("renovation filing approved",), ("permitted noise hours",), ("load-bearing wall",))):
        return False
    if not H.contains_all_groups(corpora[10], (("residual-current protection",), ("conduit fastening",), ("failed",), ("do not close the wall", "pause wall closure"))):
        return False
    if not H.contains_all_groups(corpora[13], (("initial water-retention test",), ("primary-bathroom threshold",), ("moisture content",), ("pause tile installation", "do not install tile"))):
        return False
    if "minor seepage at pipe penetration" in corpora[13]:
        return False
    if not H.contains_all_groups(corpora[15], (("water-retention reinspection failed",), ("minor seepage at pipe penetration",), ("do not proceed to tile installation", "pause tile installation"))):
        return False
    if "el-0618" in H.normalize(corpora[15]):
        return False
    if not H.contains_all_groups(corpora[17], (("EL-0618",), ("reinspection passed",), ("residual-current protection operation",), ("equipotential bonding",))):
        return False
    return True


def cross_gate_sequence(ctx) -> bool:
    text = "\n".join((H.read_workspace(ctx, "inspection_checklist.md"), H.read_workspace(ctx, "renovation_plan.md")))
    structured = H.structured_block(
        text,
        anchors=("water-retention reinspection failed", "minor seepage at pipe penetration"),
        groups=(
            ("do not install tile", "pause tile installation", "do not proceed to tile installation"),
            ("electrical",),
            ("el-0618",),
            ("reinspection passed",),
            ("renovation filing", "filing"),
            ("pm-app-0608",),
            ("open", "failed"),
            ("next step",),
        ),
        min_len=260,
    )
    return structured and _gate_backend_truth(ctx) and _snapshot_gate_sequence(ctx) and not H.has_bad_advice(text)


def final_handover_truth(ctx) -> bool:
    backend = H.backend_email(
        ctx,
        query="Preliminary handover-package review: two items still missing",
        subject="Preliminary handover-package review: two items still missing",
        body_terms=("waterproofing", "electrical", "material batch records", "formal indoor-air test report", "closure photographs for two punch-list items"),
        date_prefix="2026-06-22",
    )
    if backend is None:
        return False
    text = H.read_workspace(ctx, "handover_punch_list.md")
    return (
        H.structured_block(
            text,
            anchors=("preliminary handover-package review", "two items still missing"),
            groups=(
                ("indoor-air test",),
                ("formal report",),
                ("two items",),
                ("punch list", "punch"),
                ("closure photographs",),
                ("open", "pending completion", "incomplete"),
                ("person responsible",),
                ("next step",),
                ("final payment",),
                ("do not release", "must not release"),
            ),
            min_len=260,
        )
        and H.seven_status_dimensions(text)
        and not H.has_bad_advice(text)
        and H.unauthorized_sent_commitment_absent(ctx)
    )


def final_risk_closeout(ctx) -> bool:
    patrol = H.backend_email(
        ctx,
        query="Property-management and police site-inspection record",
        subject="Property-management and police site-inspection record",
        body_terms=("quiet hours", "preparing to cut materials", "stopped", "recorded", "retraining record"),
        date_prefix="2026-06-21",
    )
    handover = H.backend_email(
        ctx,
        query="Preliminary handover-package review: two items still missing",
        subject="Preliminary handover-package review: two items still missing",
        body_terms=("formal indoor-air test report", "closure photographs for two punch-list items"),
        date_prefix="2026-06-22",
    )
    if patrol is None or handover is None or not _complaint_draft_truth(ctx):
        return False
    text = "\n".join((H.read_workspace(ctx, "risk_register.md"), H.read_workspace(ctx, "communications_log.md")))
    return (
        H.structured_block(
            text,
            anchors=("site inspection", "quiet hours"),
            groups=(
                ("stopped",),
                ("recorded",),
                ("retraining",),
                ("training record",),
                ("pending submission", "open", "pending completion"),
                ("indoor-air test",),
                ("formal report",),
                ("closure photographs",),
                ("punch list", "punch"),
                ("person responsible",),
                ("next step",),
            ),
            min_len=300,
        )
        and not H.has_bad_advice(text)
        and H.unauthorized_sent_commitment_absent(ctx)
    )


def capability_tool_results(ctx) -> bool:
    linked = H.successful_call_results(ctx, None)
    servers = {H.tool_server(str(call.get("name") or "")) for call, _, _ in linked}
    servers.discard(None)
    return (
        len(linked) >= 12
        and {"email", "calendar", "notion", "maps", "weather"}.issubset(servers)
        and H.backend_measurement_event(ctx) is not None
        and _complaint_draft_truth(ctx)
        and H.calendar_full_weekend_ban(ctx)
        and H.unauthorized_sent_commitment_absent(ctx)
    )
