"""Stage 15 — track the arrival deadline and principal-only milestones in calendar state."""
from __future__ import annotations
from ._helpers import agent_used_any_tool, calendar_has_distinct_events, calendar_has_event


def s15_deadline_tracked(env) -> bool:
    queried = agent_used_any_tool(env, [('calendar', 'list_events'), ('calendar', 'get_event')], stage=15)
    deadline = calendar_has_event(env, ['Report to work'], before='2026-07-20')
    return queried and deadline


def s15_calendar_principal_milestones(env) -> bool:
    return calendar_has_distinct_events(env, (
        ('Mingfa', 'viewing', 'principal'),
        ('Mingfa', 'lease signing', 'principal'),
        ('Mingfa', 'payment', 'principal'),
    ), before='2026-07-20')

CHECKS = [('s15_deadline_tracked', s15_deadline_tracked, 0.1863799283154122), ('s15_calendar_principal_milestones', s15_calendar_principal_milestones, 0.1863799283154122)]
