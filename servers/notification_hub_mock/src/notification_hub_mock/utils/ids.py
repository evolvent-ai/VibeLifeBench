def subscription_id(seq: int) -> str:
    return f"sub_{seq:06d}"


def notification_id(seq: int) -> str:
    return f"ntf_{seq:08d}"


def alert_id(seq: int) -> str:
    return f"alr_{seq:06d}"
