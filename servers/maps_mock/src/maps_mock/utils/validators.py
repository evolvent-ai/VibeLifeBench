from typing import Iterable

from .exceptions import InvalidArgumentError

_MODES = {"driving", "walking", "transit", "bicycling"}

# Public category enum. Extends the SPEC §3.3 base set with the medical /
# attraction categories that actually exist in the seed (so agents can filter
# for "hospital" / "clinic" / "pharmacy" — required by the stage-17 Kyoto
# "nearest clinic" flow).
_CATEGORIES = {
    "temple", "museum", "restaurant", "station", "airport",
    "hotel", "park", "shrine", "shopping", "viewpoint",
    "hospital", "clinic", "pharmacy", "attraction",
}


def validate_mode(mode: str) -> str:
    if mode not in _MODES:
        raise InvalidArgumentError(
            f"invalid mode '{mode}', expected one of {sorted(_MODES)}"
        )
    return mode


def validate_category(category: str) -> str:
    if category is None:
        return category
    if category not in _CATEGORIES:
        raise InvalidArgumentError(
            f"invalid category '{category}', expected one of {sorted(_CATEGORIES)}"
        )
    return category


def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


def ensure_list_size(items: Iterable, lo: int, hi: int, name: str) -> list:
    lst = list(items)
    if len(lst) < lo or len(lst) > hi:
        raise InvalidArgumentError(
            f"{name} must have between {lo} and {hi} items, got {len(lst)}"
        )
    return lst
