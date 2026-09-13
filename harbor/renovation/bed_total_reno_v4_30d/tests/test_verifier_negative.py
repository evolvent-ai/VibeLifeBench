"""Pin — verifier discrimination is two-sided (real evidence, real verifier).

Regression pin for the stage-8 defect family: the frozen-evidence chain used to
crash the verifier (``int(None)`` on coupon rows whose rule fields were NULL —
applied-coupon detail dicts mis-ingested as coupon definitions) while
``cart_items`` could never populate (cart-view items carry no ``user_id`` and no
``cart`` path key existed in traces). A crash aborts the oracle arm and an
always-empty cart makes the check unpassable; either way scoring is meaningless.

This runs the real rubric code over synthetic evidence shaped exactly like the
capture produces, and asserts the check passes the genuinely optimal cart,
fails every near-miss, and scores zero for a do-nothing agent.

Runnable standalone: ``python3 tests/test_verifier_negative.py``.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in __import__("sys").path:
    __import__("sys").path.insert(0, HERE)

from rubrics import stage_8  # noqa: E402
from rubrics.shared import _backend as B  # noqa: E402
from rubrics.shared import _helpers as R  # noqa: E402

HINGES = "renovation note hinges "   # seed category of bnd_qbed_a* and HOMEWEEK50's restriction
SLIDES = "renovation note drawer slides "
PRIMER = " paint finish renovation note "
USER = "usr_du_rong"
AS_OF = "2026-06-22"
PREFIXES = ("bnd_qbed_a", "bnd_qbed_b", "bnd_qbed_c")


def _coupon(code, kind, value, minimum, restriction=None):
    return {"code": code, "kind": kind, "value_bp_or_minor": value, "min_spend_minor": minimum,
            "valid_from": "2026-06-01", "valid_until": "2026-08-31", "category_restriction": restriction,
            "max_uses": 5000, "used_count": 100, "active": 1}


COUPONS = {"coupons": [
    _coupon("HOMEWEEK50", "flat_off", 5000, 9000, HINGES),
    _coupon("JIAJU12", "percent_off", 1200, 10000),
    _coupon("MUZUO30", "flat_off", 3000, 24200),
    _coupon("QIMIAN120", "flat_off", 12000, 52200),
    _coupon("WUJIN70", "flat_off", 7000, 28000),
]}


def _product(pid, category, sku_id, price, stock):
    return {"product_id": pid, "category": category,
            "skus": [{"sku_id": sku_id, "attrs": {}, "price_minor": price, "stock": stock}]}


PRODUCTS = [
    _product("bnd_qbed_a1", HINGES, "bsk_qbed_a1", 18400, 37),
    _product("bnd_qbed_a2", HINGES, "bsk_qbed_a2", 11400, 64),
    _product("bnd_qbed_a3", HINGES, "bsk_qbed_a3", 9400, 29),
    _product("bnd_qbed_ax", HINGES, "bsk_qbed_ax", 8700, 29),
    _product("bnd_qbed_b1", SLIDES, "bsk_qbed_b1", 17400, 18),
    _product("bnd_qbed_b2", SLIDES, "bsk_qbed_b2", 12400, 46),
    _product("bnd_qbed_c1", PRIMER, "bsk_qbed_c1", 11400, 13),
    _product("bnd_qbed_c2", PRIMER, "bsk_qbed_c2", 6900, 52),
    _product("bnd_qbed_c3", PRIMER, "bsk_qbed_c3", 5400, 71),
]


def _order(oid, total, placed):
    return {"order_id": oid, "user_id": USER, "status": "delivered", "total_minor": total, "placed_at": placed}


def _cart_view(items, applied):
    subtotal = sum(i["qty"] * i["unit_price_minor"] for i in items)
    discount = sum(a["discount_minor"] for a in applied)
    return {"user_id": USER, "items": items, "subtotal_minor": subtotal,
            "applied_coupons": applied, "discount_minor": discount, "total_minor": max(0, subtotal - discount)}


def _detail(code, kind, discount):
    return {"code": code, "kind": kind, "discount_minor": discount}


DISCOUNTS = {"MUZUO30": 3000, "WUJIN70": 7000, "JIAJU12": 3444, "HOMEWEEK50": 5000}


def _applied(codes):
    return [_detail(c, "percent_off" if c == "JIAJU12" else "flat_off", DISCOUNTS[c]) for c in codes]


def _cart_item(n, product_id, sku_id, price):
    return {"cart_item_id": f"ci_{n}", "product_id": product_id, "sku_id": sku_id,
            "qty": 1, "unit_price_minor": price, "line_total_minor": price}


A3 = ("bnd_qbed_a3", "bsk_qbed_a3", 9400)
B2 = ("bnd_qbed_b2", "bsk_qbed_b2", 12400)
C2 = ("bnd_qbed_c2", "bsk_qbed_c2", 6900)
A2 = ("bnd_qbed_a2", "bsk_qbed_a2", 11400)
AX = ("bnd_qbed_ax", "bsk_qbed_ax", 8700)
C3 = ("bnd_qbed_c3", "bsk_qbed_c3", 5400)
ALL4 = ("MUZUO30", "WUJIN70", "JIAJU12", "HOMEWEEK50")
THREE = ("MUZUO30", "WUJIN70", "JIAJU12")


def _snapshot(stage, cart):
    return {"stage": stage,
            "ecommerce": {"main_order": _order("ord_qbed_0001", 3400000, "2026-06-11T14:20:00+08:00"),
                          "acceptance_order": _order("ord_qbed_0002", 85400, "2026-06-12T10:05:00+08:00"),
                          "products": [], "addresses": [], "cart": cart, "coupons": dict(COUPONS)},
            "workspace": {}}


def _env(traces):
    snapshots = {stage: _snapshot(stage, _cart_view([], [])) for stage in range(9)}

    class Env:
        active_stage = 8
        def published_stages(self):
            return sorted(snapshots)
        def snapshot(self, stage):
            return snapshots[stage]
        def trace(self, stage):
            return traces.get(stage, [])

    return Env()


def _stage8_trace(cart_triples, codes):
    """Evidence a stage-8 turn leaves behind: product discovery + cart/coupon actions."""
    trace = [{"name": "ecommerce__get_product", "result": p, "success": True} for p in PRODUCTS]
    for code in codes:
        trace.append({"name": "ecommerce__apply_coupon", "result": _cart_view(
            [_cart_item(n, *t) for n, t in enumerate(cart_triples)], _applied(codes[: codes.index(code) + 1])),
            "success": True})
    trace.append({"name": "ecommerce__get_cart", "result": _cart_view(
        [_cart_item(n, *t) for n, t in enumerate(cart_triples)], _applied(codes)), "success": True})
    return {8: trace}


def test_optimal_cart_passes():
    env = _env(_stage8_trace((A3, B2, C2), ALL4))
    assert B.optimized_cart(env) is True
    assert R.no_new_order(env, after="2026-06-22T00:00:00+08:00") is True


def test_near_misses_fail():
    kw = dict(user_id=USER, product_prefixes=PREFIXES, as_of=AS_OF)
    wrong_sku = _env(_stage8_trace((A2, B2, C2), ALL4))
    assert R.cart_is_dynamic_optimum(wrong_sku, **kw) is False
    missing_coupon = _env(_stage8_trace((A3, B2, C2), THREE))
    assert R.cart_is_dynamic_optimum(missing_coupon, **kw) is False
    no_coupons = _env(_stage8_trace((A3, B2, C2), ()))
    assert R.cart_is_dynamic_optimum(no_coupons, **kw) is False
    cheaper_looking_suboptimal = _env(_stage8_trace((AX, B2, C3), THREE))
    assert R.cart_is_dynamic_optimum(cheaper_looking_suboptimal, **kw) is False


def test_nop_evidence_scores_zero():
    env = _env({})
    assert stage_8.s8_table(env) is False
    assert stage_8.s8_optimal(env) is False


def test_null_rule_coupon_rows_never_crash():
    # The original crash: int(None) raised VerifierInfrastructureError and
    # aborted the oracle arm. A partial definition is non-applicable instead.
    bad = ("BADCODE", "flat_off", None, None, None, None, None, None, None, None)
    assert R._coupon_discount(bad, [{"price": 100, "category": HINGES}], AS_OF) is None


def test_applied_details_stay_out_of_coupons():
    # Cart-view applied-coupon dicts {code, kind, discount_minor} share code/kind
    # with definitions; ingesting them poisoned the coupons table with NULLs.
    env = _env(_stage8_trace((A3, B2, C2), ALL4))
    rows = {row[0]: row[1] for row in R.sql_rows(
        env, "ecommerce", "SELECT code,valid_from FROM coupons")}
    assert set(rows) == set(COUPONS["coupons"][i]["code"] for i in range(5))
    assert all(valid_from is not None for valid_from in rows.values()), "NULL rule row reached coupons"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
