import matplotlib.pyplot as plt
import numpy as np

from skyfield.api import load

from sat_spotter.passes import compute_all_passes

def plot_passes(passes_data):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 90)
    ax.set_yticks([0, 30, 60, 90])
    ax.set_yticklabels(['90°', '60°', '30°', '0°'])

    names = list({p.name for p in passes_data})
    colors = {name: f'C{i}' for i, name in enumerate(names)}

    for p in passes_data:
        ts = load.timescale()
        time_array = ts.linspace(p.rise, p.set, 50)
        difference = p.satellite - p.location
        topocentric = difference.at(time_array)
        alt, az, _ = topocentric.altaz()
        azimuths = np.radians(az.degrees)
        radii = 90 - alt.degrees
        color = colors[p.name]
        ax.plot(azimuths, radii, label=p.name, color=color)
        ax.plot(azimuths[0], radii[0], 'o', color=color)   # rise point
        ax.plot(azimuths[-1], radii[-1], 'o', color=color)   # set point

    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys(), loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.show()

def run_plot(args):
    all_passes = compute_all_passes(args.lat, args.lon, args.hours, args.elev)
    plot_passes(all_passes)