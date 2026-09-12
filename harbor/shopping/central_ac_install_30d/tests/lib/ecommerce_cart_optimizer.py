"""Seed-derived cart optimization used by the stage-8 rubric."""
from __future__ import annotations

import itertools
import re
import sqlite3
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class CartPlan:
    sku_ids: tuple[str, ...]
    product_titles: tuple[str, ...]
    coupon_codes: tuple[str, ...]
    subtotal_minor: int
    total_minor: int


def money_terms(amount_minor: int) -> tuple[str, ...]:
    amount_minor = int(amount_minor)
    whole, cents = divmod(abs(amount_minor), 100)
    sign = "-" if amount_minor < 0 else ""
    decimal = f"{sign}{whole}.{cents:02d}"
    return (str(amount_minor), decimal, f"${decimal}", f"CNY {decimal}")


def _seed_rows(path: Path):
    connection = sqlite3.connect(":memory:")
    try:
        schema = """
        CREATE TABLE products(product_id TEXT, title TEXT);
        CREATE TABLE skus(sku_id TEXT, product_id TEXT, attrs_json TEXT, price_minor INTEGER);
        CREATE TABLE coupons(code TEXT, kind TEXT, value_bp_or_minor INTEGER,
          min_spend_minor INTEGER, valid_from TEXT, valid_until TEXT, active INTEGER);
        """
        connection.executescript(schema)
        sql = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r"INSERT INTO products \(product_id, title,.*?\) VALUES \('([^']+)', '([^']*)'",
            sql,
        ):
            connection.execute("INSERT INTO products VALUES (?, ?)", match.groups())
        for match in re.finditer(
            r"INSERT INTO skus \(sku_id, product_id, attrs_json, price_minor\) VALUES \('([^']+)', '([^']+)', '.*?', (\d+)\)",
            sql,
        ):
            connection.execute("INSERT INTO skus VALUES (?, ?, '{}', ?)", (match.group(1), match.group(2), int(match.group(3))))
        for match in re.finditer(
            r"INSERT INTO coupons \(code, kind, value_bp_or_minor, min_spend_minor, valid_from, valid_until,.*?\) VALUES \('([^']+)', '([^']+)', (\d+), (\d+), '([^']+)', '([^']+)',.*?, (\d+)\)",
            sql,
        ):
            connection.execute("INSERT INTO coupons VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (match.group(1), match.group(2), int(match.group(3)), int(match.group(4)), match.group(5), match.group(6), int(match.group(7))))
        connection.commit()
        products = dict(connection.execute("SELECT product_id, title FROM products"))
        skus = list(connection.execute("SELECT sku_id, product_id, price_minor FROM skus"))
        coupons = list(connection.execute("SELECT code, kind, value_bp_or_minor, min_spend_minor, valid_from, valid_until, active FROM coupons"))
        return products, skus, coupons
    finally:
        connection.close()


def optimal_cart_plans(seed_path: str | Path, sku_prefix: str, as_of: date) -> tuple[CartPlan, ...]:
    products, skus, coupons = _seed_rows(Path(seed_path))
    by_need: dict[str, list[tuple[str, str, int]]] = {"n1": [], "n2": [], "n3": []}
    # The need attribute is intentionally read from the seed text so this helper
    # remains independent of the service database schema.
    sql = Path(seed_path).read_text(encoding="utf-8")
    needs = {m.group(1): m.group(2) for m in re.finditer(r"INSERT INTO skus \(sku_id, product_id, attrs_json, price_minor\) VALUES \('([^']+)', '[^']+', '\{\"need\": \"([^\"]+)\"\}',", sql)}
    for sku_id, product_id, price in skus:
        if sku_id.startswith(sku_prefix) and sku_id in needs:
            by_need.setdefault(needs[sku_id], []).append((sku_id, product_id, int(price)))
    candidates: list[CartPlan] = []
    for choices in itertools.product(by_need.get("n1", []), by_need.get("n2", []), by_need.get("n3", [])):
        sku_ids = tuple(row[0] for row in choices)
        subtotal = sum(row[2] for row in choices)
        titles = tuple(products.get(row[1], row[1]) for row in choices)
        eligible: list[tuple[str, int]] = []
        for code, kind, value, minimum, start, until, active in coupons:
            if not active or subtotal < minimum or not (start <= as_of.isoformat() <= until):
                continue
            discount = value if kind == "flat_off" else (subtotal * value) // 10000
            eligible.append((code, discount))
        codes = tuple(code for code, _ in eligible)
        discount = sum(value for _, value in eligible)
        candidates.append(CartPlan(sku_ids, titles, codes, subtotal, subtotal - discount))
    if not candidates:
        return ()
    minimum = min(plan.total_minor for plan in candidates)
    return tuple(plan for plan in candidates if plan.total_minor == minimum)
