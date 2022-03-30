import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"

from unittest.mock import MagicMock, patch

from sorunlib import acu


def mocked_clients(test_mode):
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


@patch('sorunlib.create_clients', mocked_clients)
def test_move_to():
    acu.run.initialize()
    acu.move_to(180, 60)
    acu.run.CLIENTS['acu'].go_to.assert_called_with(180, 60, None)
