import time
import datetime as dt

from .util import create_clients


class ObservationRunner:
    """An object for running observations. It gathers the required clients
    for commanding the needed hardware, and provides methods for
    orchestrating actions across groups of Agents.

    Attributes:
        clients (dict): A dictionary of clients needed for orchestrating
            observations. See :func:`sorunlib.util.create_clients` for
            structure.

    """
    def __init__(self):
        self.clients = create_clients()

    def move_to(self, az, el, wait=None):
        """Move telescope to specified coordinates.

        Args:
            az (float): destination angle for the azimuthal axis
            el (float): destination angle for the elevation axis
            wait (float): amount of time to wait for motion to end

        """
        self.clients['acu'].go_to(az, el, wait)

    def start_scan(self):
        pass

    def bias_step(self):
        """Perform a bias step on all SMuRF Controllers"""
        for smurf in self.clients['smurf']:
            smurf.run.start('bias_step.sh')

        for smurf in self.clients['smurf']:
            smurf.run.wait()

    def iv_curve(self):
        """Perform a bias step on all SMuRF Controllers"""
        for smurf in self.clients['smurf']:
            smurf.run.start('iv_curve.sh')

        for smurf in self.clients['smurf']:
            smurf.run.wait()

    @staticmethod
    def wait(target_time):
        """Wait until a specified time.

        Args:
            target_time (str): Time in ISO format to wait until,
                i.e. "2015-10-21T07:28:00"

        """
        t0 = dt.datetime.now()
        t1 = dt.datetime.fromisoformat(target_time)

        assert t1 > t0, f"time {t1} is in the past"

        diff = t1-t0
        print(f"Waiting for {diff.total_seconds()} seconds")
        time.sleep(diff.total_seconds())
