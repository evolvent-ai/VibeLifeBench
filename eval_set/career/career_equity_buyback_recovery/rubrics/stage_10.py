"""Stage 10 — 在正确 HR 原线程生成唯一未发送核算草稿。"""
from __future__ import annotations

from ._helpers import norm_num, sent_emails, stage_call_matches, text_has, unique_message

HR = "hr.songke@yiweicloud.com"
REVISE_MESSAGE_ID = "<20260624-revise@yiweicloud.com>"
HISTORY_MESSAGE_ID = "<20240520-rsu-plan@yiweicloud.com>"
_BAD_BASE = ("股权回购差额基数按月均工资", "按工作年限计算股权", "按工龄计算股权")


def s10_demand_letter_drafted(env) -> bool:
    if not stage_call_matches(env, 10, "read_email", {"email_id": "103"}):
        return False
    draft = unique_message(
        env,
        folder="drafts",
        recipient=HR,
        in_reply_to=REVISE_MESSAGE_ID,
        required_groups=[
            [HISTORY_MESSAGE_ID], ["已归属"], ["基准日"], ["收盘价", "市场价"],
            ["参考公允价值"], ["公司方案"], ["差额"],
            ["art_cc_509"], ["art_cc_496"], ["art_cc_497"], ["art_cc_151"],
            ["诉求", "补足"], ["保留", "继续主张"],
        ],
    )
    if not draft or str(draft.get("date") or "") < "2026-06-24T09:55:00Z":
        return False
    body = str(draft.get("body_text") or draft.get("body") or "").lower()
    corpus = norm_num(body)
    if not all(value in corpus for value in ("5000", "59.42", "297100", "200100", "97000")):
        return False
    if any(term in body for term in _BAD_BASE):
        return False
    for msg in sent_emails(env):
        if str(msg.get("in_reply_to") or "") == REVISE_MESSAGE_ID:
            return False
    return text_has(body, [["不是股权价差基数", "工资只作收入旁证", "工资仅作收入旁证"]])


CHECKS = [("s10_demand_letter_drafted", s10_demand_letter_drafted, 3.0)]
