from unittest.mock import patch, MagicMock

import numpy as np

from sat_spotter.models import SatellitePass
from sat_spotter.plot import plot_passes


def _make_pass_data(name="ISS", alt_peak=60):
    """Build a fake SatellitePass with mocked Skyfield objects."""
    rise_time = MagicMock()
    set_time = MagicMock()
    culminate_time = MagicMock()

    n_points = 50
    az_values = np.linspace(0, 180, n_points)
    alt_values = np.concatenate([
        np.linspace(0, alt_peak, n_points // 2),
        np.linspace(alt_peak, 0, n_points - n_points // 2),
    ])

    alt_obj = MagicMock()
    alt_obj.degrees = alt_values
    az_obj = MagicMock()
    az_obj.degrees = az_values

    topocentric = MagicMock()
    topocentric.altaz.return_value = (alt_obj, az_obj, MagicMock())

    difference = MagicMock()
    difference.at.return_value = topocentric

    satellite = MagicMock()
    location = MagicMock()
    satellite.__sub__ = MagicMock(return_value=difference)

    return SatellitePass(
        name=name,
        rise=rise_time,
        culminate=culminate_time,
        set=set_time,
        elevation=alt_peak,
        rise_azimuth=0.0,
        set_azimuth=180.0,
        is_visible=True,
        satellite=satellite,
        location=location,
    )


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_single_pass(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    line_mock = MagicMock()
    line_mock.get_color.return_value = "blue"
    mock_ax.plot.return_value = (line_mock,)
    mock_ax.get_legend_handles_labels.return_value = (["h1"], ["ISS"])

    passes = [_make_pass_data("ISS")]
    plot_passes(passes)

    mock_plt.subplots.assert_called_once_with(subplot_kw={"projection": "polar"})
    # arc + rise marker + set marker = 3 plot calls
    assert mock_ax.plot.call_count == 3
    mock_plt.show.assert_called_once()


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_multiple_passes(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    line_mock = MagicMock()
    line_mock.get_color.return_value = "red"
    mock_ax.plot.return_value = (line_mock,)
    mock_ax.get_legend_handles_labels.return_value = (["h1", "h2", "h3"], ["ISS", "HUBBLE", "STARLINK-42"])

    passes = [
        _make_pass_data("ISS"),
        _make_pass_data("HUBBLE"),
        _make_pass_data("STARLINK-42"),
    ]
    plot_passes(passes)

    # 3 passes x 3 plot calls each = 9
    assert mock_ax.plot.call_count == 9
    mock_plt.show.assert_called_once()


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_polar_axes_configuration(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    line_mock = MagicMock()
    line_mock.get_color.return_value = "green"
    mock_ax.plot.return_value = (line_mock,)
    mock_ax.get_legend_handles_labels.return_value = (["h1"], ["ISS"])

    plot_passes([_make_pass_data()])

    mock_ax.set_theta_zero_location.assert_called_once_with("N")
    mock_ax.set_theta_direction.assert_called_once_with(-1)
    mock_ax.set_ylim.assert_called_once_with(0, 90)
    mock_ax.set_yticks.assert_called_once_with([0, 30, 60, 90])
    mock_ax.set_yticklabels.assert_called_once_with(["90°", "60°", "30°", "0°"])


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_rise_and_set_markers(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    line_mock = MagicMock()
    line_mock.get_color.return_value = "blue"
    mock_ax.plot.return_value = (line_mock,)
    mock_ax.get_legend_handles_labels.return_value = (["h1"], ["ISS"])

    plot_passes([_make_pass_data()])

    plot_calls = mock_ax.plot.call_args_list
    # Second call is rise marker
    rise_call = plot_calls[1]
    assert rise_call[0][2] == "o"
    assert rise_call[1]["color"] == "C0"
    # Third call is set marker
    set_call = plot_calls[2]
    assert set_call[0][2] == "o"
    assert set_call[1]["color"] == "C0"


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_legend_created(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    line_mock = MagicMock()
    mock_ax.plot.return_value = (line_mock,)
    mock_ax.get_legend_handles_labels.return_value = (["h1"], ["HUBBLE"])

    plot_passes([_make_pass_data("HUBBLE")])

    mock_ax.get_legend_handles_labels.assert_called_once()
    mock_ax.legend.assert_called_once()


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_empty_passes(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)
    mock_ax.get_legend_handles_labels.return_value = ([], [])

    plot_passes([])

    mock_ax.plot.assert_not_called()
    mock_plt.show.assert_called_once()


@patch("sat_spotter.plot.load.timescale")
@patch("sat_spotter.plot.plt")
def test_satellite_difference_computed(mock_plt, mock_timescale):
    mock_ax = MagicMock()
    mock_fig = MagicMock()
    mock_plt.subplots.return_value = (mock_fig, mock_ax)

    line_mock = MagicMock()
    line_mock.get_color.return_value = "blue"
    mock_ax.plot.return_value = (line_mock,)
    mock_ax.get_legend_handles_labels.return_value = (["h1"], ["ISS"])

    pass_data = _make_pass_data("ISS")
    plot_passes([pass_data])

    # Verify satellite - location was called
    pass_data.satellite.__sub__.assert_called_once_with(pass_data.location)
