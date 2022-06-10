import sorunlib as run


def tune_dets():
    """Perform detector tuning on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.tune_dets.start(test_mode=run.TEST_MODE)

    for smurf in run.CLIENTS['smurf']:
        smurf.tune_dets.wait()


def iv_curve():
    """Perform an iv curve on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.take_iv.start()

    for smurf in run.CLIENTS['smurf']:
        smurf.take_iv.wait()


def bias_dets():
    """Bias the detectors on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.bias_dets.start()

    for smurf in run.CLIENTS['smurf']:
        smurf.bias_dets.wait()


def bias_step():
    """Perform a bias step on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.take_bias_steps.start()

    for smurf in run.CLIENTS['smurf']:
        smurf.take_bias_steps.wait()


def stream():
    """Stream data on all SMuRF Controllers"""
    for smurf in run.CLIENTS['smurf']:
        smurf.stream.start()

    for smurf in run.CLIENTS['smurf']:
        print(smurf.stream.status())
