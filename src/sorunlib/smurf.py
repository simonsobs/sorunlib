import sorunlib as run
from sorunlib._internal import check_response


def set_targets(targets):
    """Set the target pysmurf-controller Agents that sorunlib will command.

    Args:
        targets (list): List of pysmurf-controller instance-ids to send future
            commands to. This must be a subset of the currently active clients
            list.

    Notes:
        This modifies the global ``sorunlib.CLIENTS`` list.

    """
    _smurf_clients = []
    for smurf in run.CLIENTS['smurf']:
        if smurf.instance_id in targets:
            _smurf_clients.append(smurf)

    run.CLIENTS['smurf'] = _smurf_clients


def bias_step(tag=None):
    """Perform a bias step on all SMuRF Controllers.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_bias_steps.start(tag=tag)

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.take_bias_steps.wait()
        check_response(resp)


def iv_curve(tag=None):
    """Perform an iv curve on all SMuRF Controllers.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_iv.start(tag=tag)

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.take_iv.wait()
        check_response(resp)


def uxm_setup():
    """Perform first-time setup procedure for a UXM."""
    for smurf in run.CLIENTS['smurf']:
        smurf.uxm_setup.start()

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.uxm_setup.wait()
        check_response(resp)


def uxm_relock(test_mode=False):
    """Relocks detectors to existing tune if setup has already been run.

    Args:
        test_mode (bool): Run uxm_setup() task in test_mode, removing emulated
            wait times.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.uxm_relock.start(test_mode=test_mode)

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.uxm_relock.wait()
        check_response(resp)


def bias_dets():
    """Bias the detectors on all SMuRF Controllers."""
    for smurf in run.CLIENTS['smurf']:
        smurf.bias_dets.start()

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.bias_dets.wait()
        check_response(resp)


def take_bgmap(tag=None):
    """Take a bgmap on all SMuRF Controllers.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_bgmap.start(tag=tag)

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.take_bgmap.wait()
        check_response(resp)


def take_noise(tag=None):
    """Measure noise statistics from a short, 30 second, timestream.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_noise.start(tag=tag)

    for smurf in run.CLIENTS['smurf']:
        resp = smurf.take_noise.wait()
        check_response(resp)


def stream(state, tag=None):
    """Stream data on all SMuRF Controllers.

    Args:
        state (str): Streaming state, either 'on' or 'off'.
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.

    """
    if state.lower() == 'on':
        for smurf in run.CLIENTS['smurf']:
            smurf.stream.start(tag=tag)

    else:
        for smurf in run.CLIENTS['smurf']:
            smurf.stream.stop()
            resp = smurf.stream.wait()
            check_response(resp)
