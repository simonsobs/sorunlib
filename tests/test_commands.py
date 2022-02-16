import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
import pytest
import datetime as dt

from unittest.mock import MagicMock, patch

from sorunlib.commands import ObservationRunner


def mocked_clients():
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


class TestObservationRunner:
    @pytest.fixture
    @patch('sorunlib.commands.create_clients', mocked_clients)
    def run(self):
        """Setup an ObservationRunner with mocked Clients."""
        run = ObservationRunner()
        return run

    def test_start_scan(self, run):
        run.start_scan()

    def test_wait_in_past(self, run):
        with pytest.raises(AssertionError):
            run.wait("2020-01-01T00:00:00")

    # patch out time.sleep so we don't actually wait during testing
    @patch('sorunlib.commands.time.sleep', MagicMock())
    def test_wait(self, run):
        target = dt.datetime.now() + dt.timedelta(seconds=1)
        run.wait(target.isoformat())
