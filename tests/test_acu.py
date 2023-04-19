import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

import pytest

from unittest.mock import MagicMock, patch

from ocs.ocs_client import OCSReply
from sorunlib import acu


def mocked_clients(test_mode):
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


@patch('sorunlib.create_clients', mocked_clients)
def test_move_to():
    acu.run.initialize(test_mode=True)
    acu.move_to(180, 60)
    acu.run.CLIENTS['acu'].go_to.assert_called_with(az=180, el=60)


@patch('sorunlib.create_clients', mocked_clients)
def test_move_to_failed():
    acu.run.initialize()
    mocked_response = OCSReply(
        0, 'msg', {'success': False, 'op_name': 'go_to'})
    acu.run.CLIENTS['acu'].go_to.side_effect = [mocked_response]
    with pytest.raises(RuntimeError):
        acu.move_to(180, 90)
