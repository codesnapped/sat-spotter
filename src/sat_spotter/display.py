from zoneinfo import ZoneInfo

from skyfield.api import EarthSatellite
from skyfield.toposlib import GeographicPosition
from rich.table import Table
from rich.console import Console

from sat_spotter.models import SatellitePass
from sat_spotter.visibility import is_visible


def group_passes(times, events, satellite: EarthSatellite, location: GeographicPosition, min_elevation: float) -> list[SatellitePass]:
    # Skyfield emits events as a flat stream (0=rise, 1=culminate, 2=set). Track
    # state and only emit a pass once a full rise/culminate/set triple is seen,
    # so passes clipped by the window edges (e.g. already up at the start) are
    # dropped instead of mis-pairing the events.
    passes_list = []
    difference = satellite - location
    rise_time = culminate_time = rise_azimuth = None
    for time, event in zip(times, events):
        if event == 0:  # rise
            rise_time = time
            _, az, _ = difference.at(time).altaz()
            rise_azimuth = az.degrees
            culminate_time = None
        elif event == 1:  # culmination
            culminate_time = time
        elif event == 2:  # set
            if rise_time is None or culminate_time is None:
                rise_time = culminate_time = None
                continue
            alt, _, _ = difference.at(culminate_time).altaz()
            _, set_az, _ = difference.at(time).altaz()
            if alt.degrees > min_elevation:
                passes_list.append(SatellitePass(
                    name=satellite.name,
                    rise=rise_time,
                    culminate=culminate_time,
                    set=time,
                    elevation=alt.degrees,
                    rise_azimuth=rise_azimuth,
                    set_azimuth=set_az.degrees,
                    is_visible=is_visible(satellite, location, culminate_time),
                    satellite=satellite,
                    location=location,
                ))
            rise_time = culminate_time = None
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

def print_passes(passes: list, timezone: ZoneInfo, observer_lat: float, observer_lon: float, show_only_visible: bool):
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
    if not show_only_visible:
        table.add_column("Visible", justify="center")
    
    for p in passes:
        name = p.name
        rise_time = to_local_time(p.rise, timezone)
        set_time = to_local_time(p.set, timezone)
        event_duration = f"{((p.set.tt - p.rise.tt) * 24 * 60):.1f} min"
        event_date = to_local_time(p.rise, timezone, format='%d-%m')

        elevation = p.elevation
        if elevation > 45:
            elevation = f"[green]{p.elevation:.0f}°[/green]"
        elif elevation > 19:
            elevation = f"[yellow]{p.elevation:.0f}°[/yellow]"
        else:
            elevation = f"[red]{p.elevation:.0f}°[/red]"

        rise_dir = degrees_to_compass(p.rise_azimuth)
        set_dir = degrees_to_compass(p.set_azimuth)
        visible = "[green]Yes[/green]" if p.is_visible else "No"
        if not show_only_visible:
            table.add_row(event_date, name, rise_time, set_time, event_duration, elevation, rise_dir, set_dir, visible)
        else:
            if p['is_visible']:
                table.add_row(event_date, name, rise_time, set_time, event_duration, elevation, rise_dir, set_dir)

    console.print(table)
