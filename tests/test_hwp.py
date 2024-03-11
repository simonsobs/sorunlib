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
        hwp.run.CLIENTS['hwp'].brake.assert_called()
    else:
        hwp.run.CLIENTS['hwp'].pmx_off.assert_called()
