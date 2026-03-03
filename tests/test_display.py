from sat_spotter.display import degrees_to_compass


def test_degrees_to_compass_valid():
    deg = 55
    result = degrees_to_compass(deg)
    assert result == "NE"

def test_degrees_to_compass_north():
    deg = 0
    result = degrees_to_compass(deg)
    assert result == "N"

def test_degrees_to_compass_south():
    deg = 180
    result = degrees_to_compass(deg)
    assert result == "S"

def test_degrees_to_compass_wraparound():
    deg = 350
    result = degrees_to_compass(deg)
    assert result == "N"

def test_degrees_to_compass_boundary():
    deg = 22
    result = degrees_to_compass(deg)
    assert result == "N"