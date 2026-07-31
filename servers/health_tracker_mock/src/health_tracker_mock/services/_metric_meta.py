"""Metric type metadata: valid types, default units, descriptive normal ranges.

Normal ranges here are used ONLY to flag readings as out-of-typical-range in a
purely descriptive way (see ``AlertService``). They are not diagnostic
thresholds and the server never prescribes action — see SPEC.md §Safety.
"""

METRIC_TYPES = (
    "weight",
    "steps",
    "heart_rate",
    "sleep_minutes",
    "blood_pressure",
    "body_fat",
    "finger_pain",
    "score",
)

# Default unit per metric type when the caller omits ``unit``.
DEFAULT_UNITS = {
    "weight": "g",
    "steps": "count",
    "heart_rate": "bpm",
    "sleep_minutes": "min",
    "blood_pressure": "mmHg",
    "body_fat": "percent",
    "finger_pain": "score",
    "score": "score",
}

# Descriptive "typical resting" ranges for adults, keyed by metric type.
# (low, high) on the metric's stored numeric value. ``None`` = not range-checked.
# blood_pressure uses systolic (the stored numeric ``value``).
TYPICAL_RANGES = {
    "heart_rate": (50.0, 100.0),
    "blood_pressure": (90.0, 140.0),  # systolic mmHg
    "body_fat": (8.0, 30.0),
    "weight": None,
    "steps": None,
    "sleep_minutes": None,
    "finger_pain": None,
    "score": None,
}
