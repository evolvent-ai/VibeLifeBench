"""Domain exceptions for the ecommerce mock server.

All errors expose a stable `code` field; the MCP layer turns these into
`{"error", "code"}` JSON envelopes. Codes are documented in SPEC.md.
"""
from typing import Optional


class EcommerceMockError(Exception):
    """Base exception. Subclasses set a stable `code`."""

    code: str = "BAD_ARG"

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class BadArgError(EcommerceMockError):
    code = "BAD_ARG"


class ProductNotFoundError(EcommerceMockError):
    code = "PRODUCT_NOT_FOUND"


class SkuNotFoundError(EcommerceMockError):
    code = "SKU_NOT_FOUND"


class OutOfStockError(EcommerceMockError):
    code = "OUT_OF_STOCK"


class CartEmptyError(EcommerceMockError):
    code = "CART_EMPTY"


class CartItemNotFoundError(EcommerceMockError):
    code = "CART_ITEM_NOT_FOUND"


class AddressNotFoundError(EcommerceMockError):
    code = "ADDRESS_NOT_FOUND"


class CouponInvalidError(EcommerceMockError):
    code = "COUPON_INVALID"


class CouponExpiredError(EcommerceMockError):
    code = "COUPON_EXPIRED"


class CouponBelowMinError(EcommerceMockError):
    code = "COUPON_BELOW_MIN"


class CouponCategoryMismatchError(EcommerceMockError):
    code = "COUPON_CATEGORY_MISMATCH"


class CouponNotAppliedError(EcommerceMockError):
    code = "COUPON_NOT_APPLIED"


class OrderNotFoundError(EcommerceMockError):
    code = "ORDER_NOT_FOUND"


class OrderNotCancelableError(EcommerceMockError):
    code = "ORDER_NOT_CANCELABLE"


class OrderItemNotFoundError(EcommerceMockError):
    code = "ORDER_ITEM_NOT_FOUND"


class RefundWindowClosedError(EcommerceMockError):
    code = "REFUND_WINDOW_CLOSED"
