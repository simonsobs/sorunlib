import datetime as dt
from unittest.mock import MagicMock, patch

import sorunlib as run

from sorunlib import *
from sorunlib.commands import *

def mocked_clients():
    clients = {'acu': MagicMock(),
               'smurf': [MagicMock(), MagicMock(), MagicMock()]}

    return clients


# patch out time.sleep so we don't actually wait during testing
@patch('sorunlib.commands.time.sleep', MagicMock())
@patch('sorunlib.create_clients', mocked_clients)
def test_script():
    # We're doing
    #import sorunlib as run
    #
    #from sorunlib import *
    #from sorunlib.commands import *

    run.init_clients()
    # want to effectively run
    # import sorunlib as run
    # run.init()
    # to have all needed imports setup for us

    wait((dt.datetime.now() + dt.timedelta(seconds=1)).isoformat())  # wait until 1 second in future
    acu.move_to(39.39, 64.27)
    smurf.bias_step()
    smurf.iv_curve()
    wait((dt.datetime.now() + dt.timedelta(seconds=1)).isoformat())  # wait until 1 second in future
    seq.scan()
    smurf.bias_step()
    smurf.iv_curve()
