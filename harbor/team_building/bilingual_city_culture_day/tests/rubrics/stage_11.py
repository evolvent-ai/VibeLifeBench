from __future__ import annotations
from ._helpers import *


def s11_menu_translation_discovered(env) -> bool:
    return (
        used_tool_with_value(
            env,
            11,
            "email",
            "search_emails",
            ["menu translation correction", "pork-free does not equal halal", "gluten intolerance must not be labeled as ordinary vegetarian", "pause external sending"],
        )
        and used_tool(env, 11, "email", "save_draft")
        and draft_matches(
            env,
            "menu correction",
            "lingnan-tasting",
            ["pork-free does not equal halal", "gluten intolerance", "shared-utensil", "pause external sending"],
            ["guarantee safety", "absolutely safe"],
            stage=11,
        )
    )


CHECKS = [("s11_menu_translation_discovered", s11_menu_translation_discovered, 1.75)]
