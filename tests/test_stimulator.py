import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
os.environ["SORUNLIB_CONFIG"] = "./data/example_config.yaml"

import pytest
from unittest.mock import MagicMock, patch

from ocs.ocs_client import OCSReply
from sorunlib import stimulator

from util import create_patch_clients


patch_clients_lat = create_patch_clients('lat')


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
        stimulator.run.CLIENTS['stimulator']['blh'].set_value.assert_any_call(accl_time=10, decl_time=10)

        # start rotation
        stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_called_with(forward=True)

    # speed setting
    for speed in [225, 495, 945, 1395, 1845, 2205]:
        stimulator.run.CLIENTS['stimulator']['blh'].set_value.assert_any_call(speed=speed)

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
        stimulator.run.CLIENTS['stimulator']['blh'].set_value.assert_any_call(accl_time=10, decl_time=10)

        # start rotation
        stimulator.run.CLIENTS['stimulator']['blh'].start_rotation.assert_called_with(forward=True)

    stimulator.run.CLIENTS['stimulator']['blh'].set_value.assert_any_call(speed=90)

    # stop test
    stimulator.run.CLIENTS['stimulator']['blh'].stop_rotation.assert_called_with()
    stimulator.run.CLIENTS['stimulator']['ds378'].set_relay.assert_any_call(relay_number=1, on_off=0)
