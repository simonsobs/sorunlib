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

    def wait(self):
        pass
