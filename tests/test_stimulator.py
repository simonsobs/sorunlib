import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
os.environ["SORUNLIB_CONFIG"] = "./data/example_config.yaml"

import pytest
from unittest.mock import MagicMock, patch

from ocs.ocs_client import OCSReply
from sorunlib import stimulator

from util import create_patch_clients


patch_clients_lat = create_patch_clients('lat')


def _configure_pcr(pcr, volt_set=0, v_ac=0, output=True):
    """Configure PCR mock return values."""
    pcr.get_volt_ac.return_value = (None, None, {'data': {'volt_set': volt_set}})
    pcr.acq.status.return_value.session = {'data': {'V_AC': v_ac}}
    pcr.get_output.return_value.session = {'data': {'output': output}}


@pytest.mark.parametrize("do_setup", [True, False])
@pytest.mark.parametrize("smurf_error", [True, False])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_calibrate_tau(patch_clients_lat, do_setup, smurf_error):
    if smurf_error:
        mocked_response = OCSReply(
            0, 'msg', {'success': False, 'op_name': 'stream'})
        stimulator.run.CLIENTS['smurf'][0].stream.wait.side_effect = [mocked_response]
        stimulator.run.CLIENTS['smurf'][1].stream.wait.side_effect = [mocked_response]
        stimulator.run.CLIENTS['smurf'][2].stream.wait.side_effect = [mocked_response]

    stimulator.calibrate_tau(do_setup=do_setup)

    # setup test
    if do_setup:
        stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=1)
        stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_any_call(accl_time=10, decl_time=10)

        # start rotation
        stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_called_with(forward=True)

    # speed setting
    for speed in [225, 495, 945, 1395, 1845, 2205]:
        stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_any_call(speed=speed)

    # stop test
    stimulator.run.CLIENTS['stimulator']['blh'].stop_rotation.assert_called_with()
    stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=0)


@pytest.mark.parametrize("do_setup", [True, False])
@pytest.mark.parametrize("smurf_error", [True, False])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_calibrate_gain(patch_clients_lat, do_setup, smurf_error):
    # setup test
    if smurf_error:
        mocked_response = OCSReply(
            0, 'msg', {'success': False, 'op_name': 'stream'})
        stimulator.run.CLIENTS['smurf'][0].stream.wait.side_effect = [mocked_response]
        stimulator.run.CLIENTS['smurf'][1].stream.wait.side_effect = [mocked_response]
        stimulator.run.CLIENTS['smurf'][2].stream.wait.side_effect = [mocked_response]
    stimulator.calibrate_gain(do_setup=do_setup)

    if do_setup:
        stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=1)
        stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_any_call(accl_time=10, decl_time=10)

        # start rotation
        stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_called_with(forward=True)

    stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_any_call(speed=90)

    # stop test
    stimulator.run.CLIENTS['stimulator']['blh'].stop_rotation.assert_called_with()
    stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=0)


@pytest.mark.parametrize("smurf_error", [True, False])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_calibrate_gain_tau(patch_clients_lat, smurf_error):
    # setup test
    if smurf_error:
        mocked_response = OCSReply(
            0, 'msg', {'success': False, 'op_name': 'stream'})
        stimulator.run.CLIENTS['smurf'][0].stream.wait.side_effect = [mocked_response]
        stimulator.run.CLIENTS['smurf'][1].stream.wait.side_effect = [mocked_response]
        stimulator.run.CLIENTS['smurf'][2].stream.wait.side_effect = [mocked_response]
    stimulator.calibrate_gain_tau()

    stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=1)
    stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_any_call(accl_time=10, decl_time=10)

    # start rotation
    stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_called_with(forward=True)

    stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_any_call(speed=90)

    # stop test
    stimulator.run.CLIENTS['stimulator']['blh'].stop_rotation.assert_called_with()
    stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=0)


@pytest.mark.parametrize("method,on_off", [
    (stimulator.open_shutter, 1),
    (stimulator.close_shutter, 0),
])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_shutter(patch_clients_lat, method, on_off):
    method()
    stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_called_with(relay_number=1, on_off=on_off)


@pytest.mark.parametrize("start", [True, False])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_rotate(patch_clients_lat, start):
    stimulator.rotate(100, forward=True, start=start)
    stimulator.run.CLIENTS['stimulator']['blh'].set_values.assert_called_with(speed=100)
    if start:
        stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_called_with(forward=True)
    else:
        stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_not_called()


@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_stop_rotation(patch_clients_lat):
    stimulator.stop_rotation()
    stimulator.run.CLIENTS['stimulator']['blh'].stop_rotation.assert_called_with()


@pytest.mark.parametrize("volt,v_ac,force,check_called", [
    (10, 10, False, True),
    (10, 0, True, False),
])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_set_heater_voltage(patch_clients_lat, volt, v_ac, force, check_called):
    pcr = stimulator.run.CLIENTS['stimulator']['pcr500ma']
    _configure_pcr(pcr, v_ac=v_ac)
    stimulator.set_heater_voltage(volt, force=force)
    if check_called:
        pcr.acq.status.assert_called()
    else:
        pcr.acq.status.assert_not_called()
    pcr.set_volt_ac.assert_called_with(volt_set=volt)


@pytest.mark.parametrize("volt,v_ac,exc", [
    (10, 0, RuntimeError),
    (51, 0, AssertionError),
])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_set_heater_voltage_error(patch_clients_lat, volt, v_ac, exc):
    pcr = stimulator.run.CLIENTS['stimulator']['pcr500ma']
    _configure_pcr(pcr, v_ac=v_ac)
    with pytest.raises(exc):
        stimulator.set_heater_voltage(volt)


@pytest.mark.parametrize("output,raises", [
    (False, False),
    (True, True),
])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_set_to_0V_heater(patch_clients_lat, output, raises):
    pcr = stimulator.run.CLIENTS['stimulator']['pcr500ma']
    _configure_pcr(pcr, output=output)
    if raises:
        with pytest.raises(RuntimeError):
            stimulator.set_to_0V_heater()
    else:
        stimulator.set_to_0V_heater()
        pcr.set_volt_ac.assert_called_with(volt_set=0)


@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_ramp_heater(patch_clients_lat):
    pcr = stimulator.run.CLIENTS['stimulator']['pcr500ma']
    _configure_pcr(pcr, volt_set=0, output=True)
    with patch('sorunlib.stimulator.set_heater_voltage') as mock_set_voltage:
        stimulator.ramp_heater(3)
    calls = [c.args[0] for c in mock_set_voltage.call_args_list]
    assert calls == [1, 2, 3]


@pytest.mark.parametrize("volt,output,exc", [
    (3, False, RuntimeError),
    (51, True, AssertionError),
])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_ramp_heater_error(patch_clients_lat, volt, output, exc):
    pcr = stimulator.run.CLIENTS['stimulator']['pcr500ma']
    _configure_pcr(pcr, volt_set=0, output=output)
    with pytest.raises(exc):
        stimulator.ramp_heater(volt)


@pytest.mark.parametrize("output,force", [
    (True, False),
    (False, False),
    (False, True),
])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_set_heater_output(patch_clients_lat, output, force):
    pcr = stimulator.run.CLIENTS['stimulator']['pcr500ma']
    stimulator.set_heater_output(output, force=force)
    pcr.set_output.assert_called_with(output=output, force=force)
