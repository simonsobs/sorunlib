import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

import pytest
from unittest.mock import MagicMock, patch

from sorunlib import stimulator

from util import create_patch_clients


patch_clients_lat = create_patch_clients('lat')


@pytest.mark.parametrize("do_setup", [True, False])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_calibrate_tau(patch_clients_lat, do_setup):
    stimulator.calibrate_tau(do_setup=do_setup)

@pytest.mark.parametrize("do_setup", [True, False])
@patch('sorunlib.stimulator.time.sleep', MagicMock())
def test_calibrate_gain(patch_clients_lat, do_setup):
    stimulator.calibrate_gain(do_setup=do_setup)
