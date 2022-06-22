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
        client.take_bias_steps.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
def test_iv_curve():
    smurf.run.initialize(test_mode=True)
    smurf.iv_curve()
    for client in smurf.run.CLIENTS['smurf']:
        client.take_iv.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
def test_tune_dets():
    smurf.run.initialize(test_mode=True)
    smurf.tune_dets(test_mode=True)
    for client in smurf.run.CLIENTS['smurf']:
        client.tune_dets.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
def test_bias_dets():
    smurf.run.initialize(test_mode=True)
    smurf.bias_dets()
    for client in smurf.run.CLIENTS['smurf']:
        client.bias_dets.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
def test_stream():
    smurf.run.initialize(test_mode=True)
    smurf.stream(state='on')
    for client in smurf.run.CLIENTS['smurf']:
        client.stream.start.assert_called_once()
