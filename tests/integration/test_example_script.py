import datetime as dt
from unittest.mock import MagicMock, patch

from util import mocked_clients

from sorunlib import *


# patch out time.sleep so we don't actually wait during testing
@patch('sorunlib.commands.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
def test_script():
    initialize()
    # wait until 1 second in future
    wait_until((dt.datetime.utcnow() + dt.timedelta(seconds=1)).isoformat())
    acu.move_to(39.39, 64.27)
    smurf.iv_curve()
    smurf.bias_step()
    # wait until 1 second in future
    wait_until((dt.datetime.utcnow() + dt.timedelta(seconds=1)).isoformat())
    seq.scan(description='test', stop_time=(dt.datetime.utcnow()
             + dt.timedelta(seconds=1)).isoformat(), width=20.)
    smurf.bias_step()
