"""CRUD operations on visa_products, visa_applications, application_documents."""

import json
from typing import List, Optional

from ..models.visa import ApplicationDocument, VisaApplication, VisaProduct
from .sqlite_backend import SqliteBackend


def _row_to_product(row) -> VisaProduct:
    return VisaProduct(
        product_id=row["product_id"],
        destination=row["destination"],
        nationality=row["nationality"],
        name=row["name"],
        processing_time_days=int(row["processing_time_days"]),
        fee_amount=int(row["fee_amount"]),
        fee_currency=row["fee_currency"],
        delivery=row["delivery"],
        form_schema=json.loads(row["form_schema_json"] or "{}"),
    )


def _row_to_application(row) -> VisaApplication:
    return VisaApplication(
        application_id=row["application_id"],
        user_id=row["user_id"],
        product_id=row["product_id"],
        status=row["status"],
        applicant=json.loads(row["applicant_json"] or "{}"),
        answers=json.loads(row["answers_json"] or "{}"),
        decision_day=row["decision_day"],
        decision_note=row["decision_note"],
        evisa_doc_ref=row["evisa_doc_ref"],
        history=json.loads(row["history_json"] or "[]"),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _row_to_document(row) -> ApplicationDocument:
    return ApplicationDocument(
        doc_id=row["doc_id"],
        application_id=row["application_id"],
        kind=row["kind"],
        ref=row["ref"],
        uploaded_at=row["uploaded_at"],
    )


class VisaBackend:
    def __init__(self, backend: SqliteBackend):
        self.backend = backend

    # ---- products ----------------------------------------------------------

    def insert_or_ignore_product(self, product: VisaProduct) -> None:
        self.backend.execute(
            "INSERT OR IGNORE INTO visa_products("
            " product_id, destination, nationality, name, processing_time_days,"
            " fee_amount, fee_currency, delivery, form_schema_json"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                product.product_id,
                product.destination,
                product.nationality,
                product.name,
                int(product.processing_time_days),
                int(product.fee_amount),
                product.fee_currency,
                product.delivery,
                json.dumps(product.form_schema),
            ),
        )

    def get_product(self, product_id: str) -> Optional[VisaProduct]:
        row = self.backend.fetchone(
            "SELECT * FROM visa_products WHERE product_id = ?",
            (product_id,),
        )
        return _row_to_product(row) if row else None

    def list_products_for(self, destination: str, nationality: str) -> List[VisaProduct]:
        rows = self.backend.fetchall(
            "SELECT * FROM visa_products "
            "WHERE destination = ? AND (nationality = ? OR nationality = '*') "
            "ORDER BY processing_time_days ASC, product_id ASC",
            (destination, nationality),
        )
        return [_row_to_product(r) for r in rows]

    # ---- applications ------------------------------------------------------

    def insert_application(self, app: VisaApplication) -> None:
        self.backend.execute(
            "INSERT INTO visa_applications("
            " application_id, user_id, product_id, status, applicant_json,"
            " answers_json, decision_day, decision_note, evisa_doc_ref,"
            " history_json, created_at, updated_at"
            ") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                app.application_id,
                app.user_id,
                app.product_id,
                app.status,
                json.dumps(app.applicant),
                json.dumps(app.answers),
                app.decision_day,
                app.decision_note,
                app.evisa_doc_ref,
                json.dumps(app.history),
                app.created_at,
                app.updated_at,
            ),
        )

    def update_application(self, app: VisaApplication) -> None:
        self.backend.execute(
            "UPDATE visa_applications SET "
            " user_id = ?, product_id = ?, status = ?, applicant_json = ?,"
            " answers_json = ?, decision_day = ?, decision_note = ?,"
            " evisa_doc_ref = ?, history_json = ?, updated_at = ? "
            "WHERE application_id = ?",
            (
                app.user_id,
                app.product_id,
                app.status,
                json.dumps(app.applicant),
                json.dumps(app.answers),
                app.decision_day,
                app.decision_note,
                app.evisa_doc_ref,
                json.dumps(app.history),
                app.updated_at,
                app.application_id,
            ),
        )

    def get_application(self, application_id: str) -> Optional[VisaApplication]:
        row = self.backend.fetchone(
            "SELECT * FROM visa_applications WHERE application_id = ?",
            (application_id,),
        )
        return _row_to_application(row) if row else None

    def list_applications_for_user(self, user_id: str) -> List[VisaApplication]:
        rows = self.backend.fetchall(
            "SELECT * FROM visa_applications WHERE user_id = ? "
            "ORDER BY created_at DESC, application_id DESC",
            (user_id,),
        )
        return [_row_to_application(r) for r in rows]

    # ---- documents ---------------------------------------------------------

    def insert_document(self, doc: ApplicationDocument) -> None:
        self.backend.execute(
            "INSERT INTO application_documents("
            " doc_id, application_id, kind, ref, uploaded_at"
            ") VALUES(?, ?, ?, ?, ?)",
            (
                doc.doc_id,
                doc.application_id,
                doc.kind,
                doc.ref,
                doc.uploaded_at,
            ),
        )

    def list_documents_for(self, application_id: str) -> List[ApplicationDocument]:
        rows = self.backend.fetchall(
            "SELECT * FROM application_documents "
            "WHERE application_id = ? ORDER BY uploaded_at ASC, doc_id ASC",
            (application_id,),
        )
        return [_row_to_document(r) for r in rows]

    def get_document_by_id(self, doc_id: str) -> Optional[ApplicationDocument]:
        row = self.backend.fetchone(
            "SELECT * FROM application_documents WHERE doc_id = ?",
            (doc_id,),
        )
        return _row_to_document(row) if row else None

    def list_document_kinds_for(self, application_id: str) -> set[str]:
        rows = self.backend.fetchall(
            "SELECT DISTINCT kind FROM application_documents WHERE application_id = ?",
            (application_id,),
        )
        return {r["kind"] for r in rows}
