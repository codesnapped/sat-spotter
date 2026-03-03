from sat_spotter.tle import parse_tle


def test_parse_tle_valid():
    raw = """ISS (ZARYA)
  1 25544U 98067A   24088.54171806  .00016717  00000-0  30456-3 0  9993
  2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.49815328447129"""
    result = parse_tle(raw)
    assert result["name"] == "ISS (ZARYA)"
    assert result["line1"].startswith("1 ")
    assert result["line2"].startswith("2 ")

def test_parse_tle_none():
    result = parse_tle(None)
    assert result is None

def test_parse_tle_invalid():
    raw = "No GP data found"
    result = parse_tle(raw)
    assert result is None

def test_parse_tle_bad_lines():
    raw = """ISS (ZARYA)
  25544U 98067A   24088.54171806  .00016717  00000-0  30456-3 0  9993
  25544  51.6416 247.4627 0006703 130.5360 325.0288 15.49815328447129"""
    result = parse_tle(raw)
    assert result is None