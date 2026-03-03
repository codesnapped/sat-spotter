# sat-spotter

CLI tool for predicting satellite passes over your location. Fetches real TLE data from Celestrak, computes pass times using SGP4 propagation, and displays results with elevation, direction, and duration.

Built with a focus on European/ESA satellites and the Polish space sector.

## Features

- Track multiple satellites (ISS, EagleEye, Sentinel-6A, and more)
- Pass prediction with rise/set times, max elevation, and compass directions
- **Visibility detection** — shows which passes are actually visible (sunlit satellite + dark sky)
- Color-coded elevation (green = great, yellow = ok, red = low)
- Local timezone support (defaults to Europe/Warsaw)
- TLE caching (4-hour expiry) to avoid repeated network requests
- Configurable via CLI flags and `satellites.json`
- Satellite management — search, add, list, and remove tracked satellites
- Duplicate detection when adding satellites

## Installation

Requires Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Default: 24h forecast for Warsaw
sat-spotter passes

# Custom location and time window
sat-spotter passes --lat 50.06 --lon 19.94 --hours 48

# Only show high-elevation passes
sat-spotter passes --elev 30

# Only show passes visible to the naked eye
sat-spotter passes --visible-only --hours 48

# Different timezone
sat-spotter passes --tz Europe/Berlin

# Search for a satellite and add to tracked list
sat-spotter search sentinel

# List currently tracked satellites
sat-spotter list

# Remove a satellite from tracked list
sat-spotter remove
```

### Commands

| Command | Description |
|---------|-------------|
| `sat-spotter passes` | Predict satellite passes (default) |
| `sat-spotter search <name>` | Search Celestrak and add to tracked list |
| `sat-spotter list` | Show currently tracked satellites |
| `sat-spotter remove` | Remove a satellite from tracked list |

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--lat` | 52.23 | Observer latitude |
| `--lon` | 21.01 | Observer longitude |
| `--hours` | 24 | Prediction window in hours |
| `--elev` | 10 | Minimum elevation in degrees |
| `--tz` | Europe/Warsaw | Timezone for display |
| `--visible-only` | false | Only show passes visible to the naked eye |

## Configuring satellites

Edit `satellites.json` to add or remove tracked satellites:

```json
[
    {"name": "ISS", "norad_id": 25544},
    {"name": "EagleEye", "norad_id": 60508},
    {"name": "Sentinel-6A", "norad_id": 46984}
]
```

Or use `sat-spotter search <name>` to find and add satellites interactively.

## Tech stack

- [skyfield](https://rhodesmill.org/skyfield/) — satellite position computation (SGP4)
- [httpx](https://www.python-httpx.org/) — HTTP client for TLE fetching
- [rich](https://rich.readthedocs.io/) — terminal table formatting
