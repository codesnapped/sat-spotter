

import json
from zoneinfo import ZoneInfo

from sat_spotter.config import CONFIG_PATH
from sat_spotter.display import group_passes, print_passes
from sat_spotter.export import export_file
from sat_spotter.location import observer
from sat_spotter.predict import find_passes
from sat_spotter.tle import fetch_tle, load_satellite, parse_tle


def run_passes(args):
    observer_lat: float = args.lat
    observer_lon: float = args.lon
    chosen_timezone: ZoneInfo = ZoneInfo(args.tz)
    prediction_window: int = args.hours
    minimum_elevation_filter: int = args.elev
    show_only_visible: bool = args.visible_only
    export_format: str | None = args.export

    satellites = json.load(open(CONFIG_PATH))

    all_passes = []
    observer_location = observer(observer_lat, observer_lon)
    for s in satellites:
        satellite = load_satellite(parse_tle(fetch_tle(s["norad_id"])))
        if satellite is None:
            print(f"Skipping {s['name']}")
            continue
        times, _ = find_passes(satellite, observer_location, prediction_window)
        satellite_pass = group_passes(times, satellite, observer_location, minimum_elevation_filter)
        all_passes.extend(satellite_pass)

    all_passes.sort(key=lambda p: p['rise'].tt)
    if export_format:
        export_file(all_passes, export_format, chosen_timezone)
    print_passes(all_passes, chosen_timezone, observer_lat, observer_lon, show_only_visible)