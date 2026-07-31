from __future__ import annotations

from pydantic import BaseModel


class Observation(BaseModel):
    geo_key: str
    city: str
    temp_c: float
    humidity: float
    wind_kmh: float
    condition: str
    precip_mm: float
    observed_at: str


class HourlyForecast(BaseModel):
    dt: str
    temp_c: float
    condition: str
    precip_mm: float
    wind_kmh: float


class DailyForecast(BaseModel):
    date: str
    tmin: float
    tmax: float
    condition: str
    precip_prob: float
    wind_kmh: float


class AQI(BaseModel):
    geo_key: str
    aqi: int
    category: str
    dominant_pollutant: str
    observed_at: str
