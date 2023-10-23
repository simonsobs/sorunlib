import time

import sorunlib as run
from sorunlib._internal import check_response

# Timing between commanding separate SMuRF Controllers
# Yet to be determined in the field. Eventually might need this to be unique
# per operation. Also, move to configuration file once sorunlib has one.
CRYO_WAIT = 120


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


def bias_step(tag=None, concurrent=True, settling_time=None):
    """Perform a bias step on all SMuRF Controllers.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. If None, defaults to a fixed wait
            time of 120 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_bias_steps.start(tag=tag)
        if not concurrent:
            resp = smurf.take_bias_steps.wait()
            check_response(resp)

            # Allow cryo to settle
            wait = settling_time if settling_time else CRYO_WAIT
            time.sleep(wait)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.take_bias_steps.wait()
            check_response(resp)


def iv_curve(tag=None, concurrent=True, settling_time=None):
    """Perform an iv curve on all SMuRF Controllers.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. If None, defaults to a fixed wait
            time of 120 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_iv.start(tag=tag)
        if not concurrent:
            resp = smurf.take_iv.wait()
            check_response(resp)

            # Allow cryo to settle
            wait = settling_time if settling_time else CRYO_WAIT
            time.sleep(wait)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.take_iv.wait()
            check_response(resp)


def uxm_setup(concurrent=True, settling_time=0):
    """Perform first-time setup procedure for a UXM.

    Args:
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. Defaults to 0 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.uxm_setup.start()
        if not concurrent:
            resp = smurf.uxm_setup.wait()
            check_response(resp)

            # Allow cryo to settle
            time.sleep(settling_time)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.uxm_setup.wait()
            check_response(resp)


def uxm_relock(test_mode=False, concurrent=True, settling_time=0):
    """Relocks detectors to existing tune if setup has already been run.

    Args:
        test_mode (bool): Run uxm_setup() task in test_mode, removing emulated
            wait times.
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. Defaults to 0 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.uxm_relock.start(test_mode=test_mode)
        if not concurrent:
            resp = smurf.uxm_relock.wait()
            check_response(resp)

            # Allow cryo to settle
            time.sleep(settling_time)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.uxm_relock.wait()
            check_response(resp)


def bias_dets(concurrent=True, settling_time=0):
    """Bias the detectors on all SMuRF Controllers.

    Args:
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. Defaults to 0 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.bias_dets.start()
        if not concurrent:
            resp = smurf.bias_dets.wait()
            check_response(resp)

            # Allow cryo to settle
            time.sleep(settling_time)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.bias_dets.wait()
            check_response(resp)


def take_bgmap(tag=None, concurrent=True, settling_time=0):
    """Take a bgmap on all SMuRF Controllers.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. Defaults to 0 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_bgmap.start(tag=tag)
        if not concurrent:
            resp = smurf.take_bgmap.wait()
            check_response(resp)

            # Allow cryo to settle
            time.sleep(settling_time)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.take_bgmap.wait()
            check_response(resp)


def take_noise(tag=None, concurrent=True, settling_time=0):
    """Measure noise statistics from a short, 30 second, timestream.

    Args:
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.
        concurrent (bool, optional): A bool which determines how the operation
            is run across the active SMuRF controllers. It runs in parallel if
            True, and in series if False.
        settling_time (float, optional):
            Time in seconds to wait between operation runs across the active
            SMuRF controlls if *not* running concurrently. If running
            concurrently this is ignored. Defaults to 0 seconds.

    """
    for smurf in run.CLIENTS['smurf']:
        smurf.take_noise.start(tag=tag)
        if not concurrent:
            resp = smurf.take_noise.wait()
            check_response(resp)

            # Allow cryo to settle
            time.sleep(settling_time)

    if concurrent:
        for smurf in run.CLIENTS['smurf']:
            resp = smurf.take_noise.wait()
            check_response(resp)


def stream(state, tag=None, subtype=None):
    """Stream data on all SMuRF Controllers.

    Args:
        state (str): Streaming state, either 'on' or 'off'.
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation.
        subtype (str, optional): Operation subtype used to tag the stream.

    """
    if state.lower() == 'on':
        for smurf in run.CLIENTS['smurf']:
            smurf.stream.start(subtype=subtype, tag=tag)

    else:
        for smurf in run.CLIENTS['smurf']:
            smurf.stream.stop()
            resp = smurf.stream.wait()
            check_response(resp)
