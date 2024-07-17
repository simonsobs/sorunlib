import os
import time
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

import pytest

from unittest.mock import MagicMock, patch

import ocs
from ocs.ocs_client import OCSReply
from sorunlib import wiregrid

from util import create_session, create_patch_clients, mocked_clients

patch_clients = create_patch_clients('satp')


def create_acu_client(az, el, boresight):
    """Create an ACU client with mock monitor Process session.data.

    Args:
        az (float): Azimuth position.
        el (float): Elevation position.
        boresight (float): Boresight position.

    """
    acu_client = MagicMock()
    session = create_session('monitor')
    session.data = {'StatusDetailed': {'Azimuth current position': az,
                                       'Elevation current position': el,
                                       'Boresight current position': boresight}}
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    acu_client.monitor.status = MagicMock(return_value=reply)

    return acu_client


def create_labjack_client():
    """Create a labjack client with mock acq Process session.data."""
    client = MagicMock()
    session = create_session('acq')
    session.data = {
        "block_name": "sens",
        "data": {
            "AIN0C": 23.0,
            "AIN1C": 20.0,
            "AIN2C": 30.0,
        },
        "timestamp": time.time()
    }
    session.set_status('running')
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    client.acq.status = MagicMock(return_value=reply)

    return client


def create_actuator_client(motor):
    """Create an actuator client with mock acq Process session.data.

    Args:
        motor (int): Motor state, 0 is off, 1 is on.

    """
    client = MagicMock()
    session = create_session('acq')
    session.data = {'fields': {'motor': motor},
                    'timestamp': time.time()}
    session.set_status('running')
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    client.acq.status = MagicMock(return_value=reply)

    return client


def create_kikusui_client():
    """Create a kikusui client with mock IV_acq Process session.data."""
    client = MagicMock()
    session = create_session('IV_acq')
    session.data = {
        'fields': {
            'kikusui': {
                'volt': 12.0,
                'curr': 3.0,
                'voltset': 12.0,
                'currset': 3.0,
                'status': 1,
            }
        },
        'timestamp': time.time(),
    }
    session.set_status('running')
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    client.IV_acq.status = MagicMock(return_value=reply)

    return client


def create_encoder_client():
    """Create an encoder client with mock acq Process session.data."""
    client = MagicMock()
    session = create_session('acq')
    session.data = {
        'fields': {
            'encoder_data': {'last_updated': time.time()},
        },
        'timestamp': time.time(),
    }
    session.set_status('running')
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    client.acq.status = MagicMock(return_value=reply)

    return client


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test_insert():
    wiregrid.insert()
    wiregrid.run.CLIENTS['wiregrid']['actuator'].insert.assert_called_with()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test_insert_failed():
    mocked_response = OCSReply(
        0, 'msg', {'success': False, 'op_name': 'insert'})
    wiregrid.run.CLIENTS['wiregrid']['actuator'].insert.side_effect = [mocked_response]
    with pytest.raises(RuntimeError):
        wiregrid.insert()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test_eject():
    wiregrid.eject()
    wiregrid.run.CLIENTS['wiregrid']['actuator'].eject.assert_called_with()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test_eject_failed():
    mocked_response = OCSReply(
        0, 'msg', {'success': False, 'op_name': 'eject'})
    wiregrid.run.CLIENTS['wiregrid']['actuator'].eject.side_effect = [mocked_response]
    with pytest.raises(RuntimeError):
        wiregrid.eject()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
@patch('sorunlib.wiregrid.time.sleep', MagicMock())
def test_rotate_continuous():
    wiregrid.rotate(continuous=True)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].set_v.assert_called_once_with(volt=12)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].set_c.assert_called_once_with(current=3.0)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].set_on.assert_called_once()
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].set_off.assert_called_once()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
@patch('sorunlib.wiregrid.time.sleep', MagicMock())
def test_rotate_stepwise():
    wiregrid.rotate(continuous=False)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].set_v.assert_called_once_with(volt=12)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].set_c.assert_called_once_with(current=3.0)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].stepwise_rotation.assert_called_once_with(num_laps=1, stopped_time=10)


def test__verify_temp_response():
    session = create_session('test')
    session.data = {"data": {"TEST": 2}}
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    wiregrid._verify_temp_response(reply, 'TEST', 0)


def test__verify_temp_response_invalid():
    session = create_session('test')
    session.data = {"data": {"TEST": -10}}
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    with pytest.raises(RuntimeError):
        wiregrid._verify_temp_response(reply, 'TEST', 0)


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test__check_temperature_sensors():
    wiregrid.run.CLIENTS['wiregrid']['labjack'] = create_labjack_client()
    wiregrid._check_temperature_sensors()
    wiregrid.run.CLIENTS['wiregrid']['labjack'].acq.status.assert_called_once()


def test__check_telescope_position(patch_clients):
    wiregrid._check_telescope_position()
    wiregrid.run.CLIENTS['acu'].monitor.status.assert_called_once()


@pytest.mark.parametrize('el,boresight', [(40, 0), (50, 10)])
@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test__check_telescope_position_invalid(el, boresight):
    wiregrid.run.CLIENTS['acu'] = create_acu_client(180, el, boresight)
    with pytest.raises(RuntimeError):
        wiregrid._check_telescope_position()
    wiregrid.run.CLIENTS['acu'].monitor.status.assert_called_once()


@pytest.mark.parametrize('motor', [(0), (1)])
@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test__check_motor_on(motor):
    wiregrid.run.CLIENTS['wiregrid']['actuator'] = create_actuator_client(motor=motor)
    wiregrid._check_motor_on()
    if motor == 1:
        wiregrid.run.CLIENTS['wiregrid']['actuator'].acq.status.assert_called_once()
        wiregrid.run.CLIENTS['wiregrid']['actuator'].motor_on.assert_not_called()
    elif motor == 0:
        wiregrid.run.CLIENTS['wiregrid']['actuator'].acq.status.assert_called_once()
        wiregrid.run.CLIENTS['wiregrid']['actuator'].motor_on.assert_called_once()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test__check_motor_on_invalid_state():
    wiregrid.run.CLIENTS['wiregrid']['actuator'] = create_actuator_client(motor=3)
    with pytest.raises(RuntimeError):
        wiregrid._check_motor_on()
    wiregrid.run.CLIENTS['wiregrid']['actuator'].acq.status.assert_called_once()


@patch('sorunlib.wiregrid.run.CLIENTS', mocked_clients())
def test__check_agents_online():
    wiregrid.run.CLIENTS['wiregrid']['actuator'] = create_actuator_client(motor=1)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'] = create_kikusui_client()
    wiregrid.run.CLIENTS['wiregrid']['encoder'] = create_encoder_client()
    wiregrid.run.CLIENTS['wiregrid']['labjack'] = create_labjack_client()
    wiregrid._check_agents_online()
    wiregrid.run.CLIENTS['wiregrid']['actuator'].acq.status.assert_called_once()
    wiregrid.run.CLIENTS['wiregrid']['kikusui'].IV_acq.status.assert_called_once()
    wiregrid.run.CLIENTS['wiregrid']['encoder'].acq.status.assert_called()
    wiregrid.run.CLIENTS['wiregrid']['labjack'].acq.status.assert_called_once()


@pytest.mark.parametrize('continuous, el, tag',
                         [(True, 50, 'wiregrid, wg_continuous'),
                          (False, 90, 'wiregrid, wg_stepwise, wg_el90')])
@patch('sorunlib.wiregrid.time.sleep', MagicMock())
def test_calibrate_stepwise(patch_clients, continuous, el, tag):
    # Setup all mock clients
    wiregrid.run.CLIENTS['acu'] = create_acu_client(180, el, 0)
    wiregrid.run.CLIENTS['wiregrid']['actuator'] = create_actuator_client(motor=1)
    wiregrid.run.CLIENTS['wiregrid']['kikusui'] = create_kikusui_client()
    wiregrid.run.CLIENTS['wiregrid']['encoder'] = create_encoder_client()
    wiregrid.run.CLIENTS['wiregrid']['labjack'] = create_labjack_client()

    wiregrid.calibrate(continuous=continuous)
    # All other internal functions tested separately, just make sure smurf
    # stream is run
    for client in wiregrid.run.CLIENTS['smurf']:
        client.stream.start.assert_called_with(tag=tag, subtype='cal')
        client.stream.stop.assert_called()


def test__check_process_data_stale_data():
    with pytest.raises(RuntimeError):
        stale_time = time.time() - wiregrid.AGENT_TIMEDIFF_THRESHOLD
        wiregrid._check_process_data('test process', stale_time)
