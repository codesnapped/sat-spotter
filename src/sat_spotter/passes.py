import json
from zoneinfo import ZoneInfo

from sat_spotter.config import CONFIG_PATH
from sat_spotter.display import group_passes, print_passes
from sat_spotter.export import export_file
from sat_spotter.location import observer
from sat_spotter.models import SatellitePass
from sat_spotter.predict import find_passes
from sat_spotter.tle import fetch_tle, load_satellite, parse_tle


def compute_all_passes(observer_lat: float, observer_lon: float, hours: int, min_elevation: int) -> list[SatellitePass]:
    with open(CONFIG_PATH) as f:
        satellites = json.load(f)
    all_passes = []
    observer_location = observer(observer_lat, observer_lon)
    for s in satellites:
        satellite = load_satellite(parse_tle(fetch_tle(s["norad_id"])))
        if satellite is None:
            print(f"Skipping {s['name']}")
            continue
        times, _ = find_passes(satellite, observer_location, hours)
        satellite_pass = group_passes(times, satellite, observer_location, min_elevation)
        all_passes.extend(satellite_pass)
    all_passes.sort(key=lambda p: p.rise.tt)
    return all_passes


def run_passes(args):
    observer_lat: float = args.lat
    observer_lon: float = args.lon
    chosen_timezone: ZoneInfo = ZoneInfo(args.tz)
    show_only_visible: bool = args.visible_only
    export_format: str | None = args.export

    all_passes = compute_all_passes(observer_lat, observer_lon, args.hours, args.elev)

    if export_format:
        export_file(all_passes, export_format, chosen_timezone)
    print_passes(all_passes, chosen_timezone, observer_lat, observer_lon, show_only_visible)