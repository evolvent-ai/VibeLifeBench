"""Visa product + application MCP tool registration."""

import json
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from ..services.visa_service import VisaService
from ..utils.exceptions import VisaError


def register_visa_tools(
    mcp: FastMCP,
    visa_service: VisaService,
) -> None:
    @mcp.tool()
    async def list_visa_products(nationality: str, destination: str) -> str:
        """List visa products available for a nationality/destination pair.

        Returns a JSON-encoded list of product summaries on success, or
        a JSON-encoded error dict (``{"error":..., "code":...}``).
        """
        try:
            result = visa_service.list_products(nationality, destination)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def get_visa_product(product_id: str) -> str:
        """Return the full details of a visa product, including form schema."""
        try:
            result = visa_service.get_product(product_id)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def start_visa_application(
        product_id: str, applicant_profile: Dict[str, Any]
    ) -> str:
        """Start a draft visa application for the given product/applicant."""
        try:
            result = visa_service.start_application(product_id, applicant_profile)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def upload_document(
        application_id: str, kind: str, doc_ref: str
    ) -> str:
        """Attach a document reference (kind = passport/photo/itinerary/...)."""
        try:
            result = visa_service.upload_document(application_id, kind, doc_ref)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def submit_visa_application(
        application_id: str,
        answers: Dict[str, Any],
        docs_refs: List[str],
        payment_method_id: str,
    ) -> str:
        """Submit a draft (or RFI'd) application; sets status to processing."""
        try:
            result = visa_service.submit_application(
                application_id=application_id,
                answers=answers,
                docs_refs=docs_refs or [],
                payment_method_id=payment_method_id,
            )
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def get_visa_application(application_id: str) -> str:
        """Return the full state of a visa application, including documents and history."""
        try:
            result = visa_service.get_application(application_id)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)

    @mcp.tool()
    async def list_visa_applications(user_id: str) -> str:
        """List all visa applications for a user, most recent first.

        Returns a JSON-encoded list of summaries on success, or a JSON-
        encoded error dict on failure.
        """
        try:
            result = visa_service.list_applications(user_id)
        except VisaError as e:
            result = e.to_payload()
        except Exception as e:  # pragma: no cover
            result = {"error": str(e), "code": "internal_error"}
        return json.dumps(result, ensure_ascii=False)
