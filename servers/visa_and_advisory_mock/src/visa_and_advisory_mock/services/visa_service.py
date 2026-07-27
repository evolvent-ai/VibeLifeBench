"""Visa product listing + application lifecycle."""

import calendar
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..backends.entry_backend import EntryBackend
from ..backends.visa_backend import VisaBackend
from ..models.visa import ApplicationDocument, VisaApplication, VisaProduct
from ..utils.exceptions import InvalidState, NotFound, ValidationError
from ..utils.ids import IdGenerator
from ..utils.validators import (
    normalize_country_code,
    validate_doc_kind,
)


def _now_iso() -> str:
    # Wall-clock timestamp used for ``uploaded_at``, ``created_at``,
    # ``updated_at`` audit fields.
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _parse_iso_date(value: Any) -> Optional[datetime]:
    """Parse a YYYY-MM-DD or full ISO-8601 string to a naive datetime."""
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return None


def _add_months(dt: datetime, months: int) -> datetime:
    """Return dt shifted by `months` calendar months (clamped day-of-month)."""
    year = dt.year + (dt.month - 1 + months) // 12
    month = (dt.month - 1 + months) % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return dt.replace(year=year, month=month, day=min(dt.day, last_day))


def _required_form_fields(product: VisaProduct) -> List[str]:
    fields = product.form_schema.get("fields") or []
    return [f["name"] for f in fields if f.get("required")]


def _required_docs(product: VisaProduct) -> List[str]:
    return list(product.form_schema.get("required_docs") or [])


def _product_summary(p: VisaProduct) -> Dict[str, Any]:
    return {
        "product_id": p.product_id,
        "name": p.name,
        "processing_time_days": int(p.processing_time_days),
        "fee_amount": int(p.fee_amount),
        "fee_currency": p.fee_currency,
        "delivery": p.delivery,
    }


def _product_detail(p: VisaProduct) -> Dict[str, Any]:
    return {
        "product_id": p.product_id,
        "destination": p.destination,
        "nationality": p.nationality,
        "name": p.name,
        "processing_time_days": int(p.processing_time_days),
        "fee_amount": int(p.fee_amount),
        "fee_currency": p.fee_currency,
        "delivery": p.delivery,
        "form_schema": p.form_schema,
    }


def _document_summary(doc: ApplicationDocument) -> Dict[str, Any]:
    return {
        "doc_id": doc.doc_id,
        "kind": doc.kind,
        "ref": doc.ref,
        "uploaded_at": doc.uploaded_at,
    }


def _application_summary(app: VisaApplication) -> Dict[str, Any]:
    return {
        "application_id": app.application_id,
        "product_id": app.product_id,
        "status": app.status,
        "decision_day": app.decision_day,
    }


def _application_detail(app: VisaApplication, docs: List[ApplicationDocument]) -> Dict[str, Any]:
    return {
        "application_id": app.application_id,
        "user_id": app.user_id,
        "product_id": app.product_id,
        "status": app.status,
        "applicant": app.applicant,
        "answers": app.answers,
        "decision_day": app.decision_day,
        "decision_note": app.decision_note,
        "evisa_doc_ref": app.evisa_doc_ref,
        "documents": [_document_summary(d) for d in docs],
        "history": list(app.history),
        "created_at": app.created_at,
        "updated_at": app.updated_at,
    }


class VisaService:
    def __init__(
        self,
        visa_backend: VisaBackend,
        ids: IdGenerator,
        entry_backend: Optional[EntryBackend] = None,
    ):
        self.visa_backend = visa_backend
        self.ids = ids
        self.entry_backend = entry_backend

    # ---- products ----------------------------------------------------------

    def list_products(self, nationality: str, destination: str) -> List[Dict[str, Any]]:
        nat = normalize_country_code(nationality)
        dest = normalize_country_code(destination)
        products = self.visa_backend.list_products_for(dest, nat)
        return [_product_summary(p) for p in products]

    def get_product(self, product_id: str) -> Dict[str, Any]:
        product = self.visa_backend.get_product(product_id)
        if product is None:
            raise NotFound(f"product {product_id!r} not found", code="product_not_found")
        return _product_detail(product)

    # ---- applications ------------------------------------------------------

    def start_application(
        self, product_id: str, applicant_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        product = self.visa_backend.get_product(product_id)
        if product is None:
            raise NotFound(f"product {product_id!r} not found", code="product_not_found")

        applicant_profile = dict(applicant_profile or {})
        user_id = str(applicant_profile.get("user_id") or "anon")

        now = _now_iso()
        app_id = self.ids.application_id()
        app = VisaApplication(
            application_id=app_id,
            user_id=user_id,
            product_id=product_id,
            status="draft",
            applicant=applicant_profile,
            answers={},
            decision_day=None,
            decision_note=None,
            evisa_doc_ref=None,
            history=[{"day": None, "from": None, "to": "draft", "note": "application created"}],
            created_at=now,
            updated_at=now,
        )
        self.visa_backend.insert_application(app)

        return {
            "application_id": app_id,
            "status": "draft",
            "form_fields_required": _required_form_fields(product),
            "required_docs": _required_docs(product),
        }

    def upload_document(
        self, application_id: str, kind: str, doc_ref: str
    ) -> Dict[str, Any]:
        app = self.visa_backend.get_application(application_id)
        if app is None:
            raise NotFound(f"application {application_id!r} not found")
        validate_doc_kind(kind)
        if not isinstance(doc_ref, str) or not doc_ref:
            raise ValidationError("doc_ref must be a non-empty string")

        doc_id = self.ids.document_id()
        doc = ApplicationDocument(
            doc_id=doc_id,
            application_id=application_id,
            kind=kind,
            ref=doc_ref,
            uploaded_at=_now_iso(),
        )
        self.visa_backend.insert_document(doc)
        # touch updated_at on the application
        app.updated_at = _now_iso()
        self.visa_backend.update_application(app)
        return {
            "ok": True,
            "doc_id": doc_id,
            "application_id": application_id,
            "kind": kind,
        }

    def submit_application(
        self,
        application_id: str,
        answers: Dict[str, Any],
        docs_refs: List[str],
        payment_method_id: str,
    ) -> Dict[str, Any]:
        app = self.visa_backend.get_application(application_id)
        if app is None:
            raise NotFound(f"application {application_id!r} not found")
        if app.status not in ("draft", "rfi"):
            raise InvalidState(
                f"application {application_id!r} cannot be submitted from status {app.status!r}"
            )

        product = self.visa_backend.get_product(app.product_id)
        if product is None:
            raise NotFound(
                f"product {app.product_id!r} for application {application_id!r} not found",
                code="product_not_found",
            )

        answers = dict(answers or {})
        required_fields = _required_form_fields(product)
        missing_fields = [f for f in required_fields if f not in answers]
        if missing_fields:
            raise _MissingFields(missing_fields)

        required_docs = _required_docs(product)
        present_kinds: set[str] = set(
            self.visa_backend.list_document_kinds_for(application_id)
        )
        # SPEC §3.5 step 3: docs_refs count as evidence alongside rows in
        # application_documents. Each ref is opaque; when it matches a
        # doc_id already recorded for this application we learn its kind
        # and include it in the "present" set.
        for ref in list(docs_refs or []):
            if not isinstance(ref, str) or not ref:
                continue
            doc = self.visa_backend.get_document_by_id(ref)
            if doc is not None and doc.application_id == application_id:
                present_kinds.add(doc.kind)
        missing_docs = [k for k in required_docs if k not in present_kinds]
        if missing_docs:
            raise _MissingDocuments(missing_docs)

        # Passport-validity check: if the product destination has a seeded
        # entry rule and the applicant supplied passport_expiry + travel_start
        # (or the applicant profile has passport_expiry), enforce that the
        # expiry is at least `passport_validity_months` past the entry date.
        self._check_passport_validity(app, product, answers)

        merged_answers = dict(answers)
        merged_answers["payment"] = {"payment_method_id": payment_method_id}

        prev_status = app.status
        app.status = "processing"
        app.answers = merged_answers
        # v3: no sim clock. ``decision_day`` is now an opaque
        # processing-day count owned by whoever writes the row (the
        # orchestrator via a mutation event, or the env's init.sql).
        # ``submit_application`` only records the transition.
        app.history = list(app.history) + [
            {
                "from": prev_status,
                "to": "processing",
                "note": "submitted (user-visible: submitted)",
            }
        ]
        app.updated_at = _now_iso()
        self.visa_backend.update_application(app)

        return {
            "application_id": application_id,
            "status": "submitted",
            "processing_time_days": int(product.processing_time_days),
        }

    def _check_passport_validity(
        self,
        app: VisaApplication,
        product: VisaProduct,
        answers: Dict[str, Any],
    ) -> None:
        """Block submission when passport expires before entry_date + required_months.

        Uses the entry_requirements row for (applicant_nationality, product.destination,
        "tourism") if available, else no-op. ``passport_expiry`` may live in
        ``answers`` or in ``applicant_profile``; ``travel_start`` in
        ``answers`` is treated as entry_date.
        """
        if self.entry_backend is None:
            return
        expiry_raw = (
            answers.get("passport_expiry")
            or (app.applicant or {}).get("passport_expiry")
        )
        travel_start_raw = (
            answers.get("travel_start")
            or answers.get("entry_date")
            or (app.applicant or {}).get("travel_start")
        )
        expiry = _parse_iso_date(expiry_raw)
        entry_date = _parse_iso_date(travel_start_raw)
        if expiry is None or entry_date is None:
            return

        nationality = (
            answers.get("nationality")
            or (app.applicant or {}).get("nationality")
        )
        if not isinstance(nationality, str) or not nationality:
            return
        try:
            nat = normalize_country_code(nationality)
            dest = normalize_country_code(product.destination)
        except ValidationError:
            return
        rule = self.entry_backend.get(nat, dest, "tourism")
        required_months = int(rule.passport_validity_months) if rule else 6
        if required_months <= 0:
            return
        cutoff = _add_months(entry_date, required_months)
        if expiry < cutoff:
            raise _PassportValidity(
                passport_expiry=expiry_raw,
                entry_date=travel_start_raw,
                required_months=required_months,
                cutoff=cutoff.strftime("%Y-%m-%d"),
                destination=dest,
            )

    def get_application(self, application_id: str) -> Dict[str, Any]:
        app = self.visa_backend.get_application(application_id)
        if app is None:
            raise NotFound(f"application {application_id!r} not found")
        docs = self.visa_backend.list_documents_for(application_id)
        return _application_detail(app, docs)

    def list_applications(self, user_id: str) -> List[Dict[str, Any]]:
        apps = self.visa_backend.list_applications_for_user(user_id)
        return [_application_summary(a) for a in apps]


class _MissingFields(ValidationError):
    code = "missing_fields"

    def __init__(self, fields: List[str]):
        super().__init__(f"missing required fields: {fields}")
        self.fields = list(fields)

    def to_payload(self) -> Dict[str, Any]:
        return {
            "error": str(self),
            "code": self.code,
            "fields": self.fields,
        }


class _MissingDocuments(ValidationError):
    code = "missing_documents"

    def __init__(self, kinds: List[str]):
        super().__init__(f"missing required documents: {kinds}")
        self.kinds = list(kinds)

    def to_payload(self) -> Dict[str, Any]:
        return {
            "error": str(self),
            "code": self.code,
            "kinds": self.kinds,
        }


class _PassportValidity(ValidationError):
    code = "passport_validity_insufficient"

    def __init__(
        self,
        *,
        passport_expiry: Any,
        entry_date: Any,
        required_months: int,
        cutoff: str,
        destination: str,
    ):
        super().__init__(
            f"passport_expiry {passport_expiry!r} is before "
            f"{destination} minimum ({required_months} months after entry "
            f"{entry_date!r}; cutoff {cutoff})"
        )
        self.passport_expiry = passport_expiry
        self.entry_date = entry_date
        self.required_months = required_months
        self.cutoff = cutoff
        self.destination = destination

    def to_payload(self) -> Dict[str, Any]:
        return {
            "error": str(self),
            "code": self.code,
            "passport_expiry": self.passport_expiry,
            "entry_date": self.entry_date,
            "required_months": self.required_months,
            "cutoff": self.cutoff,
            "destination": self.destination,
        }
