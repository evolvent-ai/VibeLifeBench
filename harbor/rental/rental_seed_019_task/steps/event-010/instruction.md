[2026-07-16T13:00:00+08:00] Housing catalog update

The relocation candidate pool is now available. Some listings have complete information, while others still require verification of the floor, elevator, room partitioning, or viewing window.

For continuity, treat short `lst_tj_19xx` IDs (not bulk `lst_tj_pool_*` rows) as the tracked candidate set: the lowest-numbered active qualifying entry is primary, and any separately viewing-authorized candidate remains a conditional alternative until the user changes the ranking.

Save the primary entry on the listing platform, record its status and next step in `MOVE_CANDIDATE_TRACKER.md`, and label unknown facts as pending verification.
