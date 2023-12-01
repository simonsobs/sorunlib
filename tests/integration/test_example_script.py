import datetime as dt
from unittest.mock import MagicMock, patch

from sorunlib import *

# should import from common place, duplicating construction in smurf testing module


def _mock_smurf_client(instance_id):
    smurf = MagicMock()
    smurf.instance_id = instance_id
    smurf.take_bias_steps = MagicMock()
    smurf.take_iv = MagicMock()

    return smurf


def mocked_clients(test_mode):
    smurf_ids = ['smurf1', 'smurf2', 'smurf3']
    smurfs = [_mock_smurf_client(id_) for id_ in smurf_ids]
    clients = {'acu': MagicMock(),
               'smurf': smurfs}

    return clients


# patch out time.sleep so we don't actually wait during testing
@patch('sorunlib.commands.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
def test_script():
    initialize()
    # wait until 1 second in future
    wait_until((dt.datetime.utcnow() + dt.timedelta(seconds=1)).isoformat())
    acu.move_to(39.39, 64.27)
    smurf.iv_curve()
    smurf.bias_step()
    # wait until 1 second in future
    wait_until((dt.datetime.utcnow() + dt.timedelta(seconds=1)).isoformat())
    seq.scan(description='test', stop_time=(dt.datetime.utcnow()
             + dt.timedelta(seconds=1)).isoformat(), width=20.)
    smurf.bias_step()
