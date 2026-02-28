from zoneinfo import ZoneInfo

from skyfield.api import EarthSatellite
from skyfield.toposlib import GeographicPosition
from rich.table import Table
from rich.console import Console

from sat_spotter.visibility import is_visible


def group_passes(times, satellite: EarthSatellite, location: GeographicPosition, min_elevation: float) -> list:
    passes_list = []
    for i in range(0, len(times) - 2, 3):
        difference = satellite - location
        topocentric = difference.at(times[i + 1])
        alt, _, _ = topocentric.altaz()
        rise_topo = difference.at(times[i])
        _, rise_az, _ = rise_topo.altaz()
        set_topo = difference.at(times[i + 2])
        _, set_az, _ = set_topo.altaz()
        pass_data = {
            "name": satellite.name,
            "rise": times[i],
            "culminate": times[i + 1],
            "set": times[i + 2],
            "elevation": alt.degrees,
            "rise_azimuth": rise_az.degrees,
            "set_azimuth": set_az.degrees,
            "is_visible": is_visible(satellite, location, times[i + 1]),
        }
        if alt.degrees > min_elevation:
            passes_list.append(pass_data)
    return passes_list

def degrees_to_compass(deg: int) -> str:
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(deg / 45) % 8
    return dirs[index]

def to_local_time(time, timezone: ZoneInfo, format = '%H:%M') -> str:
    utc_dt = time.utc_datetime()
    local_dt = utc_dt.astimezone(timezone)
    local_str = local_dt.strftime(format)
    return local_str

def print_passes(passes: list, timezone: ZoneInfo, observer_lat: float, observer_lon: float):
    console = Console()
    table = Table(title=f"Satellite passes over {observer_lat}, {observer_lon}")
    table.add_column("Date", justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Rise", justify="center")
    table.add_column("Set", justify="center")
    table.add_column("Duration", justify="center")
    table.add_column("Max Elev", justify="center")
    table.add_column("Rise Dir", justify="center")
    table.add_column("Set Dir", justify="center")
    table.add_column("Visible", justify="center")
    
    for p in passes:
        name = p['name']
        rise_time = to_local_time(p['rise'], timezone)
        set_time = to_local_time(p['set'], timezone)
        event_duration = f"{((p['set'].tt - p['rise'].tt) * 24 * 60):.1f} min"
        event_date = to_local_time(p['rise'], timezone, format='%d-%m')

        elevation = p['elevation']
        if elevation > 45:
            elevation = f"[green]{p['elevation']:.0f}°[/green]"
        elif elevation > 19:
            elevation = f"[yellow]{p['elevation']:.0f}°[/yellow]"
        else:
            elevation = f"[red]{p['elevation']:.0f}°[/red]"

        rise_dir = degrees_to_compass(p['rise_azimuth'])
        set_dir = degrees_to_compass(p['set_azimuth'])
        visible = "[green]Yes[/green]" if p['is_visible'] else "No"
        table.add_row(event_date, name, rise_time, set_time, event_duration, elevation, rise_dir, set_dir, visible)

    console.print(table)
