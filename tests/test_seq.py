import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
import datetime as dt

from unittest.mock import MagicMock, patch

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
