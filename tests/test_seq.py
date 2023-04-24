import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
import datetime as dt

import pytest
from unittest.mock import MagicMock, patch

import sorunlib
from sorunlib import seq


def mocked_clients(test_mode):
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


@patch('sorunlib.create_clients', mocked_clients)
@patch('sorunlib.commands.time.sleep', MagicMock())
def test_scan():
    seq.run.initialize(test_mode=True)
    target = dt.datetime.now() + dt.timedelta(seconds=1)
    seq.scan(description='test', stop_time=target.isoformat(), width=20.)


@patch('sorunlib.create_clients', mocked_clients)
@patch('sorunlib.commands.time.sleep', MagicMock())
def test_scan_failed_to_start():
    seq.run.initialize(test_mode=True)

    # Setup mock OCSReply without session object
    mock_reply = MagicMock()
    mock_reply.session = None
    sorunlib.CLIENTS['acu'].generate_scan.start = MagicMock(return_value=mock_reply)

    target = dt.datetime.now() + dt.timedelta(seconds=1)
    with pytest.raises(Exception):
        seq.scan(description='test', stop_time=target.isoformat(), width=20.)
