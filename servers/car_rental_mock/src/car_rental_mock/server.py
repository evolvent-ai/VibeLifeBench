"""FastMCP entry point for car_rental_mock."""
from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS rental_locations (
  location_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  address TEXT NOT NULL,
  lat REAL NOT NULL,
  lng REAL NOT NULL,
  hours_json TEXT NOT NULL,
  notes TEXT,
  source_url TEXT
);

CREATE TABLE IF NOT EXISTS vehicles (
  vehicle_id TEXT PRIMARY KEY,
  model TEXT NOT NULL,
  class TEXT NOT NULL,
  energy_type TEXT NOT NULL CHECK (energy_type IN ('gasoline','ev','hybrid')),
  seats INTEGER NOT NULL,
  luggage_capacity TEXT,
  width_mm INTEGER,
  range_km_estimate REAL,
  energy_consumption_per_100km REAL,
  energy_unit TEXT NOT NULL,
  plate_tail TEXT,
  driver_notes TEXT,
  source_url TEXT
);

CREATE TABLE IF NOT EXISTS insurance_plans (
  plan_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  daily_price REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CNY',
  coverage_json TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS rental_offers (
  offer_id TEXT PRIMARY KEY,
  vehicle_id TEXT NOT NULL REFERENCES vehicles(vehicle_id),
  pickup_location_id TEXT NOT NULL REFERENCES rental_locations(location_id),
  return_location_id TEXT NOT NULL REFERENCES rental_locations(location_id),
  pickup_at TEXT NOT NULL,
  return_at TEXT NOT NULL,
  daily_price REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CNY',
  deposit_amount REAL NOT NULL,
  one_way_fee REAL NOT NULL DEFAULT 0,
  included_km_per_day REAL,
  energy_policy_json TEXT NOT NULL,
  return_requirements_json TEXT NOT NULL,
  inventory_remaining INTEGER NOT NULL DEFAULT 1,
  cancellation_policy TEXT NOT NULL,
  source_url TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
  booking_ref TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  offer_id TEXT NOT NULL REFERENCES rental_offers(offer_id),
  insurance_plan_id TEXT NOT NULL REFERENCES insurance_plans(plan_id),
  status TEXT NOT NULL,
  estimated_total REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CNY',
  created_at TEXT NOT NULL,
  drivers_json TEXT NOT NULL,
  contact_json TEXT NOT NULL,
  payment_json TEXT NOT NULL,
  pickup_condition_json TEXT,
  return_condition_json TEXT,
  history_json TEXT NOT NULL DEFAULT '[]'
);

CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings(user_id);

CREATE TABLE IF NOT EXISTS incident_reports (
  incident_id TEXT PRIMARY KEY,
  booking_ref TEXT NOT NULL REFERENCES bookings(booking_ref),
  incident_type TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  location TEXT NOT NULL,
  description TEXT NOT NULL,
  photos_count INTEGER NOT NULL DEFAULT 0,
  safe_to_drive INTEGER NOT NULL DEFAULT 1,
  platform_case_ref TEXT NOT NULL,
  created_at TEXT NOT NULL,
  status TEXT NOT NULL,
  estimated_fee REAL,
  currency TEXT NOT NULL DEFAULT 'CNY'
);

CREATE TABLE IF NOT EXISTS road_policy (
  policy_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  applies_to TEXT NOT NULL,
  detail_json TEXT NOT NULL,
  source_url TEXT
);

CREATE TABLE IF NOT EXISTS energy_stops (
  stop_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  lat REAL NOT NULL,
  lng REAL NOT NULL,
  energy_types_json TEXT NOT NULL,
  hours_json TEXT NOT NULL,
  wait_risk TEXT,
  notes TEXT,
  source_url TEXT
);

CREATE TABLE IF NOT EXISTS _counters (
  name TEXT PRIMARY KEY,
  value INTEGER NOT NULL
);
"""


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _setup_logging(debug: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )


def _connect(env_dir: Path) -> sqlite3.Connection:
    db_file = env_dir / "runtime.db"
    if db_file.exists():
        db_file.unlink()
    for sidecar in (env_dir / "runtime.db-wal", env_dir / "runtime.db-shm"):
        if sidecar.exists():
            sidecar.unlink()
    conn = sqlite3.connect(db_file, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA_SQL)
    init_sql = env_dir / "init.sql"
    if init_sql.exists():
        conn.executescript(init_sql.read_text(encoding="utf-8"))
    return conn


def _row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}


def _json(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def _next_counter(conn: sqlite3.Connection, name: str) -> int:
    conn.execute(
        "INSERT INTO _counters(name, value) VALUES (?, 0) "
        "ON CONFLICT(name) DO NOTHING",
        (name,),
    )
    conn.execute("UPDATE _counters SET value = value + 1 WHERE name = ?", (name,))
    row = conn.execute("SELECT value FROM _counters WHERE name = ?", (name,)).fetchone()
    return int(row["value"])


def _booking_ref(conn: sqlite3.Connection) -> str:
    return f"CR{_next_counter(conn, 'booking_seq'):06d}"


def _incident_ref(conn: sqlite3.Connection) -> str:
    return f"CRI{_next_counter(conn, 'incident_seq'):06d}"


def _case_ref(conn: sqlite3.Connection) -> str:
    return f"CASE-{_next_counter(conn, 'case_seq'):06d}"


def _days_inclusive(pickup_at: str, return_at: str) -> int:
    start = datetime.fromisoformat(pickup_at.replace("Z", "+00:00"))
    end = datetime.fromisoformat(return_at.replace("Z", "+00:00"))
    seconds = max(0.0, (end - start).total_seconds())
    days = int(seconds // 86400)
    if seconds % 86400:
        days += 1
    return max(1, days)


class CarRentalService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def search_vehicle_offers(
        self,
        pickup_city: str | None = None,
        return_city: str | None = None,
        pickup_at: str | None = None,
        return_at: str | None = None,
        energy_type: str | None = None,
        seats: int = 4,
        max_results: int = 20,
    ) -> dict[str, Any]:
        where = ["o.inventory_remaining > 0", "v.seats >= ?"]
        params: list[Any] = [int(seats or 1)]
        if pickup_city:
            where.append("lower(pl.city) = lower(?)")
            params.append(pickup_city)
        if return_city:
            where.append("lower(rl.city) = lower(?)")
            params.append(return_city)
        if pickup_at:
            where.append("o.pickup_at = ?")
            params.append(pickup_at)
        if return_at:
            where.append("o.return_at = ?")
            params.append(return_at)
        if energy_type:
            where.append("v.energy_type = ?")
            params.append(energy_type)
        rows = self.conn.execute(
            f"""
            SELECT o.*, v.model, v.class, v.energy_type, v.seats, v.luggage_capacity,
                   v.width_mm, v.range_km_estimate, v.energy_consumption_per_100km,
                   v.energy_unit, v.driver_notes,
                   pl.name AS pickup_name, pl.city AS pickup_city,
                   rl.name AS return_name, rl.city AS return_city
            FROM rental_offers o
            JOIN vehicles v ON v.vehicle_id = o.vehicle_id
            JOIN rental_locations pl ON pl.location_id = o.pickup_location_id
            JOIN rental_locations rl ON rl.location_id = o.return_location_id
            WHERE {' AND '.join(where)}
            ORDER BY o.daily_price ASC, v.energy_type ASC, o.offer_id ASC
            LIMIT ?
            """,
            (*params, max(1, min(int(max_results), 50))),
        ).fetchall()
        offers = [self._offer_out(row) for row in rows]
        return {"offers": offers, "count": len(offers)}

    def get_vehicle_offer(self, offer_id: str) -> dict[str, Any]:
        return self._offer_out(self._offer_row(offer_id))

    def list_insurance_plans(self) -> dict[str, Any]:
        rows = self.conn.execute(
            "SELECT * FROM insurance_plans ORDER BY daily_price ASC, plan_id ASC"
        ).fetchall()
        return {"plans": [self._insurance_out(row) for row in rows]}

    def compare_energy_options(
        self,
        pickup_city: str,
        return_city: str,
        pickup_at: str,
        return_at: str,
        route_km_estimate: float = 520.0,
        seats: int = 4,
    ) -> dict[str, Any]:
        offers = self.search_vehicle_offers(
            pickup_city=pickup_city,
            return_city=return_city,
            pickup_at=pickup_at,
            return_at=return_at,
            seats=seats,
            max_results=50,
        )["offers"]
        highway_policy = self.get_road_policy()
        comparisons = []
        for offer in offers:
            energy = offer["vehicle"]["energy_type"]
            consumption = float(offer["vehicle"].get("energy_consumption_per_100km") or 0)
            energy_policy = offer["energy_policy"]
            unit_price = float(energy_policy.get("estimated_unit_price", 0))
            energy_units = round(route_km_estimate / 100.0 * consumption, 2)
            energy_cost = round(energy_units * unit_price, 2)
            comparisons.append({
                "offer_id": offer["offer_id"],
                "model": offer["vehicle"]["model"],
                "energy_type": energy,
                "rental_subtotal": offer["price_breakdown"]["rental_subtotal"],
                "one_way_fee": offer["price_breakdown"]["one_way_fee"],
                "estimated_energy_units": energy_units,
                "energy_unit": offer["vehicle"]["energy_unit"],
                "estimated_energy_cost": {
                    "amount": energy_cost,
                    "currency": offer["currency"],
                },
                "estimated_trip_cost_without_insurance": {
                    "amount": round(offer["price_breakdown"]["rental_subtotal"] + offer["price_breakdown"]["one_way_fee"] + energy_cost, 2),
                    "currency": offer["currency"],
                },
                "planning_notes": self._energy_notes(offer),
            })
        return {
            "route_km_estimate": route_km_estimate,
            "highway_policy": highway_policy,
            "comparisons": comparisons,
        }

    def create_rental_booking(
        self,
        offer_id: str,
        insurance_plan_id: str,
        driver_user_id: str,
        drivers: list[dict[str, Any]],
        contact: dict[str, Any],
        payment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        offer = self._offer_row(offer_id)
        plan = self._insurance_row(insurance_plan_id)
        if int(offer["inventory_remaining"]) <= 0:
            return {"error": "inventory_gone", "offer_id": offer_id}
        days = _days_inclusive(offer["pickup_at"], offer["return_at"])
        total = round(
            float(offer["daily_price"]) * days
            + float(offer["one_way_fee"])
            + float(plan["daily_price"]) * days,
            2,
        )
        booking_ref = _booking_ref(self.conn)
        now = _now_iso()
        history = [{"at": now, "event": "CREATED", "detail": f"offer={offer_id}; insurance={insurance_plan_id}"}]
        self.conn.execute(
            """
            INSERT INTO bookings (
              booking_ref, user_id, offer_id, insurance_plan_id, status,
              estimated_total, currency, created_at, drivers_json,
              contact_json, payment_json, history_json
            ) VALUES (?, ?, ?, ?, 'held', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                booking_ref,
                driver_user_id,
                offer_id,
                insurance_plan_id,
                total,
                offer["currency"],
                now,
                json.dumps(drivers, ensure_ascii=False),
                json.dumps(contact, ensure_ascii=False),
                json.dumps(payment or {}, ensure_ascii=False),
                json.dumps(history, ensure_ascii=False),
            ),
        )
        self.conn.execute(
            "UPDATE rental_offers SET inventory_remaining = inventory_remaining - 1 WHERE offer_id = ?",
            (offer_id,),
        )
        return self.get_booking(booking_ref)

    def get_booking(self, booking_ref: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM bookings WHERE booking_ref = ?",
            (booking_ref,),
        ).fetchone()
        if not row:
            return {"error": "booking_not_found", "booking_ref": booking_ref}
        return self._booking_out(row)

    def list_bookings(self, user_id: str | None = None) -> dict[str, Any]:
        if user_id:
            rows = self.conn.execute(
                "SELECT * FROM bookings WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM bookings ORDER BY created_at DESC"
            ).fetchall()
        return {"bookings": [self._booking_out(row, brief=True) for row in rows], "count": len(rows)}

    def report_vehicle_condition(
        self,
        booking_ref: str,
        phase: str,
        checklist_items: dict[str, Any],
        odometer_km: float | None = None,
        fuel_or_charge_level: str | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        row = self._booking_row(booking_ref)
        field = "pickup_condition_json" if phase == "pickup" else "return_condition_json"
        condition = {
            "phase": phase,
            "recorded_at": _now_iso(),
            "odometer_km": odometer_km,
            "fuel_or_charge_level": fuel_or_charge_level,
            "checklist_items": checklist_items,
            "notes": notes,
        }
        history = _json(row["history_json"], [])
        history.append({"at": condition["recorded_at"], "event": f"{phase.upper()}_CONDITION", "detail": notes or ""})
        self.conn.execute(
            f"UPDATE bookings SET {field} = ?, history_json = ? WHERE booking_ref = ?",
            (
                json.dumps(condition, ensure_ascii=False),
                json.dumps(history, ensure_ascii=False),
                booking_ref,
            ),
        )
        return {"booking_ref": booking_ref, "condition": condition}

    def report_incident(
        self,
        booking_ref: str,
        incident_type: str,
        occurred_at: str,
        location: str,
        description: str,
        photos_count: int = 0,
        safe_to_drive: bool = True,
        estimated_fee: float | None = None,
    ) -> dict[str, Any]:
        self._booking_row(booking_ref)
        incident_id = _incident_ref(self.conn)
        case_ref = _case_ref(self.conn)
        now = _now_iso()
        self.conn.execute(
            """
            INSERT INTO incident_reports (
              incident_id, booking_ref, incident_type, occurred_at, location,
              description, photos_count, safe_to_drive, platform_case_ref,
              created_at, status, estimated_fee
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'reported', ?)
            """,
            (
                incident_id,
                booking_ref,
                incident_type,
                occurred_at,
                location,
                description,
                int(photos_count),
                1 if safe_to_drive else 0,
                case_ref,
                now,
                estimated_fee,
            ),
        )
        return self.get_incident_report(incident_id)

    def get_incident_report(self, incident_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT * FROM incident_reports WHERE incident_id = ?",
            (incident_id,),
        ).fetchone()
        if not row:
            return {"error": "incident_not_found", "incident_id": incident_id}
        return self._incident_out(row)

    def list_incident_reports(self, booking_ref: str | None = None) -> dict[str, Any]:
        if booking_ref:
            rows = self.conn.execute(
                "SELECT * FROM incident_reports WHERE booking_ref = ? ORDER BY occurred_at",
                (booking_ref,),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM incident_reports ORDER BY occurred_at"
            ).fetchall()
        return {"incidents": [self._incident_out(row) for row in rows], "count": len(rows)}

    def get_return_requirements(self, booking_ref: str) -> dict[str, Any]:
        booking = self._booking_row(booking_ref)
        offer = self._offer_row(booking["offer_id"])
        return {
            "booking_ref": booking_ref,
            "status": booking["status"],
            "return_location": self._location_out(self._location_row(offer["return_location_id"])),
            "return_at": offer["return_at"],
            "requirements": _json(offer["return_requirements_json"], {}),
            "energy_policy": _json(offer["energy_policy_json"], {}),
            "open_incidents": self.list_incident_reports(booking_ref)["incidents"],
        }

    def get_road_policy(self) -> dict[str, Any]:
        rows = self.conn.execute("SELECT * FROM road_policy ORDER BY policy_id").fetchall()
        return {"policies": [self._road_policy_out(row) for row in rows]}

    def list_energy_stops(self, energy_type: str | None = None, city: str | None = None) -> dict[str, Any]:
        rows = self.conn.execute("SELECT * FROM energy_stops ORDER BY city, name").fetchall()
        stops = []
        for row in rows:
            out = self._energy_stop_out(row)
            if city and out["city"] != city:
                continue
            if energy_type and energy_type not in out["energy_types"]:
                continue
            stops.append(out)
        return {"stops": stops, "count": len(stops)}

    def _offer_row(self, offer_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM rental_offers WHERE offer_id = ?", (offer_id,)).fetchone()
        if not row:
            raise ValueError(f"offer_not_found: {offer_id}")
        return row

    def _insurance_row(self, plan_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM insurance_plans WHERE plan_id = ?", (plan_id,)).fetchone()
        if not row:
            raise ValueError(f"insurance_plan_not_found: {plan_id}")
        return row

    def _booking_row(self, booking_ref: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM bookings WHERE booking_ref = ?", (booking_ref,)).fetchone()
        if not row:
            raise ValueError(f"booking_not_found: {booking_ref}")
        return row

    def _location_row(self, location_id: str) -> sqlite3.Row:
        row = self.conn.execute("SELECT * FROM rental_locations WHERE location_id = ?", (location_id,)).fetchone()
        if not row:
            raise ValueError(f"location_not_found: {location_id}")
        return row

    def _offer_out(self, row: sqlite3.Row) -> dict[str, Any]:
        days = _days_inclusive(row["pickup_at"], row["return_at"])
        vehicle = self.conn.execute("SELECT * FROM vehicles WHERE vehicle_id = ?", (row["vehicle_id"],)).fetchone()
        pickup = self._location_row(row["pickup_location_id"])
        ret = self._location_row(row["return_location_id"])
        rental_subtotal = round(float(row["daily_price"]) * days, 2)
        return {
            "offer_id": row["offer_id"],
            "vehicle": self._vehicle_out(vehicle),
            "pickup_location": self._location_out(pickup),
            "return_location": self._location_out(ret),
            "pickup_at": row["pickup_at"],
            "return_at": row["return_at"],
            "rental_days": days,
            "currency": row["currency"],
            "price_breakdown": {
                "daily_price": row["daily_price"],
                "rental_subtotal": rental_subtotal,
                "one_way_fee": row["one_way_fee"],
                "deposit_amount": row["deposit_amount"],
                "insurance_not_included": True,
            },
            "included_km_per_day": row["included_km_per_day"],
            "energy_policy": _json(row["energy_policy_json"], {}),
            "return_requirements": _json(row["return_requirements_json"], {}),
            "inventory_remaining": row["inventory_remaining"],
            "cancellation_policy": row["cancellation_policy"],
            "source_url": row["source_url"],
            "notes": row["notes"],
        }

    @staticmethod
    def _vehicle_out(row: sqlite3.Row | None) -> dict[str, Any]:
        if row is None:
            return {}
        return {
            "vehicle_id": row["vehicle_id"],
            "model": row["model"],
            "class": row["class"],
            "energy_type": row["energy_type"],
            "seats": row["seats"],
            "luggage_capacity": row["luggage_capacity"],
            "width_mm": row["width_mm"],
            "range_km_estimate": row["range_km_estimate"],
            "energy_consumption_per_100km": row["energy_consumption_per_100km"],
            "energy_unit": row["energy_unit"],
            "plate_tail": row["plate_tail"],
            "driver_notes": row["driver_notes"],
            "source_url": row["source_url"],
        }

    @staticmethod
    def _location_out(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "location_id": row["location_id"],
            "name": row["name"],
            "city": row["city"],
            "address": row["address"],
            "geo": {"lat": row["lat"], "lng": row["lng"]},
            "hours": _json(row["hours_json"], {}),
            "notes": row["notes"],
            "source_url": row["source_url"],
        }

    @staticmethod
    def _insurance_out(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "plan_id": row["plan_id"],
            "name": row["name"],
            "daily_price": row["daily_price"],
            "currency": row["currency"],
            "coverage": _json(row["coverage_json"], {}),
            "notes": row["notes"],
        }

    def _booking_out(self, row: sqlite3.Row, brief: bool = False) -> dict[str, Any]:
        offer = self._offer_row(row["offer_id"])
        plan = self._insurance_row(row["insurance_plan_id"])
        out = {
            "booking_ref": row["booking_ref"],
            "user_id": row["user_id"],
            "status": row["status"],
            "offer": self._offer_out(offer),
            "insurance_plan": self._insurance_out(plan),
            "estimated_total": {"amount": row["estimated_total"], "currency": row["currency"]},
            "created_at": row["created_at"],
        }
        if not brief:
            out["drivers"] = _json(row["drivers_json"], [])
            out["contact"] = _json(row["contact_json"], {})
            out["history"] = _json(row["history_json"], [])
            out["pickup_condition"] = _json(row["pickup_condition_json"], None)
            out["return_condition"] = _json(row["return_condition_json"], None)
        return out

    @staticmethod
    def _incident_out(row: sqlite3.Row) -> dict[str, Any]:
        out = _row_dict(row) or {}
        out["safe_to_drive"] = bool(out.get("safe_to_drive"))
        return out

    @staticmethod
    def _road_policy_out(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "policy_id": row["policy_id"],
            "name": row["name"],
            "applies_to": row["applies_to"],
            "detail": _json(row["detail_json"], {}),
            "source_url": row["source_url"],
        }

    @staticmethod
    def _energy_stop_out(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "stop_id": row["stop_id"],
            "name": row["name"],
            "city": row["city"],
            "geo": {"lat": row["lat"], "lng": row["lng"]},
            "energy_types": _json(row["energy_types_json"], []),
            "hours": _json(row["hours_json"], {}),
            "wait_risk": row["wait_risk"],
            "notes": row["notes"],
            "source_url": row["source_url"],
        }

    @staticmethod
    def _energy_notes(offer: dict[str, Any]) -> list[str]:
        energy = offer["vehicle"]["energy_type"]
        if energy == "ev":
            return [
                "Confirm hotel parking can support overnight charging or nearby fast charging.",
                "Add charging time to the route plan before long scenic-road days.",
                "Return charge level must match the rental offer requirements.",
            ]
        return [
            "No separate Hainan expressway toll line item; fuel cost varies with A/C, detours and traffic.",
            "Refuel before return according to the full-fuel requirement.",
        ]


def build_server(env_dir: Path) -> FastMCP:
    conn = _connect(env_dir)
    service = CarRentalService(conn)
    mcp = FastMCP("car-rental-mock", host="0.0.0.0")

    @mcp.tool()
    async def search_vehicle_offers(
        pickup_city: str | None = None,
        return_city: str | None = None,
        pickup_at: str | None = None,
        return_at: str | None = None,
        energy_type: str | None = None,
        seats: int = 4,
        max_results: int = 20,
    ) -> dict[str, Any]:
        """Search rental car offers by city, dates, seats, and energy type."""
        return service.search_vehicle_offers(
            pickup_city=pickup_city,
            return_city=return_city,
            pickup_at=pickup_at,
            return_at=return_at,
            energy_type=energy_type,
            seats=seats,
            max_results=max_results,
        )

    @mcp.tool()
    async def get_vehicle_offer(offer_id: str) -> dict[str, Any]:
        """Fetch a rental car offer."""
        return service.get_vehicle_offer(offer_id)

    @mcp.tool()
    async def list_insurance_plans() -> dict[str, Any]:
        """List insurance plans available for the rental scenario."""
        return service.list_insurance_plans()

    @mcp.tool()
    async def compare_energy_options(
        pickup_city: str,
        return_city: str,
        pickup_at: str,
        return_at: str,
        route_km_estimate: float = 520.0,
        seats: int = 4,
    ) -> dict[str, Any]:
        """Compare gasoline and EV offers including estimated energy costs."""
        return service.compare_energy_options(
            pickup_city, return_city, pickup_at, return_at, route_km_estimate, seats
        )

    @mcp.tool()
    async def create_rental_booking(
        offer_id: str,
        insurance_plan_id: str,
        driver_user_id: str,
        drivers: list[dict[str, Any]],
        contact: dict[str, Any],
        payment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a held rental booking."""
        return service.create_rental_booking(
            offer_id, insurance_plan_id, driver_user_id, drivers, contact, payment
        )

    @mcp.tool()
    async def get_booking(booking_ref: str) -> dict[str, Any]:
        """Fetch a rental booking."""
        return service.get_booking(booking_ref)

    @mcp.tool()
    async def list_bookings(user_id: str | None = None) -> dict[str, Any]:
        """List rental bookings."""
        return service.list_bookings(user_id)

    @mcp.tool()
    async def report_vehicle_condition(
        booking_ref: str,
        phase: str,
        checklist_items: dict[str, Any],
        odometer_km: float | None = None,
        fuel_or_charge_level: str | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        """Record pickup or return condition evidence for a booking."""
        return service.report_vehicle_condition(
            booking_ref, phase, checklist_items, odometer_km, fuel_or_charge_level, notes
        )

    @mcp.tool()
    async def report_incident(
        booking_ref: str,
        incident_type: str,
        occurred_at: str,
        location: str,
        description: str,
        photos_count: int = 0,
        safe_to_drive: bool = True,
        estimated_fee: float | None = None,
    ) -> dict[str, Any]:
        """Report a rental incident or scrape to the platform."""
        return service.report_incident(
            booking_ref, incident_type, occurred_at, location,
            description, photos_count, safe_to_drive, estimated_fee,
        )

    @mcp.tool()
    async def list_incident_reports(booking_ref: str | None = None) -> dict[str, Any]:
        """List incident reports."""
        return service.list_incident_reports(booking_ref)

    @mcp.tool()
    async def get_return_requirements(booking_ref: str) -> dict[str, Any]:
        """Return fuel/charge, timing, wash, and incident-document requirements."""
        return service.get_return_requirements(booking_ref)

    @mcp.tool()
    async def get_road_policy() -> dict[str, Any]:
        """Return road toll/fee policy rows relevant to the rental scenario."""
        return service.get_road_policy()

    @mcp.tool()
    async def list_energy_stops(
        energy_type: str | None = None,
        city: str | None = None,
    ) -> dict[str, Any]:
        """List seeded fuel/charging stops."""
        return service.list_energy_stops(energy_type, city)

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="car_rental_mock MCP server")
    parser.add_argument("--env", required=True)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    _setup_logging(args.debug)
    try:
        mcp = build_server(Path(args.env))
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("shutdown requested")
    except Exception as exc:  # noqa: BLE001
        logging.getLogger(__name__).exception("server startup failed: %s", exc)
        sys.exit(1)
