import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

from unittest.mock import MagicMock, patch

from sorunlib import smurf


def mocked_clients(test_mode):
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


@patch('sorunlib.create_clients', mocked_clients)
def test_bias_step():
    smurf.run.initialize(test_mode=True)
    smurf.bias_step()
    for client in smurf.run.CLIENTS['smurf']:
        client.run.start.assert_called_with('bias_step.sh')
        client.run.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
def test_iv_curve():
    smurf.run.initialize(test_mode=True)
    smurf.iv_curve()
    for client in smurf.run.CLIENTS['smurf']:
        client.run.start.assert_called_with('iv_curve.sh')
        client.run.start.assert_called_once()
