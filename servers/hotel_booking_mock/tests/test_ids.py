from __future__ import annotations

import sys
import warnings
from datetime import datetime
from pathlib import Path

SERVER_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SERVER_ROOT / "src"))

from hotel_booking_mock.utils.ids import now_iso_z  # noqa: E402


def test_now_iso_z_is_parseable_without_deprecation_warnings() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        value = now_iso_z()

    assert not [item for item in caught if issubclass(item.category, DeprecationWarning)]
    assert value.endswith("Z")
    assert datetime.fromisoformat(value.removesuffix("Z") + "+00:00").tzinfo is not None
