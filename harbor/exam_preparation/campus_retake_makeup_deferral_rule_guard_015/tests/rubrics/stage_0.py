from . import _helpers as h

def s0_notion_hub_created(env):
    return h.s0_notion_hub_created(env)

def s0_subscription_or_watch_created(env):
    return h.s0_subscription_or_watch_created(env)

CHECKS = [
    ("s0_notion_hub_created", s0_notion_hub_created, 1.0),
    ("s0_subscription_or_watch_created", s0_subscription_or_watch_created, 1.25),
]
