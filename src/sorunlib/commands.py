import time
import datetime as dt

from .util import create_clients


class ObservationRunner:
    def __init__(self):
        self.clients = create_clients()

    def move_to(self, az, el, wait=1):
        """Move telescope to specified coordinates.

        """
        self.clients['acu'].go_to(az, el)

    def start_scan(self):
        pass

    def bias_step(self):
        """Perform a bias step on all SMuRF Controllers"""
        for smurf in self.clients['smurf']:
            smurf.run.start('bias_step.sh')

        # group wait - does this work?
        for smurf in self.clients['smurf']:
            smurf.run.wait()

    def iv_curve(self):
        """Perform a bias step on all SMuRF Controllers"""
        for smurf in self.clients['smurf']:
            smurf.run.start('iv_curve.sh')

        # group wait - does this work?
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
