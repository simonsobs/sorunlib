import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
import pytest
import datetime as dt

from unittest.mock import MagicMock, patch

from sorunlib.commands import wait


def test_wait_in_past():
    with pytest.raises(AssertionError):
        wait("2020-01-01T00:00:00")


# patch out time.sleep so we don't actually wait during testing
@patch('sorunlib.commands.time.sleep', MagicMock())
def test_wait():
    target = dt.datetime.now() + dt.timedelta(seconds=1)
    wait(target.isoformat())
