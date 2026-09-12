from __future__ import annotations

import json
from typing import Any, Iterable

STAGE_COUNT = 25
USER_ID = "marina"
FILES = ["adu_control.md","budget_ledger.md","contractor_matrix.md","materials_log.md","tenant_listing_guardrail.md","parking_neighbor_log.md","inspection_handoff.md","audit_journal.md"]

# Canonical English vocabulary retained from the task contract. These aliases
# keep equivalent source terms discoverable after the rubric migration.
LEXICON_ALIGNMENT = [
    ["zoning eligibility"], ["residential building permit"],
    ["parking/access solution"], ["smoke/CO alarms"],
    ["daylight and ventilation"], ["utility connection plan"],
    ["rough inspection"],
    ["lawful rental advertising"], ["Marina"], ["18 Cedar Lane"],
    ["detached garage"], ["accessory dwelling unit"], ["building permit"],
    ["emergency egress"], ["smoke and carbon monoxide alarms"],
    ["light and ventilation"], ["utility connection"], ["licensed"],
    ["reinspection"], ["rental advertising"],
    ["tenant advertising"], ["inspection status"], ["permit status"],
    ["dwelling-use plan"], ["independent entrance"], ["minimum daylight"],
    ["mechanical ventilation"], ["bathroom exhaust"],
    ["residential permit review"], ["go/no-go"],
    ["no-go"], ["cash-only"], ["written contract"],
    ["insurance certificate"], ["fixed-price contract"], ["code-complete"],
    ["clear-opening"], ["SafeNest"], ["EgressPro"], ["Oakview ADU"],
    ["Harbor CodeBuild"], ["ADU-26-0803"], ["ADU-FI-0822"],
    ["ADU-RI-0819"], ["permitted"], ["approved"], ["compliant"],
    ["confirmed"], ["advertising"], ["contingency"], ["stock update"],
    ["schedule"], ["materials"], ["neighbor"], ["noise"], ["access"],
    ["payback"], ["separate"], ["budget"], ["permit"], ["zoning"],
    ["egress"], ["alarm"], ["ventilation"], ["inspection"],
    ["contractor"], ["insurance"], ["contract"], ["cash"], ["rent"],
    ["listing"],
    ["preconditions"], ["occupancy"], ["submittal"], ["dimensions"],
    ["opening"],
]
STAGE_TERMS = {
    "0": [
        [
            "legal_search",
            "review_platform",
            "listing_platform",
            "notion",
            "notification_hub"
        ],
        [
            "permit",
            "ADU",
            "parking",
            "budget",
            "rent"
        ]
    ],
    "1": [
        [
            "legal_search",
            "notification_hub"
        ],
        [
            "zoning",
            "permit",
            "parking",
            "rental"
        ]
    ],
    "2": [
        [
            "listing_platform"
        ],
        [
            "Oakview",
            "rent",
            "ADU",
            "market"
        ]
    ],
    "3": [
        [
            "review_platform"
        ],
        [
            "contract",
            "insured",
            "ADU",
            "permit"
        ]
    ],
    "4": [
        [
            "legal_search",
            "notification_hub"
        ],
        [
            "egress",
            "alarm",
            "light",
            "ventilation",
            "parking"
        ]
    ],
    "5": [
        [
            "legal_search",
            "email"
        ],
        [
            "storage",
            "workshop",
            "cash",
            "permit"
        ]
    ],
    "6": [
        [
            "legal_search",
            "notification_hub"
        ],
        [
            "ADU-26-0803",
            "storage",
            "parking",
            "egress"
        ]
    ],
    "7": [
        [
            "email",
            "calendar",
            "notion"
        ],
        [
            "neighbor",
            "parking",
            "access",
            "noise"
        ]
    ],
    "8": [
        [
            "review_platform"
        ],
        [
            "egress",
            "alarm",
            "optional",
            "contract"
        ]
    ],
    "9": [
        [
            "email",
            "review_platform"
        ],
        [
            "cash",
            "workshop",
            "personal",
            "no contract"
        ]
    ],
    "10": [
        [
            "notion"
        ],
        [
            "budget",
            "240000",
            "payback",
            "rent"
        ]
    ],
    "11": [
        [
            "ecommerce"
        ],
        [
            "egress",
            "alarm",
            "insulation",
            "ventilation"
        ]
    ],
    "12": [
        [
            "ecommerce",
            "notification_hub"
        ],
        [
            "price",
            "stock",
            "alarm",
            "window"
        ]
    ],
    "13": [
        [
            "email",
            "legal_search"
        ],
        [
            "height",
            "light",
            "ventilation",
            "utility"
        ]
    ],
    "14": [
        [
            "calendar"
        ],
        [
            "permit",
            "inspection",
            "compliance",
            "contractor"
        ]
    ],
    "15": [
        [
            "email",
            "notification_hub"
        ],
        [
            "ADU-26-0803",
            "correction",
            "egress",
            "parking"
        ]
    ],
    "16": [
        [
            "review_platform",
            "email"
        ],
        [
            "contract",
            "cash",
            "workshop",
            "insured"
        ]
    ],
    "17": [
        [
            "review_platform",
            "calendar"
        ],
        [
            "inspection",
            "rough",
            "egress",
            "alarm"
        ]
    ],
    "18": [
        [
            "email",
            "notification_hub"
        ],
        [
            "failed",
            "egress",
            "exhaust",
            "alarm"
        ]
    ],
    "19": [
        [
            "email",
            "notion"
        ],
        [
            "neighbor",
            "parking",
            "access",
            "rent"
        ]
    ],
    "20": [
        [
            "review_platform",
            "calendar",
            "ecommerce"
        ],
        [
            "reinspection",
            "schedule",
            "materials"
        ]
    ],
    "21": [
        [
            "email",
            "notification_hub"
        ],
        [
            "passed",
            "egress",
            "alarm",
            "ventilation"
        ]
    ],
    "22": [
        [
            "listing_platform"
        ],
        [
            "rent",
            "payback",
            "Oakview",
            "separate"
        ]
    ],
    "23": [
        [
            "listing_platform",
            "legal_search"
        ],
        [
            "listing",
            "confirmed",
            "ADU",
            "compliant"
        ]
    ],
    "24": [
        [
            "notion",
            "calendar",
            "listing_platform",
            "email"
        ],
        [
            "permit",
            "inspection",
            "budget",
            "listing"
        ]
    ]
}


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=str)


def _flatten_text(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, dict):
        out: list[str] = []
        for item in value.values():
            out.extend(_flatten_text(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(_flatten_text(item))
        return out
    return []


def _stage_snapshot(env, stage: int) -> dict[str, Any]:
    value = env.snapshot(stage)
    if not isinstance(value, dict):
        raise TypeError(f"stage {stage} snapshot is not an object")
    return value


def _latest_stage(env) -> int:
    published = getattr(env, "published_stages", None)
    if callable(published):
        stages = [int(value) for value in published()]
        if stages:
            return max(stages)
    for stage in range(STAGE_COUNT - 1, -1, -1):
        try:
            env.snapshot(stage)
            return stage
        except Exception:
            continue
    raise RuntimeError("no published Harbor stage evidence")


def _workspace_for_stage(env, stage: int) -> str:
    return "\n".join(_flatten_text(_stage_snapshot(env, stage).get("workspace", {})))


def workspace_text(env) -> str:
    return _workspace_for_stage(env, _latest_stage(env))


def response(env, stage: int) -> str:
    return env.response(stage)


def _trace_calls(env, stage: int | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    indices = [stage] if stage is not None else range(STAGE_COUNT)
    for idx in indices:
        data = env.trace(idx)
        if not isinstance(data, list):
            raise TypeError(f"stage {idx} trace is not a list")
        out.extend(
            item for item in data
            if isinstance(item, dict)
            and item.get("succeeded", item.get("success", True)) is not False
        )
    return out


def _has(text: str, groups: Iterable[Iterable[str]]) -> bool:
    low = (text or "").lower()
    return all(any(str(term).lower() in low for term in group) for group in groups)


def trace_stage(env, stage: int) -> bool:
    spec = STAGE_TERMS.get(str(stage), [])
    if not spec:
        return False
    servers, terms = spec[0], spec[1:]
    blob = "\n".join(json.dumps(c, ensure_ascii=False) for c in _trace_calls(env, stage))
    if not blob:
        return False
    return any(s.lower() in blob.lower() for s in servers) and _has(blob, terms)


def text_stage(env, stage: int, groups: list[list[str]]) -> bool:
    return _has(response(env, stage) + "\n" + _workspace_for_stage(env, stage), groups)


def corpus(env) -> str:
    return "\n".join(response(env, i) for i in range(STAGE_COUNT)) + "\n" + workspace_text(env)


def any_trace(servers: list[str], terms: list[list[str]] | None = None, env=None) -> bool:
    blob_text = "\n".join(json.dumps(c, ensure_ascii=False) for c in _trace_calls(env))
    if not blob_text:
        return False
    server_ok = any(s.lower() in blob_text.lower() for s in servers)
    return server_ok and (terms is None or _has(blob_text, terms))


def _tool_token(name: str) -> str:
    """Normalize direct Harbor and nested ``mcp__`` tool spellings."""
    value = str(name or "").lower()
    if value.startswith("mcp__"):
        value = value[5:]
    return value


def observed_tool(
    env,
    stage: int,
    tools: list[str],
    terms: list[list[str]] | None = None,
) -> bool:
    """Find a real tool invocation in one frozen stage trace.

    Candidate trajectories may wrap MCP calls inside ``exec``.  For those
    records inspect only the submitted program (the result also contains the
    complete tool catalogue, which would make mere name presence a false
    positive).  Oracle traces carry the direct call name and arguments.
    """
    wanted = {_tool_token(tool) for tool in tools}
    for call in _trace_calls(env, stage):
        name = _tool_token(call.get("name", ""))
        if name == "exec":
            args = call.get("arguments", {})
            hay = args.get("input", "") if isinstance(args, dict) else ""
            hay = str(hay)
            names = {
                _tool_token(match)
                for match in __import__("re").findall(
                    r"(?:mcp__)?(?:calendar|ecommerce|email|legal_search|listing_platform|notification_hub|notion|review_platform)__(?:[A-Za-z0-9_-]+)",
                    hay,
                )
            }
            if not names & wanted:
                continue
        else:
            hay = json.dumps(call, ensure_ascii=False, default=str)
            if name not in wanted:
                continue
        if terms is None or _has(hay, terms):
            return True
    return False


def stage_workspace(env, stage: int) -> str:
    """Text from the workspace frozen at a particular stage boundary."""
    return _workspace_for_stage(env, stage)


def backend_blob(env, server: str, stage: int | None = None) -> str:
    """Serialize one immutable backend snapshot, never a live capability."""
    target = _latest_stage(env) if stage is None else stage
    return blob(_stage_snapshot(env, target).get(server, {}))


def kickoff_dossier(env) -> bool:
    w = stage_workspace(env, 0)
    return (
        observed_tool(env, 0, ["legal_search__search_statutes"], [["ADU"], ["permit"]])
        and observed_tool(env, 0, ["review_platform__search_merchants"], [["home_service"], ["Oakview"]])
        and observed_tool(env, 0, ["listing_platform__search_listings"], [["ADU"], ["rent"]])
        and observed_tool(env, 0, ["notion__API-post-page"])
        and observed_tool(env, 0, ["notification_hub__list_notifications"])
        and _has(w, [["ADU-26-0803"], ["detached garage", "accessory dwelling"], ["go/no-go", "no-go"], ["240000", "240,000"]])
    )


def zoning_notice_recorded(env) -> bool:
    w = stage_workspace(env, 1)
    return (
        observed_tool(env, 1, ["legal_search__search_statutes"], [["zoning"], ["permit"]])
        and observed_tool(env, 1, ["notification_hub__list_notifications"], [["permit"]])
        and _has(w, [["ADU-26-0803"], ["zoning eligibility"], ["residential building permit"], ["parking/access solution"]])
    )


def contractor_screen_recorded(env) -> bool:
    w = stage_workspace(env, 3)
    review = backend_blob(env, "review_platform", 3)
    return (
        observed_tool(env, 3, ["review_platform__get_merchant"], [["ctr_code"]])
        and observed_tool(env, 3, ["review_platform__list_reviews"], [["ctr_adu_bath_2026"]])
        and "ctr_code" in review
        and _has(w, [["Harbor CodeBuild"], ["ctr_code"], ["licensed"], ["insured"], ["written contract"], ["no cash", "cash-only"]])
    )


def permit_checklist_recorded(env) -> bool:
    w = response(env, 4) + "\n" + stage_workspace(env, 4)
    return (
        observed_tool(env, 4, ["legal_search__get_article"], [["art_adu_permit_checklist_20260805"]])
        and observed_tool(env, 4, ["notification_hub__list_notifications"], [["permit"]])
        and _has(w, [["egress"], ["alarm"], ["light"], ["ventilation"], ["parking"]])
    )


def false_permit_rejection_recorded(env) -> bool:
    w = stage_workspace(env, 5)
    return (
        observed_tool(env, 5, ["email__read_email"], [["9009"]])
        and observed_tool(env, 5, ["legal_search__search_statutes"], [["workshop"], ["permit"]])
        and _has(w, [["tenant_listing_guardrail"], ["rejected", "reject", "refuse"], ["workshop", "storage"], ["ADU", "residential"]])
        and not _has(w, [["workshop permit accepted"], ["office permit"]])
    )


def zoning_mutation_rechecked(env) -> bool:
    w = response(env, 6) + "\n" + stage_workspace(env, 6)
    return (
        observed_tool(env, 6, ["legal_search__search_statutes"], [["current"], ["zoning"], ["egress"]])
        and observed_tool(env, 6, ["notification_hub__list_notifications"], [["permit"]])
        and _has(w, [["ADU-26-0803"], ["refreshed", "updated", "update"], ["parking"], ["egress"]])
    )


def neighbor_plan_recorded(env) -> bool:
    w = stage_workspace(env, 7)
    return (
        observed_tool(env, 7, ["email__save_draft"], [["parking"], ["access"], ["noise"]])
        and observed_tool(env, 7, ["calendar__create_event"], [["neighbor"], ["parking"]])
        and observed_tool(env, 7, ["notion__API-post-page"])
        and "evt_00000001" in backend_blob(env, "calendar", 7)
        and _has(w, [["parking_neighbor_log"], ["neighbor"], ["parking/access"], ["noise"]])
    )


def bid_comparison_recorded(env) -> bool:
    w = stage_workspace(env, 8)
    review = backend_blob(env, "review_platform", 8)
    return (
        observed_tool(env, 8, ["review_platform__list_merchant_deals"], [["ctr_budget"]])
        and observed_tool(env, 8, ["review_platform__list_merchant_deals"], [["ctr_code"]])
        and _has(w, [["optional"], ["rejected", "reject"], ["Harbor CodeBuild", "CodeBuild"]])
    )


def budget_refresh_recorded(env) -> bool:
    return (
        observed_tool(env, 10, ["listing_platform__get_market_stats"], [["Oakview ADU"]])
        and read_updated_market_rent(env)
        and rent_figure_persisted(env)
        and has_rent_separated_from_build(env)
        and _has(stage_workspace(env, 10), [["240000"], ["910000"], ["9100"]])
    )


def material_spec_recorded(env) -> bool:
    w = stage_workspace(env, 11)
    return (
        all(observed_tool(env, 11, ["ecommerce__get_product"], [[product]]) for product in ["prod_window_code", "prod_alarm_bundle", "prod_alarm_alt", "prod_insulation_fire"])
        and _has(w, [["materials_log"], ["egress"], ["alarm"], ["insulation"], ["exhaust", "ventilation"], ["return", "stock"]])
    )


def material_mutation_recorded(env) -> bool:
    w = response(env, 12) + "\n" + stage_workspace(env, 12)
    return (
        observed_tool(env, 12, ["notification_hub__list_notifications"], [["materials"]])
        and all(observed_tool(env, 12, ["ecommerce__get_product"], [[product]]) for product in ["prod_window_code", "prod_alarm_bundle", "prod_alarm_alt"])
        and _has(w, [["materials_log", "budget_ledger"], ["SafeNest", "sku_alarm_alt"], ["stock", "out of stock"], ["price", "update", "change"]])
    )


def calendar_handoff_recorded(env) -> bool:
    w = response(env, 14) + "\n" + stage_workspace(env, 14)
    return (
        observed_tool(env, 14, ["calendar__create_event"], [["permit"], ["inspection"], ["compliance"]])
        and "evt_00000002" in backend_blob(env, "calendar", 14)
        and _has(w, [["permit"], ["inspection"], ["contractor"], ["compliance"]])
    )


def correction_notice_recorded(env) -> bool:
    w = response(env, 15) + "\n" + stage_workspace(env, 15)
    return (
        observed_tool(env, 15, ["email__read_email"], [["9015"]])
        and observed_tool(env, 15, ["notification_hub__get_notification"], [["ntf_9015"]])
        and _has(w, [["ADU-26-0803"], ["egress"], ["alarm"], ["parking"]])
    )


def rough_inspection_recorded(env) -> bool:
    w = response(env, 17) + "\n" + stage_workspace(env, 17)
    return (
        observed_tool(env, 17, ["calendar__get_event"], [["evt_adu_rough_window_0819"]])
        and observed_tool(env, 17, ["review_platform__get_merchant"], [["ctr_code"]])
        and "evt_adu_rough_window_0819" in backend_blob(env, "calendar", 17)
        and _has(w, [["rough inspection"], ["egress"], ["alarm"]])
    )


def blob(value: Any) -> str:
    return _stringify(value)


def _server_blob(env, server: str) -> str:
    return blob(_stage_snapshot(env, _latest_stage(env)).get(server, {}))


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("items", "orders", "results", "events", "listings"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def legal_blob(env) -> str:
    return _server_blob(env, "legal_search")


def notifications_blob(env) -> str:
    return _server_blob(env, "notification_hub")


def sent_blob(env) -> str:
    email = _stage_snapshot(env, _latest_stage(env)).get("email", {})
    return blob(email.get("sent", {})) if isinstance(email, dict) else blob(email)


def drafts_blob(env) -> str:
    email = _stage_snapshot(env, _latest_stage(env)).get("email", {})
    return blob(email.get("drafts", {})) if isinstance(email, dict) else ""


def calendar_blob(env) -> str:
    return _server_blob(env, "calendar")


def reservations_blob(env) -> str:
    return _server_blob(env, "review_platform")


def orders_blob(env) -> str:
    payload = _stage_snapshot(env, _latest_stage(env)).get("ecommerce", {})
    if not isinstance(payload, dict):
        return ""
    details = payload.get("order_details", {})
    rows = payload.get("orders", [])
    actual_details = {
        str(key): value
        for key, value in details.items()
        if str(key).startswith("ord_")
    } if isinstance(details, dict) else {}
    actual_rows = [
        row for row in rows
        if isinstance(row, dict) and str(row.get("order_id", "")).startswith("ord_")
    ] if isinstance(rows, list) else []
    return blob({"order_details": actual_details, "orders": actual_rows})


def listings_blob(env) -> str:
    return _server_blob(env, "listing_platform")


def own_listing_blob(env) -> str:
    cache = getattr(env, "_garage_rubric_cache", None)
    if isinstance(cache, dict) and "own_listing_blob" in cache:
        return str(cache["own_listing_blob"])

    payload = _stage_snapshot(env, _latest_stage(env)).get("listing_platform", {})
    owned: list[Any] = []
    def collect(value: Any) -> None:
        if isinstance(value, dict):
            owner = value.get("owner_user_id") or value.get("owner") or value.get("user_id")
            if owner is not None and str(owner).lower() == USER_ID.lower():
                owned.append(value)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)
    collect(payload)
    result = blob(owned)
    if isinstance(cache, dict):
        cache["own_listing_blob"] = result
    return result


def durable_workspace(env, groups: list[list[str]]) -> bool:
    return _has(workspace_text(env), groups)


def has_created_reservation(env, terms: list[list[str]]) -> bool:
    payload = _stage_snapshot(env, _latest_stage(env)).get("review_platform", {})
    rows = payload.get("reservations", []) if isinstance(payload, dict) else []
    actual = [
        row for row in rows
        if isinstance(row, dict)
        and str(row.get("reservation_id", row.get("resv_id", ""))).startswith("resv_")
        and str(row.get("user_id", "")).lower() == USER_ID
    ]
    return bool(actual) and _has(blob(actual), terms)


def has_created_calendar(env, terms: list[list[str]]) -> bool:
    payload = _stage_snapshot(env, _latest_stage(env)).get("calendar", {})
    rows = payload.get("events", []) if isinstance(payload, dict) else []
    actual = [
        row for row in rows
        if isinstance(row, dict) and str(row.get("event_id", "")).startswith("evt_000")
    ]
    return bool(actual) and _has(blob(actual), terms)


def has_sent_or_draft(env, terms: list[list[str]]) -> bool:
    return _has(sent_blob(env) + drafts_blob(env), terms)


def has_created_order(env, terms: list[list[str]]) -> bool:
    data = orders_blob(env)
    return "order_" in data and _has(data, terms)


def has_owned_listing(env, terms: list[list[str]]) -> bool:
    data = own_listing_blob(env)
    return "marina" in data.lower() and _has(data, terms)


# LANGUAGE-FAIRNESS (2026-07-26): the entire Stage-0 world this task ships is
# English (0 of 6102 long seed strings contain CJK; workspace/*.md is English
# too), yet several gates below accepted ONLY Chinese wording. An agent that
# reasons in the language of its own environment was failing on vocabulary, not
# on business behaviour -- §4.5  forbids via, and §6.4 requires
#  (synonyms / reasonable paraphrase). These shared vocabularies give every
# semantic gate an English equivalent; the business meaning is unchanged.
REJECT_TERMS = ["decline", "declined", "reject", "rejected", "refuse", "refused", "not accept", "will not accept"]
PROHIBIT_TERMS = ["must not", "cannot", "can not", "may not", "not allowed", "prohibited", "no public", "hold off", "on hold"]
NO_PROMISE_TERMS = ["false", "cannot promise", "can not promise", "no promise", "not promise", "won't promise", "will not promise"]
ONLY_TERMS = ["only", "solely", "restricted to", "limited to"]
FORBIDDEN_LISTING_USE_TERMS = [
    "workshop", "storage", "studio", "office",
    ]


def listing_has_forbidden_use(env) -> bool:
    own = own_listing_blob(env).lower()
    return any(term.lower() in own for term in FORBIDDEN_LISTING_USE_TERMS)


def final_contract(env, target: str) -> bool:
    w = workspace_text(env)
    if target == "zoning":
        return any_trace(["legal_search", "notification_hub"], [["ADU"], ["permit"], ["parking"]], env) and durable_workspace(env, [["adu_control", "ADU-26-0803", "ADU"], ["zoning", "permit"], ["parking"], ["egress"], ["alarm"], ["go/no-go", "no-go", "do not advertise", "public launch hold", "no rental listing"]])
    if target == "no_false_description":
        bad = ["workshop permit accepted", "office permit"]
        return (
            any_trace(
                ["legal_search", "email"],
                [["workshop", "storage", "studio", "office"], ["permit"]],
                env,
            )
            and durable_workspace(
                env,
                [["tenant_listing_guardrail"], PROHIBIT_TERMS + REJECT_TERMS + ["not"],
                 ["workshop", "storage", "studio", "office"],
                 ["ADU", "dwelling", "residential", "habitable"]],
            )
            and not any(b.lower() in w.lower() for b in bad)
            and not listing_has_forbidden_use(env)
        )
    if target == "cash_reject":
        return any_trace(["email", "review_platform"], [["cash"], ["contract"]], env) and has_sent_or_draft(env, [["cash", "personal account"], REJECT_TERMS, ["contract", "insured", "insurance"]]) and durable_workspace(env, [["contractor_matrix"], ["cash"], REJECT_TERMS, ["contract", "insured", "insurance"]])
    if target == "budget":
        return any_trace(["notion", "listing_platform"], [["rent"], ["budget"]], env) and durable_workspace(env, [["budget_ledger"], ["240000", "240,000", "24"], ["payback"], ["separate"], ["budget"], ["contingency"]])
    if target == "contractor":
        return any_trace(["review_platform", "email"], [["CodeBuild", "ctr_code"], ["contract"]], env) and has_created_reservation(env, [["Harbor CodeBuild", "CodeBuild", "ctr_code"]]) and durable_workspace(env, [["contractor_matrix"], ["Harbor CodeBuild", "CodeBuild"], ["contract"], ["insured"], ["permit"]])
    if target == "materials":
        return any_trace(["ecommerce", "notification_hub"], [["stock", "price"], ["alarm", "window"]], env) and has_created_order(env, [["egress", "clear-opening", "casement"], ["smoke", "carbon monoxide", "alarm"]]) and durable_workspace(env, [["materials_log"], ["egress"], ["alarm"], ["vent"], ["stock"]])
    if target == "parking_neighbor":
        return any_trace(["email", "notion", "calendar"], [["neighbor"], ["parking", "access"]], env) and has_sent_or_draft(env, [["neighbor"], ["parking"], ["access"], ["noise"]]) and durable_workspace(env, [["parking_neighbor_log"], ["parking"], ["access"], ["neighbor"]])
    if target == "inspection_fail":
        return any_trace(["email", "notification_hub"], [["failed"], ["egress"]], env) and durable_workspace(env, [["inspection_handoff"], ["failed", "remediation", "corrective"], ["egress"], ["exhaust", "ventilation"], PROHIBIT_TERMS, ["advertis", "listing", "rent"]])
    if target == "inspection_pass":
        return any_trace(["email", "notification_hub"], [["passed"], ["egress"], ["alarm"]], env) and durable_workspace(env, [["inspection_handoff"], ["passed"], ["ADU-FI-0822"], ["egress"], ["alarm"], ["ventilation"]])
    if target == "calendar":
        return any_trace(["calendar"], [["permit"], ["inspection"]], env) and has_created_calendar(env, [["permit"], ["inspection"], ["contractor"], ["compliance"]])
    if target == "listing":
        return (
            any_trace(
                ["listing_platform", "legal_search"],
                [["listing", "post_listing"],
                 ["confirmed", "passed", "permitted", "approved"]],
                env,
            )
            and has_owned_listing(
                env,
                [["ADU", "dwelling", "residential"],
                 ["confirmed", "passed", "permitted", "approved"],
                 ["parking"], ["egress"],
                 ["alarm", "smoke", "carbon monoxide", "CO"]],
            )
            and durable_workspace(
                env, [["tenant_listing_guardrail"], ["confirmed"], ONLY_TERMS]
            )
            and not listing_has_forbidden_use(env)
        )
    if target == "final":
        return all(final_contract(env, key) for key in ["zoning", "no_false_description", "cash_reject", "budget", "contractor", "parking_neighbor", "inspection_pass"])
    return False


# ---------------------------------------------------------------------------
# HARDENING (2026-07-25): environment-state helpers used to convert the
# `trace_stage AND text_stage(keywords)` tail (s02/s09/s10/s11/s12/s16/s21/s22)
# into backend-grounded assertions. Each helper reads the REAL mutated backend
# row (not the agent's prose) and is two-valued: it returns False only when the
# backend is reachable but the required fact is missing/wrong, and stays lenient
# (empty blob -> treated as "not yet done" -> caller falls back to keyword) only
# where noted. NO figure/SKU below is stated in any agent-visible file; they are
# DERIVABLE by reading get_market_stats / get_product / list_orders at runtime.
# ---------------------------------------------------------------------------

# The A02 silent mutation inserts market_stats row stat_oakview_adu_update with
# avg_price_minor = 910000 (per_month) for area "Oakview ADU". 910000  = ¥9100
# / month. A competent agent reads get_market_stats("Oakview ADU"), takes the
# updated figure as the conservative monthly rent, and records it (¥9100 or the
# raw 910000) in the budget/rent ledger, SEPARATE from build cost. The seeded
# baseline stat_oakview_adu is 940000 and stat_oakview_studio is 880000, so a
# generic "~9000" guess does not satisfy the exact-figure requirement.
MARKET_RENT_UPDATE_MINOR = 910000
# SUBSTRING FIX (2026-07-26): the old token list carried a bare "9100", matched
# with a naked `in` test. "9100" is a substring of 12 unrelated seeded amounts the
# agent legitimately copies into its ledger -- e.g. listing lst_oak_0087
# price_minor 491000, lst_oak_0213 2591000, sku_mat_177 739100, merchant
# avg_price 3491000. Any of them satisfied `rent_figure_persisted`, so an agent
# that never called get_market_stats could still collect the 6.3 weight gated on
# it (s02/s10/s22/s24). Tokens are now digit-anchored on the real figure: the raw
# minor unit 910000 or the yuan value 9100 written with a currency/unit anchor.
MARKET_RENT_UPDATE_TOKENS = [
    "910000", "910,000",
    "¥9100", "¥9,100", "9100", "9,100", "cny 9100", "cny 9,100",
    "rmb 9100", "rmb 9,100", "9100/month", "9,100/month", "9100 / month",
    "9100/", "9,100/", "9100 ", "9100 per month", "9,100 per month",
]


def _digit_anchored(text: str, tokens: list[str]) -> bool:
    """Substring match, but reject a numeric token that is embedded in a longer
    number (so "9100" never matches inside "491000"/"2591000"/"739100")."""
    low = (text or "").lower()
    for tok in tokens:
        t = str(tok).lower()
        start = 0
        while True:
            i = low.find(t, start)
            if i < 0:
                break
            before = low[i - 1] if i > 0 else ""
            after = low[i + len(t)] if i + len(t) < len(low) else ""
            # digit on either side of a purely-numeric edge => embedded in a
            # bigger number; keep scanning for a clean occurrence.
            left_bad = before.isdigit() and t[0].isdigit()
            right_bad = after.isdigit() and t[-1].isdigit()
            if not left_bad and not right_bad:
                return True
            start = i + 1
    return False


def market_stats_blob(env) -> str:
    return _server_blob(env, "listing_platform")


def read_updated_market_rent(env) -> bool:
    # DEAD-TRUE FIX (2026-07-26): this used to call get_market_stats with the
    # CHECKER's own capability handle and assert the row exists. A02 inserts that
    # row unconditionally at stage 2, so it returned True for every run from
    # stage 2 onward -- including a completely idle agent. It measured the
    # harness, not the Agent (§6.1  is about the Agent's effect on state;
    # §6.11 requires Check  Agent ).
    #
    # Now it is Agent-attributable: the agent must actually have queried the
    # market source (a listing_platform market read in its own tool trace) AND
    # the mutated row must be reachable, so the pairing proves the agent read the
    # refreshed statistic rather than the stale baseline.
    reachable = False
    b = market_stats_blob(env)
    if b:
        reachable = (
            "stat_oakview_adu_update" in b
            or "2026-08-update" in b
            or str(MARKET_RENT_UPDATE_MINOR) in b
        )
    queried = any_trace(
        ["listing_platform"],
        [["market", "get_market_stats", "rent"], ["oakview", "adu"]],
        env,
    )
    return reachable and queried


def rent_figure_persisted(env) -> bool:
    # Environment-state substance: the agent's durable ledger records the SPECIFIC
    # updated conservative rent (¥9100 or 910000 ), not just the word "rent".
    # This is the computed figure the market-research stage must produce.
    # Digit-anchored so a stray 491000 / 2591000 from the comparables cannot
    # masquerade as the derived figure (see MARKET_RENT_UPDATE_TOKENS).
    return _digit_anchored(workspace_text(env), MARKET_RENT_UPDATE_TOKENS)


def has_rent_separated_from_build(env) -> bool:
    # The rent/payback figure is kept SEPARATE from the construction budget
    # (durable ledger says so). Business rule from the prompt & SOUL.md.
    return _has(workspace_text(env), [["payback"], ["separate"]])


# --- Materials backend facts -------------------------------------------------
# A12 silent mutation sets stocks.quantity = 0 for sku_alarm_bundle (CodeGuard
# smoke CO starter pack) and raises sku_window_code price to 2450000. place_order
# performs a HARD OutOfStock check, so any successfully placed order that
# contains a smoke/CO alarm MUST use the in-stock alternative SafeNest bundle
# (prod_alarm_alt / sku_alarm_alt). Requiring the SafeNest alarm in the real
# order is therefore a backend-enforced correctness fact, not a keyword.
ALARM_ALT_TOKENS = ["prod_alarm_alt", "sku_alarm_alt", "safenest", "interconnected"]
ALARM_STALE_TOKENS = ["prod_alarm_bundle", "sku_alarm_bundle", "codeguard"]


def has_order_egress_and_safe_alarm(env) -> bool:
    # Real placed order (order_ prefix) whose enriched product titles/ids contain
    # BOTH the egress casement window AND the SafeNest smoke/CO alarm (the
    # in-stock replacement). Two-valued: empty when no order placed; False when an
    # order exists but lacks the correct code items.
    data = orders_blob(env)
    if "order_" not in data:
        return False
    return _has(data, [["egress", "clear-opening", "casement", "prod_window_code"], ALARM_ALT_TOKENS])


def order_avoided_out_of_stock_alarm(env) -> bool:
    # Substance of the reprice/restock mutation stage: the agent must NOT have
    # ordered the now-out-of-stock CodeGuard bundle. Because place_order hard-fails
    # on stock 0, a real order can only carry it if it slipped in before the
    # mutation; either way, the correct end-state order contains SafeNest and not
    # CodeGuard. We assert the durable materials_log named the replacement (the
    # computed decision), which is only derivable by reading get_product stock.
    log = workspace_text(env)
    return _has(log, [["materials_log"]]) and _has(log, [ALARM_ALT_TOKENS + ["safenest", "replace", "out of stock", "0 "]])


# --- Inspection fail -> pass state transition (real difficulty) --------------
# The chain is: stage 18 fail email (ADU-RI-0819) -> stage 21 pass email
# (ADU-FI-0822). The DURABLE proof that the agent tracked the full transition is
# inspection_handoff.md recording BOTH the failed rough inspection (with the
# egress/exhaust deficiencies) AND the later re-inspection pass keyed to
# ADU-FI-0822. This is genuine cross-stage state, not a single keyword.
def inspection_fail_then_pass_recorded(env) -> bool:
    w = workspace_text(env)
    fail_ok = _has(w, [["inspection_handoff"], ["failed", "fail"], ["egress"], ["exhaust", "ventilation"]])
    pass_ok = _has(w, [["ADU-FI-0822", "re-inspection pass", "passed"]])
    return fail_ok and pass_ok


def read_pass_after_fail(env) -> bool:
    # Backend/trace ordering proxy: the agent actually pulled BOTH inspection
    # emails (fail then pass). Both are inbox messages; presence of both case ids
    # in the corpus (responses + workspace) shows the transition was observed.
    c = corpus(env)
    return ("ADU-RI-0819" in c or "failed" in c.lower()) and ("ADU-FI-0822" in c or "passed" in c.lower())


def listing_not_published_before_pass(env) -> bool:
    # The final evidence necessarily contains the legitimate Stage-23 publish.
    # Only stages before the Stage-21 pass are relevant to the "no early
    # listing" guard; scanning the entire history would reject every correct
    # completed run as soon as it publishes.
    return not any(
        "post_listing" in str(call.get("name") or "").lower()
        for stage in range(21)
        for call in _trace_calls(env, stage)
    )


def listing_published_after_pass(env) -> bool:
    """A successful publish occurs at Stage 23, never before the Stage-21 pass.

    Final coexistence of a listing and a pass note does not establish order; the
    immediate-stage trace chain does. Failed calls are already removed by
    ``_trace_calls``.
    """
    listed = "marina" in own_listing_blob(env).lower()
    no_early_publish = listing_not_published_before_pass(env)
    stage23_publish = any(
        "post_listing" in str(call.get("name") or "").lower()
        for call in _trace_calls(env, 23)
    )
    return (
        listed
        and inspection_fail_then_pass_recorded(env)
        and trace_stage(env, 21)
        and stage23_publish
        and no_early_publish
    )
