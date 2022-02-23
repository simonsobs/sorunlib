import sorunlib as run


def bias_step():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.run.start('bias_step.sh')

    for smurf in run.CLIENTS['smurf']:
        smurf.run.wait()


def iv_curve():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.run.start('iv_curve.sh')

    for smurf in run.CLIENTS['smurf']:
        smurf.run.wait()
