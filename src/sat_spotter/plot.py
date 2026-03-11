import json

import matplotlib.pyplot as plt
import numpy as np

from skyfield.api import EarthSatellite, load
from skyfield.toposlib import GeographicPosition

from sat_spotter.config import CONFIG_PATH
from sat_spotter.display import group_passes
from sat_spotter.location import observer
from sat_spotter.predict import find_passes
from sat_spotter.tle import fetch_tle, load_satellite, parse_tle

def plot_passes(passes_data):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 90)
    ax.set_yticks([0, 30, 60, 90])
    ax.set_yticklabels(['90°', '60°', '30°', '0°'])

    for p in passes_data:
        satellite: EarthSatellite = p['satellite']
        location: GeographicPosition = p['location']
        rise_time = p['rise']
        set_time = p['set']
        ts = load.timescale()
        time_array = ts.linspace(rise_time, set_time, 50)
        difference = satellite - location
        topocentric = difference.at(time_array)
        alt, az, _ = topocentric.altaz()
        azimuths = np.radians(az.degrees)
        radii = 90 - alt.degrees
        line, = ax.plot(azimuths, radii, label=p['name'])                                                       
        color = line.get_color()
        ax.plot(azimuths[0], radii[0], 'o', color=color)   # rise point                      
        ax.plot(azimuths[-1], radii[-1], 'o', color=color)   # set point

    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys(), loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.show()

def run_plot(args):
    observer_lat: float = args.lat
    observer_lon: float = args.lon
    prediction_window: int = args.hours
    minimum_elevation_filter: int = args.elev
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
    plot_passes(all_passes)