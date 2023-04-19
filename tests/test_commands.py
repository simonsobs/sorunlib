import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
import pytest
import datetime as dt

from unittest.mock import MagicMock, patch

from sorunlib.commands import wait


@pytest.mark.parametrize("target_time", ["2020-01-01T00:00:00", "2020-01-01T00:00:00+00:00"])
def test_wait_in_past(target_time):
    with pytest.raises(AssertionError):
        wait(target_time)


def test_wait_unsupported_tz():
    with pytest.raises(ValueError):
        tz = dt.timezone(offset=dt.timedelta(hours=5))
        t = dt.datetime.now(tz).isoformat()  # i.e. '2023-04-22T00:59:56.264293+05:00'
        wait(t)


# patch out time.sleep so we don't actually wait during testing
@patch('sorunlib.commands.time.sleep', MagicMock())
def test_wait():
    target = dt.datetime.now() + dt.timedelta(seconds=1)
    wait(target.isoformat())
