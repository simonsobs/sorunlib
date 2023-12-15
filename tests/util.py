import pytest

from unittest.mock import MagicMock

import ocs
from ocs.ocs_agent import OpSession
from ocs.ocs_client import OCSReply


def create_session(op_name, status=None, success=None):
    """Create an OpSession with a mocked app for testing."""
    mock_app = MagicMock()
    session = OpSession(1, op_name, app=mock_app)
    session.op_name = 'test_op'
    if status is not None:
        session.set_status(status)
    session.success = success

    return session


# Mocked Clients
# This should be considered the authoritative source for mocking the CLIENTS
# dict. Otherwise each test ends up implementing their own version of the
# clients.
#
# Tests that need to interact with a client should import from here unless
# they're testing some specific unique response from a client, like if it
# raises an exception under certain conditions.
def _mock_smurf_client(instance_id):
    smurf = MagicMock()
    smurf.instance_id = instance_id
    smurf.take_bias_steps = MagicMock()
    smurf.take_iv = MagicMock()
    smurf.uxm_setup = MagicMock()
    smurf.uxm_relock = MagicMock()
    smurf.bias_dets = MagicMock()
    smurf.set_biases = MagicMock()
    smurf.zero_biases = MagicMock()
    smurf.take_bgmap = MagicMock()
    smurf.take_noise = MagicMock()

    return smurf


def _mock_acu_client(platform_type):
    """Create an ACU client with mock monitor Process session.data."""
    acu_client = MagicMock()
    session = create_session('monitor')
    session.data = {'PlatformType': platform_type}
    reply = OCSReply(ocs.OK, 'msg', session.encoded())
    acu_client.monitor.status = MagicMock(return_value=reply)

    return acu_client


def mocked_clients(**kwargs):
    platform_type = kwargs.get('platform_type', 'satp')

    smurf_ids = ['smurf1', 'smurf2', 'smurf3']
    smurfs = [_mock_smurf_client(id_) for id_ in smurf_ids]

    clients = {'acu': _mock_acu_client(platform_type),
               'smurf': smurfs,
               'wiregrid': {'actuator': MagicMock(),
                            'encoder': MagicMock(),
                            'kikusui': MagicMock(),
                            'labjack': MagicMock()}}

    return clients


def create_patch_clients(platform_type, autouse=False):
    """Create patch_clients fixture that patches out the global CLIENTS list
    with a set of mocked clients using the ``pytest-mock`` plugin.

    Args:
        platform_type (str): Either 'satp' or 'ccat'.
        autouse (bool): Whether to enable 'autouse' on the fixture. This will
            enable the fixture for all tests within a test module.

    Returns:
        function: A pytest fixture that patches out ``sorunlib.CLIENTS`` with a
            set of mocked clients.

    """
    @pytest.fixture(autouse=autouse)
    def patch_clients(mocker):
        mocker.patch('sorunlib.CLIENTS', mocked_clients(platform_type=platform_type))

    return patch_clients
