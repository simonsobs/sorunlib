from unittest.mock import MagicMock

from ocs.ocs_agent import OpSession


def create_session(op_name):
    """Create an OpSession with a mocked app for testing."""
    mock_app = MagicMock()
    session = OpSession(1, op_name, app=mock_app)

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


def mocked_clients(**kwargs):
    smurf_ids = ['smurf1', 'smurf2', 'smurf3']
    smurfs = [_mock_smurf_client(id_) for id_ in smurf_ids]

    clients = {'acu': MagicMock(),
               'smurf': smurfs}

    return clients
