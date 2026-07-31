from __future__ import annotations

from pathlib import Path


HF_ROOT = Path(__file__).resolve().parents[1]


def _workspace_file(task: str, name: str) -> str:
    return (HF_ROOT / "eval_set" / task / "workspace" / name).read_text(
        encoding="utf-8"
    )


def test_civil_service_contract_routes_cross_cutting_evidence_to_scored_ledgers() -> None:
    text = _workspace_file(
        "exam_preparation/civil_service_written_to_interview_audit", "AGENTS.md"
    )
    required_phrases = (
        "补充公告等来源事实先写入 `source_evidence.md`",
        "同步更新 `qualification_matrix.md`",
        "日历新增或变更必须写入 `calendar_change_log.md`",
        "授权状态写入 `auth_log.md`",
        "隐私与最小披露写入 `privacy_log.md`",
        "咨询或通知草稿写入 `communication_log.md`",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_broadcast_contract_makes_stage_marker_requirement_globally_visible() -> None:
    text = _workspace_file(
        "fitness/broadcast_exam_posture_breathing_32d", "AGENTS.md"
    )
    assert "每个 stage 的持久化更新都要标注本次可见的阶段编号" in text
    for marker in ("`S7`", "`Stage 7`", "`阶段7`"):
        assert marker in text


def test_career_contracts_define_minor_units_without_requiring_raw_data_dumps() -> None:
    tasks = (
        "career/career_espp_refund_recovery",
        "career/career_equity_buyback_recovery",
    )
    for task in tasks:
        text = _workspace_file(task, "AGENTS.md")
        assert "`*_minor`" in text
        assert "整数分" in text
        assert "可读的元金额" in text
        assert "不等于粘贴完整 JSON 或整张原始表" in text
