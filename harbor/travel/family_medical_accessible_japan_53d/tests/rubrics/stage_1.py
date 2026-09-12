from __future__ import annotations

from ._helpers import _tool_call_matches, _workspace_file_text, text_has


def s1_profile_was_read_and_persisted(env) -> bool:
    searched = _tool_call_matches(
        env,
        ["notion__api-post-search"],
        lambda a: any(x in str(a.get("query") or "").lower() for x in ("household", "mobility", "parents", "family", "access")),
        stage=1,
    )
    read_blocks = _tool_call_matches(
        env,
        ["notion__api-get-block-children"],
        lambda a: bool(a.get("block_id")),
        stage=1,
    )
    risk = _workspace_file_text(env, "risk_register.md")
    durable = text_has(
        risk,
        [["father", "paternal", "dad"], ["mother", "maternal", "mom"], ["mobility", "accessibility", "walking"], ["passport", "identity document", "travel document"], ["privacy", "plaintext", "private data"]],
    )
    return bool(searched and read_blocks and durable)


CHECKS = [("s1_profile_was_read_and_persisted", s1_profile_was_read_and_persisted, 2.0)]
