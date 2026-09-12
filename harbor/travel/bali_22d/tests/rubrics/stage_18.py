"""Stage 18: route incidents and venue alternatives must both be verified and persisted."""
from __future__ import annotations

from .shared._helpers import _tool_call_matches, workspace_file_content


def s18_indoor_plan_uses_verified_places(env) -> bool:
    venue_search = _tool_call_matches(
        env,
        "maps",
        "search_places",
        lambda a: any(x in str(a.get("query") or "").casefold() for x in ("ubud", "indoor", "wellness", "cafe", "palace")),
        stage=18,
    )
    flooded_route = _tool_call_matches(
        env,
        "maps",
        "get_traffic_estimate",
        lambda a: "2026-06-20" in str(a.get("depart_at") or "") and any(x in str(a).casefold() for x in ("ubud", "pl_ubud_palace")),
        stage=18,
    )
    text = (workspace_file_content(env, "/workspace/itinerary.md") + "\n" + workspace_file_content(env, "/workspace/risk_register.md")).casefold()
    known = ("the yoga barn", "como shambhala", "ubud royal palace", "cafe pomegranate", "locavore")
    venues = sum(1 for venue in known if venue in text) >= 2
    incidents = all(x in text for x in ("evt_ubud_flood_20260620", "evt_ubud_flood2_20260620"))
    closed = "campuhan" in text and any(x in text for x in ("closed", "cancel", "closed", "cancel"))
    dated = all(x in text for x in ("2026-06-20", "2026-06-21"))
    return bool(venue_search and flooded_route and venues and incidents and closed and dated)


CHECKS = [("s18_indoor_plan_uses_verified_places", s18_indoor_plan_uses_verified_places, 2.5)]
