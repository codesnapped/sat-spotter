from dataclasses import dataclass

from skyfield.api import EarthSatellite, Time
from skyfield.toposlib import GeographicPosition


@dataclass
class TLEData:
    name: str
    line1: str
    line2: str


@dataclass
class SatellitePass:
    name: str
    rise: Time
    culminate: Time
    set: Time
    elevation: float
    rise_azimuth: float
    set_azimuth: float
    is_visible: bool
    satellite: EarthSatellite
    location: GeographicPosition
