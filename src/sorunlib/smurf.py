import sorunlib as run


def bias_step():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.take_bias_steps.start()

    for smurf in run.CLIENTS['smurf']:
        smurf.take_bias_steps.wait()


def iv_curve():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.take_iv.start()

    for smurf in run.CLIENTS['smurf']:
        smurf.take_iv.wait()
