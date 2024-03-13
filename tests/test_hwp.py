import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

import pytest

from sorunlib import hwp

from util import create_patch_clients


patch_clients_satp = create_patch_clients('satp')


@pytest.mark.parametrize("active", [True, False])
def test_stop(patch_clients_satp, active):
    hwp.stop(active=active)
    if active:
        hwp.run.CLIENTS['hwp'].brake.assert_called_with()
    else:
        hwp.run.CLIENTS['hwp'].pmx_off.assert_called()


def test_stop_brake_voltage(patch_clients_satp):
    VOLTAGE = 5.0
    hwp.stop(active=True, brake_voltage=VOLTAGE)
    hwp.run.CLIENTS['hwp'].brake.assert_called_with(brake_voltage=VOLTAGE)


def test_set_freq(patch_clients_satp):
    hwp.set_freq(freq=2.0)
    hwp.run.CLIENTS['hwp'].pid_to_freq.assert_called_with(target_freq=2.0)
