import os

from unittest.mock import MagicMock, patch

from sorunlib import util

os.environ["OCS_CONFIG_DIR"] = "./test_util/"


def mock_registry_client(*args, **kwargs):
    """Mock out the client connection to the registry. Returning an example of
    the session object that is inspected to find agent instances on the network.

    """
    client = MagicMock()
    session_dict = {'session_id': 0,
                    'op_name': 'main',
                    'op_code': 3,
                    'status': 'running',
                    'success': None,
                    'start_time': 1669919099.7585046,
                    'end_time': None,
                    'data': {
                        'observatory.smurf-file-emulator-5': {
                            'expired': False,
                            'time_expired': None,
                            'last_updated': 1669935108.8366735,
                            'op_codes': {
                                'uxm_setup': 1,
                                'uxm_relock': 1,
                                'take_iv': 1,
                                'take_bias_steps': 1,
                                'take_bgmap': 1,
                                'bias_dets': 1,
                                'take_noise': 1,
                                'stream': 1},
                            'agent_class': 'SmurfFileEmulator',
                            'agent_address': 'observatory.smurf-file-emulator-5'},
                        'observatory.smurf-file-emulator-7': {
                            'expired': False,
                            'time_expired': None,
                            'last_updated': 1669935108.989246,
                            'op_codes': {
                                'uxm_setup': 1,
                                'uxm_relock': 1,
                                'take_iv': 1,
                                'take_bias_steps': 1,
                                'take_bgmap': 1,
                                'bias_dets': 1,
                                'take_noise': 1,
                                'stream': 1},
                            'agent_class': 'SmurfFileEmulator',
                            'agent_address': 'observatory.smurf-file-emulator-7'},
                        'observatory.fake-data-1': {
                            'expired': True,
                            'time_expired': None,
                            'last_updated': 1669935108.989246,
                            'op_codes': {
                                'acq': 3,
                                'count': 3,
                                'set_heartbeat': 1,
                                'delay_task': 1},
                            'agent_class': 'FakeDataAgent',
                            'agent_address': 'observatory.fake-data-1'},
                        'observatory.acu-sat1': {
                            'expired': False,
                            'time_expired': None,
                            'last_updated': 1669997169.469505,
                            'op_codes': {
                                'monitor': 3,
                                'broadcast': 3,
                                'generate_scan': 1,
                                'go_to': 1,
                                'constant_velocity_scan': 1,
                                'fromfile_scan': 1,
                                'set_boresight': 1,
                                'stop_and_clear': 1},
                            'agent_class': 'ACUAgent',
                            'agent_address': 'observatory.acu-sat1'}}}
    client.main.status = MagicMock(return_value=(None, None, session_dict))
    return client


def test_load_site_config():
    cfg = util._load_site_config()
    assert 'localhost' in cfg.hosts
    assert 'ocs-docker' in cfg.hosts
    assert 'registry_address' in cfg.hub.data


def test_find_instances():
    instances = util._find_instances('PysmurfController')
    assert instances == ['pysmurf-controller']


def test_find_instances_host():
    instances = util._find_instances('PysmurfController', host='localhost')
    assert instances == []


@patch('sorunlib.util.OCSClient', mock_registry_client)
def test_find_active_instances():
    instances = util._find_active_instances('SmurfFileEmulator')
    assert 'smurf-file-emulator-5' in instances
    assert 'smurf-file-emulator-7' in instances


@patch('sorunlib.util.OCSClient', mock_registry_client)
def test_find_active_instances_expired():
    instances = util._find_active_instances('FakeDataAgent')
    assert 'fake-data-1' not in instances


@patch('sorunlib.util.OCSClient', mock_registry_client)
def test_create_clients():
    clients = util.create_clients()
    assert 'acu' in clients
    assert 'smurf' in clients
    assert len(clients['smurf']) == 0  # since we're not in test_mode


@patch('sorunlib.util.OCSClient', mock_registry_client)
def test_create_clients_test_mode():
    clients = util.create_clients(test_mode=True)
    assert 'acu' in clients
    assert 'smurf' in clients
    assert len(clients['smurf']) == 2
