import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

import pytest

from ocs.ocs_client import OCSReply
from sorunlib import acu

from util import create_patch_clients


patch_clients_satp = create_patch_clients('satp')
patch_clients_lat = create_patch_clients('ccat')


def test_move_to(patch_clients_satp):
    acu.move_to(180, 60)
    acu.run.CLIENTS['acu'].go_to.assert_called_with(az=180, el=60)


def test_move_to_failed(patch_clients_satp):
    mocked_response = OCSReply(
        0, 'msg', {'success': False, 'op_name': 'go_to'})
    acu.run.CLIENTS['acu'].go_to.side_effect = [mocked_response]
    with pytest.raises(RuntimeError):
        acu.move_to(180, 90)


def test_set_boresight(patch_clients_satp):
    acu.set_boresight(20)
    acu.run.CLIENTS['acu'].set_boresight.assert_called_with(target=20)


def test_set_boresight_lat(patch_clients_lat):
    with pytest.raises(RuntimeError):
        acu.set_boresight(20)


def test_set_scan_params(patch_clients_satp):
    acu.set_scan_params(az_speed=2, az_accel=2, reset=True)
    acu.run.CLIENTS['acu'].set_scan_params.assert_called_with(
        az_speed=2,
        az_accel=2,
        reset=True)
