from .util import create_clients

CLIENTS = create_clients()


def move_to(az, el, wait=1):
    """Move telescope to specified coordinates.

    """
    CLIENTS['acu'].go_to(az, el)


def start_scan():
    pass


def bias_step():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in CLIENTS['smurf']:
        smurf.run.start('bias_step.sh')

    # group wait - does this work?
    for smurf in CLIENTS['smurf']:
        smurf.run.wait()


def iv_curve():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in CLIENTS['smurf']:
        smurf.run.start('iv_curve.sh')

    # group wait - does this work?
    for smurf in CLIENTS['smurf']:
        smurf.run.wait()


def wait():
    pass
