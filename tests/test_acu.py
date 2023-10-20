import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

import pytest

from unittest.mock import MagicMock, patch

import ocs
from ocs.ocs_client import OCSReply
from sorunlib import acu

from util import create_session


def create_acu_client(platform_type):
    """Create an ACU client with mock monitor Process session.data.

    Args:
        platform_type (str): Either 'satp' or 'ccat'.

    """
    acu_client = MagicMock()
    session = create_session('monitor')
    session.data = {'PlatformType': platform_type}
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    acu_client.monitor.status = MagicMock(return_value=reply)

    return acu_client


def mocked_clients(test_mode):
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


@patch('sorunlib.create_clients', mocked_clients)
def test_move_to():
    acu.run.initialize(test_mode=True)
    acu.move_to(180, 60)
    acu.run.CLIENTS['acu'].go_to.assert_called_with(az=180, el=60)


@patch('sorunlib.create_clients', mocked_clients)
def test_set_boresight():
    acu.run.initialize(test_mode=True)
    acu.run.CLIENTS['acu'] = create_acu_client('satp')
    acu.set_boresight(20)
    acu.run.CLIENTS['acu'].set_boresight.assert_called_with(target=20)


@patch('sorunlib.create_clients', mocked_clients)
def test_set_boresight_lat():
    acu.run.initialize(test_mode=True)
    acu.run.CLIENTS['acu'] = create_acu_client('ccat')
    with pytest.raises(RuntimeError):
        acu.set_boresight(20)


@patch('sorunlib.create_clients', mocked_clients)
def test_move_to_failed():
    acu.run.initialize()
    mocked_response = OCSReply(
        0, 'msg', {'success': False, 'op_name': 'go_to'})
    acu.run.CLIENTS['acu'].go_to.side_effect = [mocked_response]
    with pytest.raises(RuntimeError):
        acu.move_to(180, 90)


@patch('sorunlib.create_clients', mocked_clients)
def test_set_scan_params():
    acu.run.initialize(test_mode=True)
    acu.set_scan_params(az_speed=2, az_accel=2, reset=True)
    acu.run.CLIENTS['acu'].set_scan_params.assert_called_with(
        az_speed=2,
        az_accel=2,
        reset=True)
