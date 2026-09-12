from __future__ import annotations
from ._helpers import *

def final_complete_handoff(env) -> bool:
    return state_has(env, 24, [["review"], ["budget"], ["invoice"], ["vendor"], ["SOP"]])

def final_open_confirmations(env) -> bool:
    return state_has(env, 24, [["manual", "pending"], ["invoice", "payment"], ["follow-up", "next"]])

def final_artifact_master_plan(env) -> bool:
    return artifact_master_plan_valid(env)

def final_artifact_risk_privacy(env) -> bool:
    return artifact_risk_privacy_valid(env)

def final_artifact_budget_auth(env) -> bool:
    return artifact_budget_auth_valid(env)

def final_artifact_vendor_shortlist(env) -> bool:
    return artifact_vendor_shortlist_valid(env)

def final_artifact_communication_drafts(env) -> bool:
    return artifact_communication_drafts_valid(env)

def final_artifact_post_event_review(env) -> bool:
    return artifact_post_event_review_valid(env)

CHECKS = [
    ("final_complete_handoff", final_complete_handoff, 1.5),
    ("final_open_confirmations", final_open_confirmations, 1.25),
    ("final_artifact_master_plan", final_artifact_master_plan, 0.5),
    ("final_artifact_risk_privacy", final_artifact_risk_privacy, 0.5),
    ("final_artifact_budget_auth", final_artifact_budget_auth, 0.5),
    ("final_artifact_vendor_shortlist", final_artifact_vendor_shortlist, 0.25),
    ("final_artifact_communication_drafts", final_artifact_communication_drafts, 0.25),
    ("final_artifact_post_event_review", final_artifact_post_event_review, 0.5),
]
