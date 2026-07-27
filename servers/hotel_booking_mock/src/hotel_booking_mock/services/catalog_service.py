import hashlib
import json
import sqlite3
from typing import List, Optional

from ..utils.dates import current_date_iso, iter_nights
from ..utils.exceptions import BadDateRangeError, HotelNotFoundError
from ..utils.pricing import haversine_km


ALLOWED_SORTS = {"price_asc", "price_desc", "user_rating_desc", "star_desc"}


class CatalogService:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def search_hotels(
        self,
        city_or_geo: str,
        check_in: str,
        check_out: str,
        guests: int,
        filters: Optional[dict] = None,
    ) -> List[dict]:
        try:
            nights = iter_nights(check_in, check_out)
        except ValueError:
            raise BadDateRangeError("check_out must be after check_in")
        if len(nights) > 30:
            raise BadDateRangeError("stay exceeds 30 nights")
        if not isinstance(guests, int) or guests < 1 or guests > 6:
            raise BadDateRangeError("guests must be an integer in 1..6")

        filters = filters or {}
        sort_key = filters.get("sort", "price_asc")
        if sort_key not in ALLOWED_SORTS:
            sort_key = "price_asc"
        limit = int(filters.get("limit", 20) or 20)
        limit = max(1, min(limit, 50))

        hotel_rows = self._select_hotels(city_or_geo)
        results: List[dict] = []
        current_date = current_date_iso(self.conn)

        for h in hotel_rows:
            # occupancy check
            amenities = json.loads(h["amenities_json"])
            if "min_star_rating" in filters and int(h["star_rating"]) < int(filters["min_star_rating"]):
                continue
            if "max_star_rating" in filters and int(h["star_rating"]) > int(filters["max_star_rating"]):
                continue
            if "min_user_rating" in filters and float(h["user_rating"]) < float(filters["min_user_rating"]):
                continue
            if "amenities" in filters:
                required = filters["amenities"] or []
                if not all(a in amenities for a in required):
                    continue

            # pull per-night rate_plans for this hotel and window, respecting guests & filters
            cheapest_per_night = {}
            plan_meta = {}  # (room_type, flavor) -> {'min_price': int, 'refundable_until': str|None, 'breakfast': bool}
            rp_rows = self.conn.execute(
                """
                SELECT rate_plan_row_id, date, room_type, flavor, nightly_price, currency, inventory_remaining,
                       refundable_until, breakfast_included, max_occupancy
                FROM rate_plans
                WHERE hotel_id = ? AND date IN (%s)
                """ % (",".join(["?"] * len(nights))),
                [h["hotel_id"], *nights],
            ).fetchall()

            per_combo_coverage = {}
            for r in rp_rows:
                if int(r["max_occupancy"]) < guests:
                    continue
                if int(r["inventory_remaining"]) <= 0:
                    continue
                if filters.get("refundable_only") and not r["refundable_until"]:
                    continue
                if filters.get("breakfast_included") and not int(r["breakfast_included"]):
                    continue
                if "max_nightly_price" in filters and int(r["nightly_price"]) > int(filters["max_nightly_price"]):
                    continue
                combo = (r["room_type"], r["flavor"])
                per_combo_coverage.setdefault(combo, {})[r["date"]] = r

            # Check which combos cover ALL nights
            hotel_min_price = None
            cheapest_combo_row = None
            for combo, date_map in per_combo_coverage.items():
                if not all(n in date_map for n in nights):
                    continue
                currencies = {str(date_map[n]["currency"]) for n in nights}
                if len(currencies) != 1:
                    continue
                total_min_nightly = min(int(date_map[n]["nightly_price"]) for n in nights)
                # record this combo's minimum nightly for hotel_min_price selection
                if hotel_min_price is None or total_min_nightly < hotel_min_price:
                    hotel_min_price = total_min_nightly
                    cheapest_combo_row = date_map[nights[0]]

            if hotel_min_price is None:
                continue  # no combo covers all nights

            refundable = False
            if cheapest_combo_row and cheapest_combo_row["refundable_until"]:
                # refundable when any night's refundable_until is still in the future relative to current_date
                ru = cheapest_combo_row["refundable_until"]
                # accept if date prefix > current_date
                if ru[:10] >= current_date:
                    refundable = True

            results.append({
                "hotel_id": h["hotel_id"],
                "name": h["name"],
                "star_rating": int(h["star_rating"]),
                "user_rating": float(h["user_rating"]),
                "nightly_price_from": int(hotel_min_price),
                "currency": str(cheapest_combo_row["currency"]),
                "refundable": refundable,
                "thumbnail": f"https://mock.hotels.local/img/{h['hotel_id']}/1.jpg",
                "district": h["district"],
                "city": h["city"],
            })

        # sorting
        if sort_key == "price_asc":
            results.sort(key=lambda r: r["nightly_price_from"])
        elif sort_key == "price_desc":
            results.sort(key=lambda r: -r["nightly_price_from"])
        elif sort_key == "user_rating_desc":
            results.sort(key=lambda r: -r["user_rating"])
        elif sort_key == "star_desc":
            results.sort(key=lambda r: (-r["star_rating"], -r["user_rating"]))

        return results[:limit]

    def _select_hotels(self, city_or_geo: str) -> List[sqlite3.Row]:
        s = (city_or_geo or "").strip()
        # Geo format: "lat,lng;radius_km"
        if ";" in s and "," in s.split(";", 1)[0]:
            try:
                coords, radius_s = s.split(";", 1)
                lat_s, lng_s = coords.split(",", 1)
                lat, lng, radius = float(lat_s), float(lng_s), float(radius_s)
                all_rows = self.conn.execute("SELECT * FROM hotels").fetchall()
                return [h for h in all_rows if haversine_km(lat, lng, float(h["geo_lat"]), float(h["geo_lng"])) <= radius]
            except Exception:
                return []
        # City (case-insensitive)
        city_match = self.conn.execute(
            "SELECT * FROM hotels WHERE lower(city) = lower(?)",
            (s,),
        ).fetchall()
        if city_match:
            return city_match
        # District (case-insensitive)
        district_match = self.conn.execute(
            "SELECT * FROM hotels WHERE lower(district) = lower(?)",
            (s,),
        ).fetchall()
        return district_match

    def get_hotel_details(self, hotel_id: str) -> dict:
        row = self.conn.execute("SELECT * FROM hotels WHERE hotel_id = ?", (hotel_id,)).fetchone()
        if not row:
            raise HotelNotFoundError("hotel not found")

        amenities = json.loads(row["amenities_json"])
        address = json.loads(row["address_json"])
        policies = json.loads(row["policies_json"])
        # Merge geo into address so the caller has one coordinate source.
        address.setdefault("geo_lat", float(row["geo_lat"]))
        address.setdefault("geo_lng", float(row["geo_lng"]))

        photos = [f"https://mock.hotels.local/img/{hotel_id}/{i}.jpg" for i in range(1, 4)]

        out = {
            "hotel_id": row["hotel_id"],
            "name": row["name"],
            "description": row["description"],
            "star_rating": int(row["star_rating"]),
            "user_rating": float(row["user_rating"]),
            "user_rating_count": int(row["user_rating_count"]),
            "address": address,
            "amenities": amenities,
            "photos": photos,
            "policies": policies,
            "contact": {
                # Deterministic across processes: Python's built-in hash() is
                # PYTHONHASHSEED-salted, so use sha256 for a stable digest.
                "phone": f"+81-3-0000-{int(hashlib.sha256(hotel_id.encode('utf-8')).hexdigest()[:8], 16) % 10000:04d}",
                "email": f"reservations@mock-{hotel_id}.example",
            },
        }
        return out
