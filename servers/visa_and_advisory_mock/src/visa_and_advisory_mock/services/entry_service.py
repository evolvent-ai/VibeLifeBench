"""check_entry_requirements logic with fallback chain."""

from typing import Any, Dict, List, Optional

from ..backends.entry_backend import EntryBackend
from ..models.entry import EntryRequirement
from ..utils.exceptions import ValidationError
from ..utils.validators import normalize_country_code, validate_purpose


_DEFAULT_DOCS = ["passport"]


def _entry_to_dict(entry: EntryRequirement) -> Dict[str, Any]:
    return {
        "visa_required": bool(entry.visa_required),
        "allowed_stay_days": int(entry.allowed_stay_days),
        "passport_validity_months": int(entry.passport_validity_months),
        "docs_needed": list(entry.docs_needed),
        "notes": entry.notes,
    }


class EntryService:
    def __init__(self, entry_backend: EntryBackend):
        self.entry_backend = entry_backend

    def check(
        self,
        nationality: str,
        destination: str,
        purpose: str,
        transit_countries: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        nat = normalize_country_code(nationality)
        dest = normalize_country_code(destination)
        purpose = validate_purpose(purpose)

        primary = self.entry_backend.get(nat, dest, purpose)
        fallback_used = False
        if primary is None and purpose != "tourism":
            primary = self.entry_backend.get(nat, dest, "tourism")
            if primary is not None:
                fallback_used = True

        if primary is not None:
            payload: Dict[str, Any] = {
                "nationality": nat,
                "destination": dest,
                "purpose": purpose,
                **_entry_to_dict(primary),
                "source": "seeded_matrix",
            }
        else:
            payload = {
                "nationality": nat,
                "destination": dest,
                "purpose": purpose,
                "visa_required": True,
                "allowed_stay_days": 0,
                "passport_validity_months": 6,
                "docs_needed": list(_DEFAULT_DOCS),
                "notes": "No seeded rule; treat as visa-required.",
                "source": "default_fallback",
            }

        if fallback_used:
            payload["fallback"] = True

        transit_advice: List[Dict[str, Any]] = []
        for code in transit_countries or []:
            try:
                tc = normalize_country_code(code)
            except ValidationError:
                continue
            row = self.entry_backend.get(nat, tc, "transit")
            if row is None:
                transit_advice.append(
                    {
                        "country": tc,
                        "visa_required": True,
                        "max_hours": 0,
                        "notes": "No seeded transit rule; assume transit visa required.",
                    }
                )
            else:
                transit_advice.append(
                    {
                        "country": tc,
                        "visa_required": bool(row.visa_required),
                        "max_hours": int(row.allowed_stay_days) * 24,
                        "notes": row.notes,
                    }
                )

        if transit_advice:
            payload["transit_advice"] = transit_advice

        return payload
