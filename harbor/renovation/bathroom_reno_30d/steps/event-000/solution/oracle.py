#!/usr/bin/env python3
"""Executable Harbor Oracle for the bathroom renovation workflow."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

TASK_ID = "bathroom_reno_30d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The bathroom renovation record was updated from authoritative sources while all approval boundaries were preserved."

SERVICE_URLS = {
    "calendar": "http://calendar:8000/mcp",
    "credit_card": "http://credit-card:8000/mcp",
    "delivery_logistics": "http://delivery-logistics:8000/mcp",
    "ecommerce": "http://ecommerce:8000/mcp",
    "email": "http://email:8000/mcp",
    "listing_platform": "http://listing-platform:8000/mcp",
    "notification_hub": "http://notification-hub:8000/mcp",
    "weather": "http://weather:8000/mcp",
}

USER_ID = "usr_gan_mei"
ORDER_MAIN = "ord_r2bth_0001"
ORDER_ACCEPTANCE = "ord_r2bth_0002"
SETTLEMENT = "lst_r2bth_0001"
CARD_ID = "card_r2bth_01"
REFUND_ID = "ref_r2bth_b"


def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value
    return value


def _unwrap_mcp(result: Any) -> Any:
    """Normalize supported MCP return shapes; an empty content list succeeds."""
    if result is None:
        raise RuntimeError("MCP returned no result")
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if isinstance(structured, dict) and "result" in structured:
            return _decode(structured["result"])
        if structured not in (None, {}):
            return _decode(structured)
        result = blocks
    structured = getattr(result, "structuredContent", None)
    if structured is None:
        structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict) and "result" in structured:
        return _decode(structured["result"])
    if structured not in (None, {}):
        return _decode(structured)
    content = result if isinstance(result, list) else getattr(result, "content", None)
    if content is not None:
        if content == []:
            return []
        for block in content:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            text = getattr(block, "text", None)
            if text is None and isinstance(block, dict):
                text = block.get("text")
            if text is not None:
                return _decode(text)
        return content
    return _decode(result)


def _is_success(result: Any) -> bool:
    """Fail closed on explicit error envelopes while accepting empty reads."""
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    try:
        value = _unwrap_mcp(result)
    except Exception:
        return False
    if isinstance(value, dict):
        if value.get("isError") is True or value.get("is_error") is True:
            return False
        if value.get("error") not in (None, False, ""):
            return False
        if str(value.get("status") or "").lower() in {"error", "failed", "failure"}:
            return False
        if value.get("ok") is False:
            return False
    if isinstance(value, list):
        return all(_is_success(item) for item in value) if value else True
    return value is not None


class Recorder:
    """MCP client that records every successful or failed call for ATIF."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        if service not in SERVICE_URLS:
            raise ValueError(f"unsupported MCP service: {service!r}")
        call_id = f"call-{len(self.calls) + 1}"
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client

            configured = _decode(os.environ.get("HARBOR_MCP_URLS", "{}"))
            url = (configured.get(service) if isinstance(configured, dict) else None) or SERVICE_URLS[service]
            async with streamablehttp_client(url) as (read, write, _meta):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            value = _unwrap_mcp(raw)
            if not _is_success(raw):
                raise RuntimeError(f"{service}.{tool} returned an error envelope")
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": value,
                "success": True,
                "error": None,
            })
            return value
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            self.calls.append({
                "tool_call_id": call_id,
                "function_name": f"{service}__{tool}",
                "arguments": arguments,
                "result": {"error": error},
                "success": False,
                "error": error,
            })
            raise RuntimeError(f"MCP call failed: {service}.{tool}: {error}") from exc


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"version": 1, "events": [], "vars": {}}
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"oracle state is unreadable: {STATE_PATH}") from exc
    if not isinstance(value, dict) or value.get("version") != 1:
        raise RuntimeError("oracle state must be a versioned JSON object")
    if not isinstance(value.get("events"), list) or not isinstance(value.get("vars"), dict):
        raise RuntimeError("oracle state has invalid events/vars fields")
    return value


def _save_state(state: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(STATE_PATH.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def _append(path_name: str, marker: str, text: str) -> None:
    if Path(path_name).name != path_name:
        raise ValueError("workspace path must be a file name")
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    path = WORKSPACE / path_name
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    tag = f"<!-- oracle:{marker} -->"
    if tag in current:
        return
    path.write_text(current.rstrip() + f"\n\n{tag}\n{text.rstrip()}\n", encoding="utf-8")


BASE_FILES = {
    "order_tracker.md": """# Bathroom Renovation Order Tracker

## ord_r2bth_0001 - Contract and materials track
- Status: active verification; source: marketplace order, official product page, provider profile, and contract.
- Query time: 2026-06-15 09:00 +08:00; owner: Gan Mei with platform verification support.
- Qualification checks: contract verification code, licensed electrician, material batch, SKU, payment receipt, and grab-bar backing method.
- Next step: reconcile every inconsistency before any irreversible approval; user confirmation required.

## ord_r2bth_0002 - Quality and rework track
- Status: stage acceptance evidence in progress; source: work order, inspection records, email, and calendar.
- Query time: 2026-06-15 09:00 +08:00; owner: Gan Mei, contractor, property management, and inspector.
- Safety scope: threshold waterproofing, floor-drain slope, grab-bar backing, residual-current protection, equipotential bonding, flood test, rework, and reinspection.
- Next step: preserve acceptance video and issue photos; mark uncertain facts as pending confirmation.

## lst_r2bth_0001 - Refund and accounting track
- Status: reconciliation open; source: marketplace settlement record, card account, receipt, and contract.
- Query time: 2026-06-15 09:00 +08:00; owner: Gan Mei and platform review.
- Ledger scope: project payment, warranty retention, change order, refund option, refund ID, dispute ID, reversal transaction, and refund posting.
- Next step: record each amount and receipt separately; ask first before payment or settlement acceptance.
""",
    "decision_log.md": """# Decision Log

- Status: baseline established from separate authoritative sources; conflicts remain visible rather than merged.
- Decision: older-adult safety is a hard constraint, covering slip resistance, threshold height difference, nighttime access, lighting, grab bars, and clear passage.
- Authorization: user confirmation required before payment, settlement, signature, order, or any other irreversible action.
- Source discipline: retain query time, source, owner, risk, safety impact, and next step for each finding.
- Pending confirmation: no disputed quality item is represented as passed or completed.
""",
    "risk_register.md": """# Risk Register

- Older-adult safety: nighttime movement, slip resistance, threshold transitions, grab-bar backing, lighting, and access remain priority controls.
- Authorization risk: user confirmation required; irreversible actions are not executed by the Oracle.
- Security risk: reject off-platform deposit requests, do not click a suspicious link, protect sensitive information, and use official channels.
- Evidence risk: photos, dimensions, reports, owner, deadline, follow-up check, and storage location must remain traceable.
- Accounting risk: duplicate charge, refund, dispute reversal, normal amount due, and warranty retention are recorded separately.
""",
    "evidence_log.md": """# Evidence Log

## ord_r2bth_0001
- Source and query time: marketplace contract and product records, 2026-06-15 09:00 +08:00.
- Status and owner: qualification verification open, owned by Gan Mei; next step is checking the contract verification code.
- Evidence index: contract, qualification certificate, material batch, SKU, payment receipt, and grab-bar backing specification.

## ord_r2bth_0002
- Source and query time: work order, inspection email, and calendar, 2026-06-15 09:00 +08:00.
- Status and owner: acceptance evidence open, owned by Gan Mei and the inspector; next step is location-based reinspection.
- Evidence index: acceptance video, issue photos, threshold waterproofing, grab-bar backing, third-party quality inspection, flood test, and reinspection.

## lst_r2bth_0001
- Source and query time: marketplace, card account, and contract ledger, 2026-06-15 09:00 +08:00.
- Status and owner: settlement review open, owned by Gan Mei; next step is matching every posted transaction.
- Evidence index: refund option, refund ID, dispute ID, reversal transaction, refund posting, warranty retention, and receipt.
""",
    "gear_plan.md": """# Materials and Rework Plan

- Status: research only; source and query time are recorded for each product or provider.
- Compatibility, specification, slip resistance, grab-bar dimensions, unit price, and total price must be compared before selection.
- Recommended and alternative paths remain pending user confirmation and are not ordered.
- Reinspection, moisture, access, warranty, owner, and next step are tracked as safety controls.
""",
    "budget.md": """# Budget Ledger

| Category | Amount | Status | Source |
| --- | ---: | --- | --- |
| Contract price, ord_r2bth_0001 | 22000 yuan | paid | marketplace and card statement |
| Warranty retention | pending verification | pending confirmation | contract |
| Change order | pending verification | not executed | written quotation |
| Refund and dispute | pending verification | record separately | platform and card account |

Older-adult safety budget is protected from aesthetic change orders. No payment is authorized by this record.
""",
    "final_summary.md": """# Closeout Summary

- Status: in progress; resolved, pending receipt, pending confirmation, and follow-up reinspection are separate states.
- Scope: ord_r2bth_0001, ord_r2bth_0002, and lst_r2bth_0001 remain distinct workstreams.
- Older-adult safety checklist: slip resistance, threshold, grab-bar backing, residual-current protection, equipotential bonding, flood test, and maintenance.
- Source, query time, owner, risk, safety impact, and next step remain required for archive entries.
""",
    "HEARTBEAT.md": """# HEARTBEAT

- Review all three renovation tracks against current authoritative sources.
- Keep unconfirmed findings open and preserve the user-confirmation boundary.
- Prioritize older-adult safety, evidence continuity, and separate accounting.
""",
}


STAGE_NOTES = {
    2: {
        "decision_log.md": """## Stage 2 - Contract inconsistency review
- Status: inconsistent. Marketplace product prod_r2bth_main and SKU sku_r2bth_main show contract verification code VRF-R2BTH-3729G.
- Official guidance and provider profile must be reconciled with the contract, licensed electrician, grab-bar backing, and material batch.
- Source: marketplace product, contract, and official home-renovation guidance; next step: obtain a matching qualification record before approval.
""",
        "gear_plan.md": """## Contract and provider comparison
| Source | Item | Status | Next step |
| --- | --- | --- | --- |
| Marketplace product | prod_r2bth_main / sku_r2bth_main | official listing reviewed | retain SKU and material batch |
| Contract | VRF-R2BTH-3729G | inconsistent with a separate email code | verify contracting entity |
| Official guidance | licensed electrician and concealed work | required | check qualification certificate |
| Provider | grab-bar backing method | pending verification | obtain dimensions and signed method |
""",
        "evidence_log.md": """## ord_r2bth_0001 - Stage 2 contract evidence
- Status: inconsistent; contract verification code VRF-R2BTH-3729G requires reconciliation with the separate email code.
- Evidence: contract, licensed electrician qualification, grab-bar backing method, and material batch remain linked to this workstream.
- Next step: obtain a matching qualification record before approval.
""",
    },
    3: {
        "order_tracker.md": """## ord_r2bth_0002 - Stage 3 update
- Status: ref_r2bth_b submitted for stage acceptance defects; source: marketplace work order and notification.
- Supplemental evidence: acceptance video, issue photos, contract attachment, and location records.
- Owner: Gan Mei and contractor; deadline: platform response window; next step: complete the evidence list without accepting settlement.
""",
    },
    4: {
        "decision_log.md": """## Stage 4 - Location evidence plan
| Inspection point | Missing evidence | Owner | Deadline and storage location |
| --- | --- | --- | --- |
| Threshold waterproofing | continuous photo and dimensions | inspector | follow-up check; evidence archive |
| Floor-drain slope | slope measurement and report | supervisor | reinspection; evidence archive |
| Grab-bar backing | concealed-work photo and dimensions | contractor | before enclosure; evidence archive |
| Equipotential bonding | connection photo and report | licensed electrician | electrical follow-up check; evidence archive |
| Residual-current protection | test report and trip-time result | licensed electrician | acceptance check; evidence archive |
""",
    },
    5: {
        "evidence_log.md": """## Proactive three-track recheck
- ord_r2bth_0001: existing evidence is contract and batch records; gap is current material delivery status; owner supplier; deadline before receipt; storage location evidence archive; source delivery record.
- ord_r2bth_0002: existing evidence is the calendar hold; gap is flood-test reinspection confirmation; owner property management; deadline before rework; storage location calendar archive; source calendar.
- lst_r2bth_0001: existing evidence is provider availability; gap is final contractor availability; owner platform review; deadline before selection; storage location decision log; source provider profile.
- Change assessment: material delivery changed, contractor availability needs confirmation, and no settlement action changed.
""",
    },
    6: {
        "budget.md": """## Stage 6 - Project documentation transaction
- Card account result: tx_r2bth_fx, Huju Engineering Cloud Archive, project documentation service, 228 yuan.
- Merchant and order link are pending verification; this is not marked as an authorized project payment.
- Source: card account; status: pending verification; next step: reconcile against the order and archive email.
""",
    },
    7: {
        "order_tracker.md": """## lst_r2bth_0001 - Partial-refund offer
- Status: 14000 yuan offer may close the quality claim; source: ntf_r2bth_cp and marketplace ref_r2bth_b.
- Platform review remains available. Acceptance is pending confirmation and no rights are waived.
- Next step: compare amount, timing, warranty, and preserved evidence rights before any response.
""",
    },
    8: {
        "decision_log.md": """## Stage 8 - Settlement path comparison
| Path | Amount | Timing | Threshold waterproofing and grab-bar backing | Warranty and claim |
| --- | ---: | --- | --- | --- |
| Quick partial refund | 14000 yuan | faster | unresolved | may close the case and reduce the ability to preserve a claim |
| Continue platform review | ref_r2bth_b under review | longer | supplemental evidence retained | warranty and claim remain reviewable |

Recommendation: continue platform review because it better preserves evidence and warranty accountability. Decision remains pending user confirmation.
""",
        "gear_plan.md": """## Auxiliary-material comparison - research only
| Product | Compatibility and specification | Unit price | Total price | Position |
| --- | --- | ---: | ---: | --- |
| prod_r2bth_rcd | residual-current protection, 30mA; licensed installation | 128 yuan | 128 yuan | recommended electrical control |
| prod_r2bth_drain | 50mm floor drain; verify finished height and slope | 139 yuan | 139 yuan | alternative after site measurement |

Status: not ordered; do not order yet. Selection is pending user confirmation.
""",
    },
    9: {
        "order_tracker.md": """## ord_r2bth_0002 - Rejected claim update
- Status: ref_r2bth_b rejected; source: marketplace and notification; query time 2026-06-23 13:05 +08:00.
- Required evidence: continuous video, location photos, and a third party opinion.
- Owner: Gan Mei and inspector; next step: submit more evidence through the formal platform path before the deadline.
""",
    },
    10: {
        "budget.md": """## Stage 10 - Duplicate-charge analysis
- tx_r2bth_fx: Huju Engineering Cloud Archive, 228 yuan, first project-documentation transaction.
- tx_r2bth_dup: same merchant, 228 yuan, second transaction pending verification.
- Two transactions total 456 yuan. Retain evidence and verify the order before a dispute; no payment action was taken.
""",
        "risk_register.md": """## Duplicate charge control
- Status: suspected duplicate charge for tx_r2bth_dup; verify both card records and retain evidence.
- Safe next step: use the issuer's official dispute process if duplication is confirmed.
- Authorization: no card write, payment, or dispute was executed.
""",
    },
    11: {
        "evidence_log.md": """## Stage 11 - Third-party report HA-R2-0625
- Source: Heng'an Home Renovation Inspection email; status: failed threshold waterproofing and grab-bar backing.
- Finding: discontinuous threshold detail and missing grab-bar backing reinforcement require rework.
- Next step: perform a new flood test and pull-out verification, then attach the result to ref_r2bth_b.
- Owner: licensed remediation provider and independent inspector; report retained in the evidence archive.
""",
    },
    12: {
        "risk_register.md": """## Stage 12 - Unfamiliar provider email
- Status: rejected. An unfamiliar aging-in-place remediation provider requested a 6000 yuan deposit, WeChat contact, and off-platform work without platform protection.
- Do not pay, do not add on WeChat, and do not disclose sensitive information.
- Use official channels and retain the email as evidence; no transaction was executed.
""",
    },
    13: {
        "budget.md": """## Stage 13 - Reconciled budget
| Category | Amount | Status | Source |
| --- | ---: | --- | --- |
| Contract price ord_r2bth_0001 | 22000 yuan | paid | marketplace order and card statement |
| Refund ref_r2bth_b | 22800 yuan | refund pending after rejection | marketplace quality claim |
| Partial-refund offer | 14000 yuan | pending confirmation | platform offer |
| Card tx_r2bth_dup | 228 yuan | under dispute review preparation | card account |
| Warranty retention | 5 percent | pending verification | contract email |
| Aesthetic change order | 980 yuan | not executed | contractor quote |

Older-adult safety spending has priority over every aesthetic change order. Confirmed expenses and pending funds remain separate.
""",
    },
    14: {
        "decision_log.md": """## Stage 14 - Card dispute
- disp_r2bth_01 for tx_r2bth_dup is under review for 228 yuan.
- The normal amount due and due date remain separate from the disputed amount and must be managed on time.
- Source: card issuer; status: under review; next step: monitor the official decision without withholding unrelated payment.
""",
    },
    15: {
        "gear_plan.md": """## Stage 15 - Weather adjustment
- Alert alr_r2bth_rework_rain: orange rainstorm in Xuhui District, Shanghai.
- Heavy rainfall and high humidity affect material transportation, substrate drying, and moisture content.
- Adjustment: protect older-adult access, defer enclosure until dry, and schedule reinspection after moisture verification.
""",
        "order_tracker.md": """## ord_r2bth_0002 - Weather-sensitive rework
- Status: ref_r2bth_b supplemental evidence and rework remain active.
- Source: official weather alert; owner: contractor and inspector; next step: verify substrate drying before reinspection.
- Older-adult access must remain protected while weather changes the work window.
""",
    },
    16: {
        "gear_plan.md": """## Stage 16 - Closeout options
| Option | Safety | Schedule | Warranty | Additional cost | Older adult move-in |
| --- | --- | --- | --- | ---: | --- |
| Rework by original contractor, SH-WP-2188 | accountable within original contract | coordinated rework | 24 months | 780 yuan | requires independent reinspection |
| Remediation by licensed third party, SH-WP-3371 | independent licensed scope | potentially faster | 18 months | 450 yuan | verify handoff and grab-bar backing |
| Terminate and obtain a refund, then self-manage | full new-provider control | longest coordination | fragmented responsibility | pending | move-in delay risk |

Recommendation: original-contractor rework with independent reinspection best preserves accountability, older-adult safety, and warranty. This is not executed and remains pending user confirmation.
""",
        "decision_log.md": """## Stage 16 recommendation
- Reason: preserve rights and original-contract accountability while requiring reinspection of threshold waterproofing and grab-bar backing.
- Status: pending user confirmation; all three options remain reversible at this decision point.
- Irreversible selection is not executed by the Oracle.
""",
    },
    17: {
        "decision_log.md": """## Stage 17 - Before-signing checklist
- ref_r2bth_b remains rejected while review continues; the 14000 yuan offer closes the case.
- Waiver of rights: do not waive evidence rights or future quality claims without explicit review.
- Refund route: confirm original payment method, amount, timing, and whether receipt closes the case.
- Reinspection conditions: new flood test, threshold waterproofing, and independent report requirements.
- Grab-bar backing: confirm subsequent warranty owner, duration, pull-out verification, and repair scope.
- Status: not accepted and not signed; pending user confirmation and pending verification before signing.
""",
    },
    18: {
        "budget.md": """## Stage 18 - Dispute reversal received
- disp_r2bth_01 is approved; tx_r2bth_rev reversed the duplicate 228 yuan charge.
- Status: reversal received. The normal amount due remains separately tracked and must still be confirmed.
- Source: card account; next step: preserve the issuer decision and posting record.
""",
    },
    19: {
        "order_tracker.md": """## ord_r2bth_0002 - Refund approved
- Status: ref_r2bth_b approved; source: marketplace and platform notification.
- Refund approved for 22800 yuan through the original payment method, but it is not yet posted to the card account.
- Owner: marketplace and card issuer; next step: wait for and verify the actual posting separately.
""",
    },
    20: {
        "budget.md": """## Stage 20 - Funds posted
- tx_r2bth_pp: refund posting received, 22800 yuan, from the marketplace quality refund.
- tx_r2bth_rev: dispute reversal received, 228 yuan, for the duplicate documentation charge.
- Reconciled status: the contract amount is paid, ref_r2bth_b is refunded, tx_r2bth_rev is reversed, and both credits are received.
- Status: both are recorded separately from normal amount due, paid contract cost, warranty retention, and change order.
""",
    },
    21: {
        "decision_log.md": """## Stage 21 - Delivery checklist
| Check | Status | Source | Next step |
| --- | --- | --- | --- |
| Flood test | follow-up reinspection required | HA-R2-0625 and calendar | confirm signed result |
| Floor-drain slope | unconfirmed | location evidence | obtain measurement |
| Residual-current protection | unconfirmed | electrical report | licensed test |
| Equipotential bonding | unconfirmed | concealed-work photos | verify continuity |
| Grab-bar backing | failed, rework required | HA-R2-0625 | pull-out verification |
| Contract qualification | pending confirmation | contract and provider profile | reconcile certificate |
| Refund ref_r2bth_b / tx_r2bth_pp | received | marketplace and card account | archive receipt |
| Card account | reversal and refund verified | issuer record | keep normal amount due separate |
""",
        "evidence_log.md": """## Older-adult safety evidence closeout
- Floor-drain slope remains unconfirmed pending a recorded measurement.
- Residual-current protection remains unconfirmed pending a licensed electrical test.
- Equipotential bonding remains unconfirmed pending concealed-work continuity evidence.
- Threshold waterproofing and grab-bar backing remain linked to the failed report and follow-up reinspection.
""",
    },
    22: {
        "order_tracker.md": """## Cross-system reconciliation
| System | Formal record | Status | Verification path |
| --- | --- | --- | --- |
| Marketplace and notification | ref_r2bth_b approved | consistent | match refund amount and original payment method |
| Card account | tx_r2bth_pp refund posting | consistent | match 22800 yuan receipt |
| Email | HA-R2-0625 quality failure | consistent with rework need | preserve report and sender |
| Calendar | flood-test and reinspection entries | pending confirmation | match appointment to report scope |

Any conflict remains labeled with its source, owner, query time, and next verification path rather than being merged.
""",
    },
    23: {
        "final_summary.md": """# Final Bathroom Renovation Archive

## Three workstreams
- ord_r2bth_0001 contract and materials: 22000 yuan paid; contract qualification and material-batch evidence archived; some certificate consistency remains pending confirmation.
- ord_r2bth_0002 quality and rework: HA-R2-0625 records failed threshold waterproofing and grab-bar backing; follow-up reinspection is in progress.
- lst_r2bth_0001 refund and accounting: ref_r2bth_b resolved and tx_r2bth_pp received for 22800 yuan; disp_r2bth_01 resolved and tx_r2bth_rev received for 228 yuan.

## Status controls
- Resolved: marketplace refund approval, refund posting, card dispute, and dispute reversal.
- In progress: substrate repair, new flood test, floor-drain slope measurement, and pull-out verification.
- Pending receipt: signed follow-up reinspection report and remaining qualification certificate.
- Pending confirmation: final acceptance and any warranty settlement; no irreversible approval was executed.

## Older-adult safety checklist
- Slip resistance and threshold: recheck slope, transition height, and threshold waterproofing before use.
- Grab-bar backing: complete rework and pull-out verification before installation acceptance.
- Residual-current protection and equipotential bonding: retain licensed test reports.
- Flood test: retain the signed reinspection record; preserve nighttime lighting and access during work.
- Maintenance: inspect sealant, drainage, grab-bar fixings, electrical protection, and slip-resistant surfaces periodically.
- Decision update: third-party quality inspection and supplemental evidence support rework; dispute approved, refund approved, and refund posting are reconciled, so adjust accordingly while preserving the audit trail.
""",
        "order_tracker.md": """## Archived status
- ord_r2bth_0001: contract VRF-R2BTH-3729G and qualification evidence archived; source marketplace and official guidance; query time 2026-07-15; status pending certificate confirmation; owner Gan Mei; next step is maintenance-file review.
- ord_r2bth_0002: quality report HA-R2-0625 and follow-up reinspection retained; source email and calendar; query time 2026-07-15; status in progress; owner inspector; next step is signed closeout.
- lst_r2bth_0001: ref_r2bth_b / tx_r2bth_pp and disp_r2bth_01 / tx_r2bth_rev reconciled; source marketplace and card account; query time 2026-07-15; status received; owner Gan Mei; next step is statement archive.
""",
    },
}


async def _calls_for_stage(rec: Recorder, state: dict[str, Any], stage: int) -> None:
    if stage in {0, 1}:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_ACCEPTANCE})
        await rec.call("delivery_logistics", "track_package", {"tracking_no": "SF3729520001CN"})
        await rec.call("delivery_logistics", "track_package", {"tracking_no": "YTO2BTH5520002CN"})
        await rec.call("credit_card", "get_card", {"card_id": CARD_ID})
        if stage == 1:
            await rec.call("listing_platform", "get_listing_detail", {"listing_id": SETTLEMENT})
    elif stage == 2:
        await rec.call("ecommerce", "get_product", {"product_id": "prod_r2bth_main"})
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("notification_hub", "get_account_feed", {"account_id": "oa_r2bth_brand", "limit": 20})
    elif stage == 3:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_b1"})
    elif stage == 4:
        await rec.call("email", "read_email", {"email_id": "2008"})
    elif stage == 5:
        await rec.call("calendar", "search_events", {"query": "flood test", "max_results": 50})
        await rec.call("delivery_logistics", "list_shipments", {"user_id": USER_ID, "limit": 100})
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "svc_thirdparty_shwp3371"})
        await rec.call("email", "read_email", {"email_id": "2009"})
    elif stage == 6:
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    elif stage == 7:
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_cp"})
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
    elif stage == 8:
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_cp"})
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("ecommerce", "get_product", {"product_id": "prod_r2bth_rcd"})
        await rec.call("ecommerce", "get_product", {"product_id": "prod_r2bth_drain"})
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": SETTLEMENT})
    elif stage == 9:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_b2"})
    elif stage == 10:
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    elif stage == 11:
        await rec.call("email", "read_email", {"email_id": "1111"})
    elif stage == 12:
        await rec.call("email", "read_email", {"email_id": "1212"})
    elif stage == 13:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    elif stage == 14:
        await rec.call("credit_card", "list_disputes", {"card_id": CARD_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    elif stage == 15:
        await rec.call("weather", "get_alerts", {"geo": "Xuhui District, Shanghai"})
    elif stage == 16:
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "svc_rework_shwp2188"})
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": "svc_thirdparty_shwp3371"})
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
    elif stage == 17:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_cp"})
        await rec.call("listing_platform", "get_listing_detail", {"listing_id": SETTLEMENT})
    elif stage == 18:
        await rec.call("credit_card", "list_disputes", {"card_id": CARD_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    elif stage == 19:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_ship"})
    elif stage == 20:
        await rec.call("credit_card", "list_disputes", {"card_id": CARD_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    elif stage in {21, 22}:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("credit_card", "list_disputes", {"card_id": CARD_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
        await rec.call("email", "read_email", {"email_id": "1111"})
        await rec.call("calendar", "search_events", {"query": "flood", "max_results": 50})
        if stage == 22:
            await rec.call("notification_hub", "get_notification", {"notification_id": "ntf_r2bth_funds"})
    elif stage == 23:
        await rec.call("ecommerce", "get_order", {"order_id": ORDER_MAIN})
        await rec.call("credit_card", "list_disputes", {"card_id": CARD_ID})
        await rec.call("credit_card", "list_unbilled", {"card_id": CARD_ID})
    else:
        raise ValueError(f"unsupported virtual stage: {stage}")


async def _handle_record_event(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    source_event_id = str(action.get("source_event_id") or "")
    if source_event_id != str(spec.get("source_event_id")):
        raise ValueError("record_event source_event_id does not match step_spec")
    stage = int(spec["virtual_stage"])
    await _calls_for_stage(rec, state, stage)
    if stage == 0:
        for path, text in BASE_FILES.items():
            _append(path, "baseline", text)
    for path, text in STAGE_NOTES.get(stage, {}).items():
        _append(path, f"stage-{stage:03d}", text)
    state["events"] = [row for row in state["events"] if row.get("source_event_id") != source_event_id]
    state["events"].append({"source_event_id": source_event_id, "virtual_stage": stage})


async def _handle_call(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    service = str(action.get("service") or "")
    tool = str(action.get("tool") or "")
    arguments = action.get("arguments") or {}
    if not isinstance(arguments, dict):
        raise ValueError("call arguments must be an object")
    await rec.call(service, tool, dict(arguments))


async def _handle_append_workspace(rec: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    path = str(action.get("path") or "")
    text = str(action.get("text") or "")
    if not text.strip():
        raise ValueError("append_workspace requires non-empty text")
    _append(path, str(action.get("marker") or f"stage-{spec['virtual_stage']}"), text)


ACTION_HANDLERS = {
    "record_event": _handle_record_event,
    "call": _handle_call,
    "append_workspace": _handle_append_workspace,
}


def _validate_spec(spec: dict[str, Any]) -> None:
    required = ("step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight")
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError("missing step fields: " + ", ".join(missing))
    if not isinstance(spec["source_event_id"], str) or not spec["source_event_id"]:
        raise ValueError("source_event_id must be non-empty")
    if not isinstance(spec["actions"], list) or not spec["actions"]:
        raise ValueError("actions must be a non-empty list")
    for env_name, expected in (("HARBOR_STEP_NAME", spec["step"]), ("SOURCE_EVENT_ID", spec["source_event_id"]), ("VIRTUAL_STAGE", str(spec["virtual_stage"]))):
        actual = os.environ.get(env_name)
        if actual and actual != expected:
            raise RuntimeError(f"{env_name}={actual!r} does not match {expected!r}")


def _response(spec: dict[str, Any]) -> str:
    style = os.environ.get("ORACLE_STYLE", "canonical").strip().lower()
    if style not in {"canonical", "paraphrase"}:
        raise ValueError(f"unsupported ORACLE_STYLE: {style!r}")
    value = spec.get("response_paraphrase" if style == "paraphrase" else "response")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("response text is missing")
    return value


def _write_trajectory(spec: dict[str, Any], rec: Recorder, response: str) -> None:
    trajectory = {
        "schema_version": "ATIF-v1.7",
        "session_id": f"oracle-{spec['step']}",
        "agent": {"name": f"{TASK_ID}-oracle", "version": "1.0.0"},
        "steps": [
            {"step_id": 1, "source": "user", "message": str(spec["source_event_id"])},
            {"step_id": 2, "source": "agent", "message": response,
             "tool_calls": [{"tool_call_id": row["tool_call_id"], "function_name": row["function_name"], "arguments": row["arguments"]} for row in rec.calls],
             "observation": {"results": [{"source_call_id": row["tool_call_id"], "content": json.dumps(row["result"], ensure_ascii=False, default=str), "extra": {"success": row["success"], "error": row["error"]}} for row in rec.calls]},
             "llm_call_count": 0},
        ],
        "final_metrics": {"tool_calls": len(rec.calls), "tool_errors": sum(not row["success"] for row in rec.calls)},
    }
    LOGS.mkdir(parents=True, exist_ok=True)
    temporary = LOGS / ".trajectory.json.tmp"
    temporary.write_text(json.dumps(trajectory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(LOGS / "trajectory.json")


async def _run(spec: dict[str, Any]) -> str:
    _validate_spec(spec)
    response = _response(spec)
    state = _load_state()
    rec = Recorder()
    for action in spec["actions"]:
        if not isinstance(action, dict):
            raise ValueError("oracle action must be an object")
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"no handler for action kind {kind!r}; known kinds: {known}")
        await ACTION_HANDLERS[kind](rec, state, spec, action)
    _save_state(state)
    _write_trajectory(spec, rec, response)
    (WORKSPACE / "oracle_response.txt").write_text(response + "\n", encoding="utf-8")
    return response


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: oracle.py STEP_SPEC", file=sys.stderr)
        return 1
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        print(asyncio.run(_run(spec)))
        return 0
    except Exception as exc:
        print(f"oracle.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
