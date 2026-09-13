"""Pin L6 — snapshot shape contract: capture must feed what scoring reads.

The verifier's frozen database is built only from stage snapshots and traces
(``_helpers._frozen_database``). Stage 8's dynamic-cart check therefore needs
the snapshot to carry the ecommerce cart and the official coupon definitions —
without those capture keys the check can only crash (NULL rule fields) or read
an always-empty cart. This pins the capture ↔ scoring round-trip in both
directions: capture keys exist, capture calls resolve to real mock tools, and a
snapshot in the captured shape ingests cart rows and coupon definitions.

Runnable standalone: ``python3 tests/test_snapshot_shape_contract.py``.
"""
import ast
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CAPTURE = os.path.join(ROOT, "environment", "evidence-collector", "snapshot_capture.py")

# Keys the scoring side requires in capture_stage_snapshot()["ecommerce"].
REQUIRED_ECOMMERCE_KEYS = {"main_order", "acceptance_order", "products", "addresses", "cart", "coupons"}


def _capture_module_ast():
    with open(CAPTURE, encoding="utf-8") as fh:
        return ast.parse(fh.read())


def _capture_calls():
    """(server, tool) pairs referenced by capture_stage_snapshot's body."""
    pairs = set()
    for node in ast.walk(_capture_module_ast()):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("_call", "_paged_call"):
            if len(node.args) >= 3:
                env_arg, server, tool = node.args[:3]
                if (isinstance(env_arg, ast.Name) and env_arg.id == "env"
                        and isinstance(server, ast.Constant) and isinstance(tool, ast.Constant)):
                    pairs.add((server.value, tool.value))
    return pairs


def test_capture_exposes_cart_and_coupon_sources():
    for node in ast.walk(_capture_module_ast()):
        if isinstance(node, ast.FunctionDef) and node.name == "capture_stage_snapshot":
            for stmt in ast.walk(node):
                if (isinstance(stmt, ast.Dict)):
                    keys = {k.value for k in stmt.keys if isinstance(k, ast.Constant)}
                    if "main_order" in keys:  # the ecommerce block
                        missing = REQUIRED_ECOMMERCE_KEYS - keys
                        assert not missing, f"ecommerce snapshot block missing keys: {missing}"
                        return
    raise AssertionError("capture_stage_snapshot has no ecommerce block")


def test_capture_calls_resolve_to_mocks():
    import importlib.util

    spec = importlib.util.spec_from_file_location("registry_pin", os.path.join(HERE, "test_tool_name_registry.py"))
    registry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(registry)
    surface = registry.mock_tool_surface()
    phantom = [(server, tool) for server, tool in sorted(_capture_calls())
               if server not in surface or tool not in surface[server]]
    assert not phantom, f"phantom snapshot capture calls: {phantom}"


def test_no_capture_for_unregistered_servers():
    with open(os.path.join(HERE, "services.json"), encoding="utf-8") as fh:
        import json
        registered = set(json.load(fh)["mcp_servers"])
    stray = {server for server, _tool in _capture_calls() if server not in registered}
    assert not stray, f"capture references servers outside services.json: {stray}"


def test_captured_shape_ingests_cart_and_coupons():
    """A snapshot in the captured shape populates cart_items and real coupons."""
    if os.path.join(HERE) not in __import__("sys").path:
        __import__("sys").path.insert(0, os.path.join(HERE))
    from rubrics.shared import _helpers as R

    hinges = "renovation note hinges "
    coupon = {
        "code": "MUZUO30", "kind": "flat_off", "value_bp_or_minor": 3000,
        "min_spend_minor": 24200, "valid_from": "2026-06-01", "valid_until": "2026-08-31",
        "category_restriction": None, "max_uses": 5000, "used_count": 187, "active": 1,
    }
    item = {"cart_item_id": "ci_1", "product_id": "bnd_qbed_a3", "sku_id": "bsk_qbed_a3",
            "qty": 1, "unit_price_minor": 9400, "line_total_minor": 9400}
    snapshot = {
        "ecommerce": {
            "main_order": {"order_id": "ord_qbed_0001", "user_id": "usr_du_rong", "status": "delivered"},
            "cart": {"user_id": "usr_du_rong", "items": [item], "applied_coupons": [
                {"code": "MUZUO30", "kind": "flat_off", "discount_minor": 3000}]},
            "coupons": {"coupons": [coupon]},
        },
    }

    class Env:
        active_stage = 0
        def published_stages(self):
            return [0]
        def snapshot(self, stage):
            return snapshot
        def trace(self, stage):
            return []

    conn = R._frozen_database(Env(), 0)
    assert [tuple(r) for r in conn.execute("SELECT user_id,sku_id,qty FROM cart_items")] == [
        ("usr_du_rong", "bsk_qbed_a3", 1)]
    rows = list(conn.execute("SELECT code,kind,value_bp_or_minor,min_spend_minor,valid_from,valid_until,active FROM coupons"))
    assert rows == [("MUZUO30", "flat_off", 3000, 24200, "2026-06-01", "2026-08-31", 1)]
    assert [r[0] for r in conn.execute("SELECT code FROM applied_coupons")] == ["MUZUO30"]
    # A definition row with NULL rule fields is non-applicable, not a crash.
    assert R._coupon_discount(("X", "flat_off", None, None, None, None, None, None, None, None),
                              [{"price": 1, "category": hinges}], "2026-06-22") is None


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
