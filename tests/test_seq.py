import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
os.environ["SORUNLIB_CONFIG"] = "./data/example_config.yaml"
import datetime as dt

import pytest
from unittest.mock import MagicMock, patch

import sorunlib
from sorunlib import seq

from util import create_patch_clients


patch_clients = create_patch_clients('satp')


@patch('sorunlib.commands.time.sleep', MagicMock())
def test_scan(patch_clients):
    target = dt.datetime.now() + dt.timedelta(seconds=1)
    seq.scan(description='test', stop_time=target.isoformat(), width=20.)


@patch('sorunlib.commands.time.sleep', MagicMock())
def test_scan_failed_to_start(patch_clients):
    # Setup mock OCSReply without session object
    mock_reply = MagicMock()
    mock_reply.session = None
    sorunlib.CLIENTS['acu'].generate_scan.start = MagicMock(return_value=mock_reply)

    target = dt.datetime.now() + dt.timedelta(seconds=1)
    with pytest.raises(Exception):
        seq.scan(description='test', stop_time=target.isoformat(), width=20.)
