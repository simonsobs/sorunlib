import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

from unittest.mock import MagicMock, patch

import pytest

from sorunlib import smurf


def _mock_smurf_client(instance_id):
    smurf = MagicMock()
    smurf.instance_id = instance_id

    return smurf


def mocked_clients(test_mode):
    smurf_ids = ['smurf1', 'smurf2', 'smurf3']
    smurfs = [_mock_smurf_client(id_) for id_ in smurf_ids]

    clients = {'acu': MagicMock(),
               'smurf': smurfs}

    return clients


@patch('sorunlib.create_clients', mocked_clients)
def test_set_targets():
    smurf.run.initialize(test_mode=True)
    smurf.set_targets(['smurf1'])
    assert len(smurf.run.CLIENTS['smurf']) == 1
    assert smurf.run.CLIENTS['smurf'][0].instance_id == 'smurf1'


@patch('sorunlib.smurf.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_bias_step(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.bias_step(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.take_bias_steps.start.assert_called_once()


@patch('sorunlib.smurf.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_iv_curve(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.iv_curve(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.take_iv.start.assert_called_once()


@patch('sorunlib.smurf.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_uxm_setup(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.uxm_setup(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.uxm_setup.start.assert_called_once()


@patch('sorunlib.smurf.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_uxm_relock(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.uxm_relock(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.uxm_relock.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_bias_dets(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.bias_dets(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.bias_dets.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_bgmap(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.take_bgmap(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.take_bgmap.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
@pytest.mark.parametrize("concurrent", [(True), (False)])
def test_take_noise(concurrent):
    smurf.run.initialize(test_mode=True)
    smurf.take_noise(concurrent=concurrent)
    for client in smurf.run.CLIENTS['smurf']:
        client.take_noise.start.assert_called_once()


@patch('sorunlib.create_clients', mocked_clients)
def test_stream():
    smurf.run.initialize(test_mode=True)
    smurf.stream(state='on')
    for client in smurf.run.CLIENTS['smurf']:
        client.stream.start.assert_called_once()
