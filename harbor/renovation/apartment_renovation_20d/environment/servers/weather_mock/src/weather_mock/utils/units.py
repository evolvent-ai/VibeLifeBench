def c_to_f(c: float) -> float:
    return round(c * 9 / 5 + 32, 1)


def kmh_to_mph(kmh: float) -> float:
    return round(kmh * 0.621371, 1)


def convert_obs_units(obs: dict, units: str) -> dict:
    """Return a copy of ``obs`` with units applied.

    "metric" → temps in Celsius and winds in km/h (no-op).
    "imperial" → temps in Fahrenheit (temp_f / tmin_f / tmax_f) and winds in mph
    (wind_mph). The original metric keys are replaced to avoid duplicate shape.
    """
    if units != "imperial":
        return obs
    out = dict(obs)
    if "temp_c" in out:
        out["temp_f"] = c_to_f(out.pop("temp_c"))
    if "tmin" in out:
        out["tmin"] = c_to_f(out["tmin"])
    if "tmax" in out:
        out["tmax"] = c_to_f(out["tmax"])
    if "wind_kmh" in out:
        out["wind_mph"] = kmh_to_mph(out.pop("wind_kmh"))
    return out
