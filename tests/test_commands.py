import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

from unittest.mock import MagicMock, patch

from sorunlib.commands import ObservationRunner


def mocked_clients():
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


@patch('sorunlib.commands.create_clients', mocked_clients)
def test_move_to():
    run = ObservationRunner()
    run.move_to(180, 60)
    run.clients['acu'].go_to.assert_called_with(180, 60)


@patch('sorunlib.commands.create_clients', mocked_clients)
def test_start_scan():
    run = ObservationRunner()
    run.start_scan()


@patch('sorunlib.commands.create_clients', mocked_clients)
def test_bias_step():
    run = ObservationRunner()
    run.bias_step()
    for client in run.clients['smurf']:
        client.run.start.assert_called_with('bias_step.sh')
        client.run.start.assert_called_once()


@patch('sorunlib.commands.create_clients', mocked_clients)
def test_iv_curve():
    run = ObservationRunner()
    run.iv_curve()
    for client in run.clients['smurf']:
        client.run.start.assert_called_with('iv_curve.sh')
        client.run.start.assert_called_once()


@patch('sorunlib.commands.create_clients', mocked_clients)
def test_wait():
    run = ObservationRunner()
    run.wait()
